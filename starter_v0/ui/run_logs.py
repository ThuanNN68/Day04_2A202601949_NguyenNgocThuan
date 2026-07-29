"""
run_logs.py — Tab Run Logs: dashboard metrics của runs/*.json.
Hiển thị: summary metrics, per-case table, version history chart.
"""

from __future__ import annotations
import json
import streamlit as st
from typing import Any


METRIC_LABELS = {
    "case_accuracy": "Case Accuracy",
    "tool_routing_accuracy": "Routing Accuracy",
    "argument_accuracy": "Arg Accuracy",
    "multiturn_accuracy": "Multi-turn Accuracy",
}


def render_run_logs_tab() -> None:
    """
    Render tab Run Logs.
    """
    from pathlib import Path
    import json
    import csv

    ROOT = Path(__file__).parent.parent
    runs_dir = ROOT / "runs"
    version_log_path = ROOT / "artifacts" / "version_log.csv"

    runs = []
    if runs_dir.exists():
        for p in sorted(runs_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                data["run_file"] = f"runs/{p.name}"
                runs.append(data)
            except Exception:
                pass

    version_log = []
    if version_log_path.exists():
        try:
            with open(version_log_path, encoding="utf-8") as f:
                version_log = list(csv.DictReader(f))
        except Exception:
            pass

    st.markdown("## 📊 Run Logs & Metrics")
    st.caption("Dashboard tổng hợp kết quả eval từ thư mục `runs/` và `version_log.csv` ")

    if not runs:
        st.info("Chưa có run log. Chạy `python run_eval.py` để có data.")
        return

    # ── Overall progression chart ─────────────────────────────
    st.markdown("### 📈 Metric Progression (v0 → latest)")
    _render_progression_chart(runs)

    st.markdown("---")

    # ── Version log table ─────────────────────────────────────
    st.markdown("### 📒 Version Log")
    st.caption("TODO: Đọc từ `artifacts/version_log.csv`")
    _render_version_log_table(version_log)

    st.markdown("---")

    # ── Per-run detail ────────────────────────────────────────
    st.markdown("### 🔍 Run Details")
    run_options = {r["run_file"].split("/")[-1]: r for r in runs}
    selected_run_key = st.selectbox("Chọn run", list(run_options.keys()), key="selected_run")
    selected_run = run_options[selected_run_key]

    _render_run_summary(selected_run)
    _render_case_table(selected_run)


def _render_progression_chart(runs: list[dict]) -> None:
    """Render line chart hiển thị metric qua các version."""
    try:
        import pandas as pd  # type: ignore
        import altair as alt  # type: ignore

        rows = []
        for run in runs:
            version = run.get("version", "?")
            summary = run.get("summary", {})
            for metric_key, metric_label in METRIC_LABELS.items():
                val = summary.get(metric_key)
                if val is not None:
                    rows.append({
                        "Version": version,
                        "Metric": metric_label,
                        "Value": round(val * 100, 1),
                    })

        if not rows:
            st.caption("Không có metric data")
            return

        df = pd.DataFrame(rows)
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Version:N", sort=None),
                y=alt.Y("Value:Q", scale=alt.Scale(domain=[0, 100]), title="Score (%)"),
                color="Metric:N",
                tooltip=["Version", "Metric", "Value"],
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)

    except ImportError:
        # Fallback nếu altair chưa cài
        st.caption("Cài `altair` để xem chart: `pip install altair`")
        _render_metrics_table_fallback(runs)


def _render_metrics_table_fallback(runs: list[dict]) -> None:
    """Fallback: hiển thị table nếu không có altair."""
    try:
        import pandas as pd  # type: ignore
        rows = []
        for run in runs:
            row = {"Version": run.get("version", "?")}
            for key, label in METRIC_LABELS.items():
                val = run.get("summary", {}).get(key)
                row[label] = f"{val:.0%}" if val is not None else "N/A"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    except ImportError:
        for run in runs:
            st.json(run.get("summary", {}))


def _render_version_log_table(version_log: list[dict]) -> None:
    """Render bảng version log."""
    if not version_log:
        st.caption("Chưa có entry trong version_log.csv")
        return

    try:
        import pandas as pd  # type: ignore
        df = pd.DataFrame(version_log)
        display_cols = ["version", "changed_artifact", "hypothesis", "metric_name", "metric_before", "metric_after"]
        existing_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[existing_cols], hide_index=True, use_container_width=True)
    except ImportError:
        for entry in version_log:
            st.write(entry)


def _render_run_summary(run: dict) -> None:
    """Render summary metrics cho 1 run."""
    summary = run.get("summary", {})

    st.markdown(f"**Run:** `{run.get('run_file', '?')}` | Version: `{run.get('version', '?')}` | Suite: `{run.get('suite', '?')}`")

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("case_accuracy", "Case Accuracy", col1),
        ("tool_routing_accuracy", "Routing Accuracy", col2),
        ("argument_accuracy", "Arg Accuracy", col3),
        ("multiturn_accuracy", "Multi-turn Accuracy", col4),
    ]
    for key, label, col in metrics:
        val = summary.get(key)
        with col:
            st.metric(label, f"{val:.0%}" if val is not None else "N/A")

    # Validity checks
    measured = summary.get("measured_cases", 0)
    total = summary.get("total_cases", 0)
    errors = summary.get("provider_error_cases", 0)

    validity_ok = (errors == 0) and (measured == total)
    validity_msg = (
        f"✅ Valid: {measured}/{total} cases measured, {errors} provider errors"
        if validity_ok
        else f"⚠️ Invalid: {measured}/{total} measured, {errors} provider errors"
    )
    if validity_ok:
        st.success(validity_msg)
    else:
        st.warning(validity_msg)


def _render_case_table(run: dict) -> None:
    """Render per-case result table."""
    results = run.get("results", [])

    if not results:
        st.caption("Không có per-case data trong run này (TODO: đọc từ run JSON đầy đủ)")
        return

    st.markdown("**Per-case Results:**")

    try:
        import pandas as pd  # type: ignore
        rows = []
        for r in results:
            rows.append({
                "Case ID": r.get("case_id", "?"),
                "Query": r.get("query", "?")[:40] + "...",
                "Expected": r.get("expected_tool", "?"),
                "Actual": r.get("actual_tool", "?"),
                "Pass": "✅" if r.get("passed") else "❌",
                "Failures": "; ".join(r.get("failures", [])) or "—",
            })
        df = pd.DataFrame(rows)
        st.dataframe(
            df.style.apply(
                lambda row: ["background-color: rgba(0,210,106,0.1)" if row["Pass"] == "✅" else "background-color: rgba(255,75,75,0.1)"] * len(row),
                axis=1
            ),
            hide_index=True,
            use_container_width=True,
        )
    except ImportError:
        for r in results:
            status = "✅" if r.get("passed") else "❌"
            st.markdown(f"{status} **{r.get('case_id')}**: expected `{r.get('expected_tool')}`, got `{r.get('actual_tool')}`")

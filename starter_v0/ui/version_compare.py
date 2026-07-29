"""
version_compare.py — Tab Version Compare: so sánh 2 transcript side-by-side.
Mục tiêu: thấy rõ cải thiện routing/behavior qua các version.
"""

from __future__ import annotations
import streamlit as st
from typing import Any


def render_version_compare_tab() -> None:
    """
    Render tab Version Compare.

    TODO: Thay mock bằng đọc thật từ filesystem:
        - Transcripts: glob("transcripts/*.transcript.json")
        - Runs: glob("runs/*.json") để lấy summary metrics
    """
    from .mock_data import get_mock_transcripts, get_mock_run_logs

    transcripts = get_mock_transcripts()
    runs = get_mock_run_logs()

    st.markdown("## 🔁 Version Compare")
    st.caption("So sánh 2 version side-by-side để thấy cải thiện rõ ràng")

    if len(transcripts) < 2:
        st.info("Cần ít nhất 2 transcript để so sánh. Hãy chạy thêm turns ở tab Chat.")
        return

    # ── Chọn 2 transcript ─────────────────────────────────────
    options = {
        f"[{t['version']}] {t['transcript_id']}": t
        for t in transcripts
    }
    option_keys = list(options.keys())

    col_left, col_arrow, col_right = st.columns([5, 1, 5])
    with col_left:
        left_key = st.selectbox("Version A (baseline)", option_keys, index=0, key="compare_left")
    with col_arrow:
        st.markdown("<div style='text-align:center;font-size:2rem;padding-top:1.5rem'>⟹</div>", unsafe_allow_html=True)
    with col_right:
        right_key = st.selectbox("Version B (improved)", option_keys, index=min(1, len(option_keys)-1), key="compare_right")

    left_t = options[left_key]
    right_t = options[right_key]

    st.markdown("---")

    # ── Metrics comparison ────────────────────────────────────
    st.markdown("### 📊 Metrics Comparison")
    st.caption("TODO: Lấy metrics thật từ `runs/*.json` tương ứng với mỗi transcript version")

    _render_metrics_comparison(runs, left_t["version"], right_t["version"])

    st.markdown("---")

    # ── Side-by-side transcript ───────────────────────────────
    st.markdown("### 💬 Same Query, Different Responses")
    st.caption("So sánh behavior của agent trên cùng một câu hỏi")

    _render_side_by_side(left_t, right_t)

    st.markdown("---")

    # ── Tool call diff ────────────────────────────────────────
    st.markdown("### 🔧 Tool Call Differences")
    _render_tool_diff(left_t, right_t)


def _render_metrics_comparison(runs: list[dict], v_left: str, v_right: str) -> None:
    """Render metrics so sánh giữa 2 version từ run logs."""
    run_map = {r["version"]: r for r in runs}
    left_run = run_map.get(v_left)
    right_run = run_map.get(v_right)

    metrics = [
        ("case_accuracy", "Case Accuracy"),
        ("tool_routing_accuracy", "Routing Accuracy"),
        ("argument_accuracy", "Arg Accuracy"),
        ("multiturn_accuracy", "Multi-turn Accuracy"),
    ]

    cols = st.columns(len(metrics))
    for i, (key, label) in enumerate(metrics):
        with cols[i]:
            left_val = left_run["summary"].get(key, 0) if left_run else None
            right_val = right_run["summary"].get(key, 0) if right_run else None

            if left_val is not None and right_val is not None:
                delta = right_val - left_val
                delta_str = f"{delta:+.0%}"
                st.metric(
                    label,
                    f"{right_val:.0%}" if right_run else "N/A",
                    delta=delta_str,
                    delta_color="normal" if delta >= 0 else "inverse",
                    help=f"TODO: Lấy từ runs/{v_right}_base.json"
                )
            else:
                st.metric(label, "N/A", help=f"Chưa có run cho version {v_right}")


def _render_side_by_side(left_t: dict, right_t: dict) -> None:
    """Render side-by-side so sánh turns cùng query."""
    left_turns = left_t.get("turns", [])
    right_turns = right_t.get("turns", [])

    if not left_turns or not right_turns:
        st.info("Cần ít nhất 1 turn trong mỗi transcript.")
        return

    # Ghép theo turn_index
    max_turns = max(len(left_turns), len(right_turns))
    for i in range(min(max_turns, 3)):  # Hiển thị tối đa 3 turn
        left_turn = left_turns[i] if i < len(left_turns) else None
        right_turn = right_turns[i] if i < len(right_turns) else None

        user_query = (left_turn or right_turn or {}).get("user", "N/A")

        with st.expander(f"Turn {i+1}: {user_query[:50]}...", expanded=(i == 0)):
            col_l, col_r = st.columns(2)

            with col_l:
                st.markdown(f"**[{left_t['version']}] {left_t['artifact_version'][:20]}...**")
                if left_turn:
                    _render_compact_turn(left_turn, "left")
                else:
                    st.caption("Không có turn này")

            with col_r:
                st.markdown(f"**[{right_t['version']}] {right_t['artifact_version'][:20]}...**")
                if right_turn:
                    _render_compact_turn(right_turn, "right")
                else:
                    st.caption("Không có turn này")


def _render_compact_turn(turn: dict, side: str) -> None:
    """Render compact view của 1 turn để so sánh."""
    rounds = turn.get("rounds", [])
    all_tools = []
    for r in rounds:
        for call in r.get("tool_calls", []):
            all_tools.append(call.get("name", "?"))

    if all_tools:
        tools_str = " → ".join(f"`{t}`" for t in all_tools)
        st.markdown(f"🔧 **Tools:** {tools_str}")
    else:
        st.markdown("🔧 **Tools:** (none)")

    status = turn.get("status", "answered")
    status_badge = {"answered": "✅", "waiting_for_user": "⏳", "max_tool_rounds": "⚠️"}.get(status, "❓")
    st.markdown(f"{status_badge} **Status:** `{status}`")

    assistant_text = turn.get("assistant_text", "")
    st.markdown("**Response:**")
    st.markdown(assistant_text[:200] + ("..." if len(assistant_text) > 200 else ""))


def _render_tool_diff(left_t: dict, right_t: dict) -> None:
    """Render bảng diff tool calls giữa 2 version."""
    import pandas as pd  # type: ignore

    left_calls = _collect_tool_calls(left_t)
    right_calls = _collect_tool_calls(right_t)

    all_queries = set(left_calls.keys()) | set(right_calls.keys())

    rows = []
    for query in sorted(all_queries):
        l_tools = " → ".join(left_calls.get(query, ["—"]))
        r_tools = " → ".join(right_calls.get(query, ["—"]))
        changed = "🔄 Changed" if l_tools != r_tools else "✅ Same"
        rows.append({
            "Query": query[:40] + "...",
            f"[{left_t['version']}] Tools": l_tools,
            f"[{right_t['version']}] Tools": r_tools,
            "Diff": changed,
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption("Không có data để so sánh")


def _collect_tool_calls(transcript: dict) -> dict[str, list[str]]:
    """Gom tool calls theo query từ transcript."""
    result = {}
    for turn in transcript.get("turns", []):
        query = turn.get("user", "")[:40]
        tools = []
        for r in turn.get("rounds", []):
            for call in r.get("tool_calls", []):
                tools.append(call.get("name", "?"))
        result[query] = tools
    return result

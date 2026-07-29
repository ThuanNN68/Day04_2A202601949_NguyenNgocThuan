"""
tool_trace.py — Component hiển thị tool trace sau mỗi turn của agent.
Hiển thị: tên tool, args, round index, status (ok/error), result.
"""

from __future__ import annotations
import json
import streamlit as st
from typing import Any


TOOL_ICONS = {
    "timeline": "📅",
    "social_search": "🔍",
    "lookup": "🌐",
    "fetch": "📄",
    "format": "✍️",
    "clarify": "❓",
    "send": "📨",
    "policy": "📋",
    "papers": "📚",
    "paper_text": "📑",
}

STATUS_COLOR = {
    "ok": "#00d26a",
    "error": "#ff4b4b",
    "waiting": "#ffa62b",
}


def _get_tool_status(result: dict[str, Any]) -> tuple[str, str]:
    """Xác định status của tool call từ result."""
    if isinstance(result, dict) and "error" in result:
        return "error", result.get("message", result["error"])
    if isinstance(result, dict) and result.get("awaiting_user"):
        return "waiting", "Chờ user xác nhận"
    return "ok", ""


def render_tool_badge(tool_name: str, status: str) -> str:
    color = STATUS_COLOR.get(status, "#888")
    icon = TOOL_ICONS.get(tool_name, "🔧")
    return f"""
    <span class="tool-badge" style="border-color:{color}">
        {icon} <strong>{tool_name}</strong>
        <span class="tool-status-dot" style="background:{color}"></span>
    </span>
    """


def render_tool_trace(rounds: list[dict[str, Any]], expanded: bool = True) -> None:
    """
    Render toàn bộ tool trace theo từng round.

    Args:
        rounds: list của round records từ run_model_tool_loop output
        expanded: có expand expander mặc định không

    Schema rounds:
        [
            {
                "round": int,
                "assistant_text": str,
                "tool_calls": [{"name": str, "args": dict}],
                "tool_results": [{"tool": str, "args": dict, "result": dict}]
            }
        ]
    """
    if not rounds:
        st.caption("Không có tool call nào trong turn này.")
        return

    total_calls = sum(len(r.get("tool_calls", [])) for r in rounds)
    label = f"🔧 Tool Trace — {len(rounds)} round(s), {total_calls} call(s)"

    with st.expander(label, expanded=expanded):
        for round_rec in rounds:
            round_num = round_rec.get("round", "?")
            tool_calls = round_rec.get("tool_calls", [])
            tool_results = round_rec.get("tool_results", [])

            # Round header
            st.markdown(
                f'<div class="round-header">⟳ Round {round_num}</div>',
                unsafe_allow_html=True,
            )

            if round_rec.get("assistant_text"):
                st.markdown(
                    f'<div class="round-thinking">💭 {round_rec["assistant_text"]}</div>',
                    unsafe_allow_html=True,
                )

            if not tool_calls:
                st.caption("Không có tool call")
                continue

            # Build result lookup by tool name
            result_map: dict[str, Any] = {}
            for r in tool_results:
                result_map[r.get("tool", "")] = r.get("result", {})

            for call in tool_calls:
                tool_name = call.get("name", "unknown")
                args = call.get("args", {})
                result = result_map.get(tool_name, {})
                status, err_msg = _get_tool_status(result)

                _render_single_call(
                    tool_name=tool_name,
                    args=args,
                    result=result,
                    status=status,
                    err_msg=err_msg,
                    round_num=round_num,
                )

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


def _render_single_call(
    tool_name: str,
    args: dict,
    result: Any,
    status: str,
    err_msg: str,
    round_num: int,
) -> None:
    """Render một tool call duy nhất với args và result."""
    icon = TOOL_ICONS.get(tool_name, "🔧")
    color = STATUS_COLOR.get(status, "#888")
    status_label = {"ok": "✅ OK", "error": "❌ ERROR", "waiting": "⏳ WAITING"}.get(status, status)

    st.markdown(
        f"""
        <div class="tool-call-card" style="border-left:3px solid {color}">
            <div class="tool-call-header">
                <span class="tool-name">{icon} <code>{tool_name}</code></span>
                <span class="tool-status" style="color:{color}">{status_label}</span>
                <span class="tool-round">Round {round_num}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_args, col_result = st.columns(2)

    with col_args:
        st.markdown("**Args**")
        st.code(
            json.dumps(args, ensure_ascii=False, indent=2) if args else "{}",
            language="json",
        )

    with col_result:
        st.markdown("**Result**")
        if status == "error":
            st.error(f"Error: {err_msg}")
            st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")
        elif status == "waiting":
            st.warning(f"⏳ {err_msg}")
        else:
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if len(result_str) > 500:
                result_str = result_str[:500] + "\n... (truncated)"
            st.code(result_str, language="json")

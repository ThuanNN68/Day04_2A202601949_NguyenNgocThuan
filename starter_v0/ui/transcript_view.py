"""
transcript_view.py — Tab Transcripts: browser xem transcript đã lưu.
Hiển thị: artifact_version, provider, model, turn-by-turn log với tool trace.
"""

from __future__ import annotations
import json
import streamlit as st
from typing import Any
from .tool_trace import render_tool_trace


def render_transcript_tab() -> None:
    """
    Render tab Transcripts.
    """
    from pathlib import Path
    
    ROOT = Path(__file__).parent.parent
    transcripts_dir = ROOT / "transcripts"
    
    transcripts = []
    if transcripts_dir.exists():
        for p in sorted(transcripts_dir.glob("*.transcript.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                transcripts.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                pass

    st.markdown("## 📋 Transcript Browser")
    st.caption("Xem lại các phiên chat đã được lưu từ thư mục `transcripts/` ")

    if not transcripts:
        st.info("Chưa có transcript nào. Hãy chat trước ở tab Chat.")
        return

    # ── Chọn transcript ───────────────────────────────────────
    transcript_options = {
        f"[{t['version']}] {t['transcript_id']} — {t.get('created_at', '')}": t
        for t in transcripts
    }
    selected_key = st.selectbox(
        "Chọn transcript",
        list(transcript_options.keys()),
        key="selected_transcript",
    )
    selected = transcript_options[selected_key]

    st.markdown("---")

    # ── Metadata ──────────────────────────────────────────────
    _render_transcript_metadata(selected)

    st.markdown("---")

    # ── Turns ─────────────────────────────────────────────────
    turns = selected.get("turns", [])
    st.markdown(f"### 🔄 Turns ({len(turns)} total)")

    for turn in turns:
        _render_turn(turn)


def _render_transcript_metadata(t: dict[str, Any]) -> None:
    """Render metadata card cho transcript."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Version", t.get("version", "—"))
    with col2:
        st.metric("Provider", t.get("provider", "—"))
    with col3:
        st.metric("Turns", len(t.get("turns", [])))
    with col4:
        total_tools = sum(
            len(turn.get("tool_events", []))
            for turn in t.get("turns", [])
        )
        st.metric("Total Tool Calls", total_tools)

    st.markdown(
        f"""
        <div class="metadata-card">
            <div class="meta-row">
                <span class="meta-label">artifact_version</span>
                <code class="meta-value">{t.get('artifact_version', '—')}</code>
            </div>
            <div class="meta-row">
                <span class="meta-label">prompt_hash</span>
                <code class="meta-value">{t.get('prompt_hash', '—')[:16]}...</code>
            </div>
            <div class="meta-row">
                <span class="meta-label">tools_hash</span>
                <code class="meta-value">{t.get('tools_hash', '—')[:16]}...</code>
            </div>
            <div class="meta-row">
                <span class="meta-label">model</span>
                <code class="meta-value">{t.get('model', '—')}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_turn(turn: dict[str, Any]) -> None:
    """Render một turn trong transcript."""
    turn_idx = turn.get("turn_index", "?")
    status = turn.get("status", "answered")
    started = turn.get("started_at", "")
    ended = turn.get("ended_at", "")

    status_emoji = {"answered": "✅", "waiting_for_user": "⏳", "max_tool_rounds": "⚠️", "provider_error": "❌"}.get(status, "❓")

    with st.expander(
        f"{status_emoji} Turn {turn_idx}: {turn.get('user', '')[:60]}...",
        expanded=(turn_idx == 1),
    ):
        # User query
        st.markdown("**👤 User**")
        st.markdown(f"> {turn.get('user', '')}")

        # Tool trace
        rounds = turn.get("rounds", [])
        if rounds:
            render_tool_trace(rounds, expanded=False)

        # Agent response
        st.markdown("**🤖 Agent**")
        assistant_text = turn.get("assistant_text", "")
        if status == "waiting_for_user":
            st.warning(f"⏳ {assistant_text}")
        elif status == "provider_error":
            st.error(f"❌ {turn.get('error', assistant_text)}")
        else:
            st.markdown(assistant_text)

        # Timing
        if started and ended:
            st.caption(f"⏱️ {started} → {ended}")

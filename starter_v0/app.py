"""
app.py — Entrypoint Streamlit cho Research Agent UI.

Chạy:
    streamlit run app.py

PASS khi mở được http://localhost:8501

Architecture:
    app.py
    └── ui/
        ├── sidebar.py          → config panel (provider, version, params)
        ├── chat_view.py        → tab Chat (với tool trace)
        ├── tool_trace.py       → component tool trace
        ├── transcript_view.py  → tab Transcripts
        ├── version_compare.py  → tab Version Compare
        ├── run_logs.py         → tab Run Logs
        ├── mock_data.py        → MOCK data (thay bằng logic thật khi ready)
        └── styles.css          → custom dark theme

Tích hợp logic thật:
    - Tìm mọi comment "TODO:" trong các file ui/*.py
    - Mock data nằm trong ui/mock_data.py
    - Điểm tích hợp chính: ui/chat_view.py:_call_agent()
"""

from __future__ import annotations
from pathlib import Path

import streamlit as st

# ── Page config (PHẢI gọi đầu tiên) ──────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent — Tool Eval Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
CSS_PATH = Path(__file__).parent / "ui" / "styles.css"
if CSS_PATH.exists():
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ── Import UI components ──────────────────────────────────────────────────────
from ui.sidebar import render_sidebar
from ui.chat_view import render_chat_tab
from ui.transcript_view import render_transcript_tab
from ui.version_compare import render_version_compare_tab
from ui.run_logs import render_run_logs_tab

# ── App header ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🔬 Research <span>Agent</span> — Tool Eval Lab</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar → config ──────────────────────────────────────────────────────────
config = render_sidebar()

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab_chat, tab_transcripts, tab_compare, tab_runs = st.tabs([
    "💬 Chat",
    "📋 Transcripts",
    "🔁 Version Compare",
    "📊 Run Logs",
])

with tab_chat:
    render_chat_tab(config)

with tab_transcripts:
    render_transcript_tab()

with tab_compare:
    render_version_compare_tab()

with tab_runs:
    render_run_logs_tab()

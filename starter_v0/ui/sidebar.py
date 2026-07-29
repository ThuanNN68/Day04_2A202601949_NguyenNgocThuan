"""
sidebar.py — Sidebar config panel: chọn provider, version, model, parameters.
Trả về config dict dùng chung cho toàn app.
"""

from __future__ import annotations
import streamlit as st
from pathlib import Path


PROVIDERS = ["openrouter", "openai", "anthropic", "gemini"]
VERSIONS = ["v0", "v1", "v2", "v3"]


def render_sidebar() -> dict:
    """
    Render sidebar và trả về config dict.

    TODO (khi tích hợp logic):
    - Đọc danh sách version thật từ artifacts/version_log.csv
    - Validate API key có trong .env không
    - Load system_prompt và tools.yaml thật
    """
    with st.sidebar:
        # Header
        st.markdown(
            """
            <div class="sidebar-header">
                <div class="sidebar-logo">🔬</div>
                <div>
                    <div class="sidebar-title">Research Agent</div>
                    <div class="sidebar-subtitle">Tool Eval Lab</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Provider ─────────────────────────────────────────
        st.markdown("**⚙️ Provider Config**")

        provider = st.selectbox(
            "Provider",
            PROVIDERS,
            index=0,
            help="LLM provider để gọi agent",
            key="sb_provider",
        )

        # TODO: Load model list thật từ provider SDK
        model_placeholder = st.text_input(
            "Model (để trống = default)",
            value="",
            placeholder="e.g. anthropic/claude-3.5-sonnet",
            help="TODO: Lấy danh sách model từ provider",
            key="sb_model",
        )
        model = model_placeholder.strip() or None

        st.divider()

        # ── Artifact Version ──────────────────────────────────
        st.markdown("**📦 Artifact Version**")

        version = st.selectbox(
            "Version label",
            VERSIONS,
            index=0,
            help="Version prompt/tool đang dùng",
            key="sb_version",
        )

        # TODO: Đọc system_prompt.md thật và hiển thị preview
        with st.expander("📄 System Prompt Preview", expanded=False):
            # TODO: Thay bằng Path("artifacts/system_prompt.md").read_text()
            st.code(
                "# [MOCK] System Prompt\n\nBạn là Research Agent...\n\n"
                "TODO: Load từ artifacts/system_prompt.md",
                language="markdown",
            )

        # TODO: Đọc tools.yaml thật
        with st.expander("🔧 Tools Preview", expanded=False):
            st.code(
                "# [MOCK] Tools YAML\n\ntools:\n  - name: clarify\n  - name: timeline\n  ...\n\n"
                "TODO: Load từ artifacts/tools.yaml",
                language="yaml",
            )

        st.divider()

        # ── Agent Parameters ──────────────────────────────────
        st.markdown("**🎛️ Agent Parameters**")

        max_tool_rounds = st.slider(
            "Max Tool Rounds",
            min_value=1,
            max_value=8,
            value=4,
            help="Số lượt tool call tối đa mỗi turn",
            key="sb_max_rounds",
        )

        history_window = st.slider(
            "History Window",
            min_value=0,
            max_value=10,
            value=5,
            help="Số lượt chat giữ trong context",
            key="sb_history",
        )

        st.divider()

        # ── Status ────────────────────────────────────────────
        st.markdown("**📊 Session Status**")

        # TODO: Đọc số transcript / run thật từ filesystem
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Transcripts", "2", help="TODO: đếm từ transcripts/")
        with col2:
            st.metric("Runs", "3", help="TODO: đếm từ runs/")

        # Artifact version badge
        # TODO: Tính artifact_version thật từ versioning.build_artifact_version()
        mock_av = f"{version}+pMOCK1234+tMOCK5678"
        st.markdown(
            f"""
            <div class="version-badge">
                <span class="version-label">artifact_version</span>
                <code class="version-code">{mock_av}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("⚠️ MOCK mode — chưa kết nối logic thật")

    return {
        "provider": provider,
        "model": model,
        "version": version,
        "max_tool_rounds": max_tool_rounds,
        "history_window": history_window,
        # TODO: Thêm artifact_version thật khi tích hợp versioning.py
        "artifact_version": mock_av,
    }

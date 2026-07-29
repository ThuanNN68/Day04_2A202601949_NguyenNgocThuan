"""
chat_view.py — Tab Chat: giao diện chat với agent, hiển thị tool trace.
"""

from __future__ import annotations
import streamlit as st
from typing import Any
from .tool_trace import render_tool_trace


def _init_chat_state() -> None:
    """Khởi tạo session state cho chat."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "turn_history" not in st.session_state:
        # Lưu lịch sử turn kèm tool trace để render lại
        st.session_state.turn_history = []


def _render_message_bubble(role: str, content: str) -> None:
    """Render bubble chat với styling khác nhau cho user/agent."""
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-bubble user-bubble">
                <div class="bubble-avatar">👤</div>
                <div class="bubble-content">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-bubble agent-bubble">
                <div class="bubble-avatar">🤖</div>
                <div class="bubble-content">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_chat_tab(config: dict) -> None:
    """
    Render tab Chat hoàn chỉnh.

    Args:
        config: dict từ sidebar.render_sidebar()
                {"provider", "model", "version", "max_tool_rounds", "history_window", "artifact_version"}
    """
    _init_chat_state()

    # ── Header ────────────────────────────────────────────────
    col_title, col_info = st.columns([3, 1])
    with col_title:
        st.markdown("## 💬 Chat with Agent")
    with col_info:
        st.markdown(
            f"""
            <div class="chat-info-badge">
                <div>🏷️ <code>{config['artifact_version']}</code></div>
                <div>🔌 {config['provider']} | 📦 {config['version']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Chat history ──────────────────────────────────────────
    chat_container = st.container()

    with chat_container:
        if not st.session_state.turn_history:
            st.markdown(
                """
                <div class="empty-chat">
                    <div class="empty-icon">🔬</div>
                    <div class="empty-text">Bắt đầu chat với Research Agent</div>
                    <div class="empty-hint">Thử: "Tìm timeline @elonmusk" hoặc "Tìm paper về AI safety"</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for turn in st.session_state.turn_history:
                # User message
                _render_message_bubble("user", turn["user"])

                # Tool trace (nếu có)
                if turn.get("rounds"):
                    render_tool_trace(turn["rounds"], expanded=False)

                # Agent response
                status = turn.get("status", "answered")
                assistant_text = turn.get("assistant_text", "")

                if status == "waiting_for_user":
                    st.warning(f"⏳ **Agent cần xác nhận:** {assistant_text}")
                elif status == "max_tool_rounds":
                    st.error(f"⚠️ {assistant_text}")
                else:
                    _render_message_bubble("assistant", assistant_text)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Input area ────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])

    with col_input:
        user_input = st.chat_input(
            placeholder="Nhập câu hỏi... (VD: Tìm timeline @username, Tìm paper về GPT-5)",
            key="chat_input",
        )

    # ── Quick examples ────────────────────────────────────────
    st.markdown("**💡 Thử nhanh:**")
    example_cols = st.columns(4)
    examples = [
        ("📅 Timeline", "Tìm timeline @elonmusk"),
        ("📚 Papers", "Tìm paper về AI safety"),
        ("🌐 Web search", "Tin tức mới nhất về GPT-5"),
        ("📨 Telegram", "Gửi summary lên Telegram"),
    ]
    triggered_example = None
    for i, (label, query) in enumerate(examples):
        with example_cols[i]:
            if st.button(label, key=f"example_{i}", use_container_width=True):
                triggered_example = query

    # Dùng example nếu click
    query_to_run = triggered_example or user_input

    # ── Run agent ─────────────────────────────────────────────
    if query_to_run:
        with st.spinner("🤔 Agent đang xử lý..."):
            result = _call_agent(query_to_run, config)

        # Lưu vào history
        turn_record = {
            "user": query_to_run,
            **result,
        }
        st.session_state.turn_history.append(turn_record)
        st.rerun()

    # ── Clear button ──────────────────────────────────────────
    if st.session_state.turn_history:
        if st.button("🗑️ Xoá lịch sử chat", key="clear_chat"):
            st.session_state.turn_history = []
            st.rerun()


def _call_agent(user_input: str, config: dict) -> dict[str, Any]:
    """
    Gọi agent và trả về kết quả.

    TODO: Thay mock bằng logic thật:
        1. Khởi tạo provider từ config["provider"]
        2. Load system_prompt và tools từ artifacts/
        3. Gọi run_model_tool_loop() từ chat.py
        4. Lưu transcript vào transcripts/
        5. Return result dict

    Ví dụ tích hợp:
        from env_loader import load_lab_env
        from providers import make_provider
        from tools import load_tool_declarations, to_openai_tools
        from chat import run_model_tool_loop, trim_history, write_transcript
        from versioning import build_artifact_version
        from pathlib import Path

        ROOT = Path(__file__).parent.parent
        load_lab_env(ROOT)

        provider = make_provider(config["provider"])
        tool_declarations = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
        openai_tools = to_openai_tools(tool_declarations)
        system_prompt = (ROOT / "artifacts" / "system_prompt.md").read_text()

        history = st.session_state.get("chat_raw_history", [])
        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(history, config["history_window"]),
            {"role": "user", "content": user_input},
        ]

        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=openai_tools,
            model=config["model"],
            max_tool_rounds=config["max_tool_rounds"],
        )

        # Update history
        st.session_state.chat_raw_history = history + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": result["assistant_text"]},
        ]

        # TODO: write_transcript(transcript_path, transcript)

        return result
    """
    from .mock_data import get_mock_agent_response
    return get_mock_agent_response(user_input)

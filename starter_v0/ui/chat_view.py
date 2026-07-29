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
    st.markdown("**💡 Thử nhanh kịch bản A4:**")
    
    import json
    from pathlib import Path
    scenarios_json_path = Path(__file__).parent.parent / "artifacts" / "demo_scenarios.json"
    
    scenarios = []
    if scenarios_json_path.exists():
        try:
            with open(scenarios_json_path, "r", encoding="utf-8") as f:
                scenarios = json.load(f)
        except Exception:
            pass

    triggered_example = None

    if not scenarios:
        # Fallback if file doesn't exist or is invalid
        examples = [
            ("📰 Tin tức AI", "Tin tức AI hôm nay"),
            ("📚 Tìm Paper", "bạn giúp tôi tìm paper về cách làm 1 AI agent được kohong"),
            ("📝 Đọc Paper", "bạn có thể gửi cho tôi nội dung của bài báo Meaningful human control không"),
            ("⏳ Hỏi lại (Clarify)", "Tóm tắt bài viết này"),
        ]
        example_cols = st.columns(len(examples))
        for i, (label, query) in enumerate(examples):
            with example_cols[i]:
                if st.button(label, key=f"example_{i}", use_container_width=True):
                    triggered_example = query
    else:
        # Render group by scenarios
        for s_idx, scenario in enumerate(scenarios):
            st.markdown(f"**{scenario.get('scenario_name', f'Kịch bản {s_idx+1}')}**")
            turns = scenario.get("turns", [])
            cols = st.columns(len(turns)) if turns else []
            for t_idx, turn in enumerate(turns):
                with cols[t_idx]:
                    if st.button(turn["label"], key=f"btn_{s_idx}_{t_idx}", use_container_width=True):
                        triggered_example = turn["query"]

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
    Gọi agent và thực thi loop thật, sau đó ghi transcript JSON chuẩn tương tự chat.py
    """
    from env_loader import load_lab_env
    from providers import make_provider
    from tools import load_tool_declarations, to_openai_tools
    from chat import run_model_tool_loop, trim_history, write_transcript, safe_slug, now_iso
    from versioning import build_artifact_version, artifact_version_dict
    from pathlib import Path
    from datetime import datetime

    ROOT = Path(__file__).parent.parent
    load_lab_env(ROOT)

    # 1. Khởi tạo provider & model
    provider = make_provider(config["provider"])
    selected_model = config["model"] or getattr(provider, "default_model", None)

    # 2. Đọc file prompt & tools hiện tại để build artifact version (và hash prompt/tool)
    system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
    tools_path = ROOT / "artifacts" / "tools.yaml"

    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    
    # Chỉ giữ lại 3 tool được yêu cầu: papers, paper_review, paper_compare
    allowed_tool_names = {"papers", "paper_review", "paper_compare"}
    filtered_declarations = [td for td in tool_declarations if td["name"] in allowed_tool_names]
    openai_tools = to_openai_tools(filtered_declarations)
    
    artifact_version = build_artifact_version(config["version"], system_prompt_path, tools_path)

    # 3. Chuẩn bị message history
    if "chat_raw_history" not in st.session_state:
        st.session_state.chat_raw_history = []
    
    history = st.session_state.chat_raw_history
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(history, config["history_window"]),
        {"role": "user", "content": user_input},
    ]

    # 4. Chạy loop gọi LLM và chạy tool thật
    result = run_model_tool_loop(
        provider=provider,
        messages=messages,
        tools=openai_tools,
        model=selected_model,
        max_tool_rounds=config["max_tool_rounds"],
    )

    # 5. Lưu lại lịch sử chat thô phục vụ context turn sau
    st.session_state.chat_raw_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": result["assistant_text"]},
    ]

    # 6. Khởi tạo hoặc cập nhật file Transcript JSON trong phiên chat này
    transcripts_dir = ROOT / "transcripts"
    if "current_transcript_path" not in st.session_state:
        # Nếu là turn đầu tiên, khởi tạo file transcript mới
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        transcript_id = "_".join([
            safe_slug(config["version"]),
            safe_slug(config["provider"]),
            timestamp,
        ])
        transcript_path = transcripts_dir / f"{transcript_id}.transcript.json"
        
        st.session_state.current_transcript_path = str(transcript_path)
        st.session_state.current_transcript_data = {
            "transcript_id": transcript_id,
            **artifact_version_dict(artifact_version),
            "provider": config["provider"],
            "model": selected_model,
            "system_prompt": str(system_prompt_path),
            "tools": str(tools_path),
            "history_window": config["history_window"],
            "max_tool_rounds": config["max_tool_rounds"],
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        }
        st.session_state.current_turn_index = 0

    # Tăng chỉ số lượt chat
    st.session_state.current_turn_index += 1
    
    # Ghi nhận thông tin lượt chat này
    turn_record = {
        "turn_index": st.session_state.current_turn_index,
        "started_at": now_iso(),
        "user": user_input,
        "ended_at": now_iso(),
        "status": result.get("status", "answered"),
        "assistant_text": result.get("assistant_text", ""),
        "rounds": result.get("rounds", []),
        "tool_events": result.get("tool_events", []),
    }
    
    # Append turn và write ra disk
    st.session_state.current_transcript_data["turns"].append(turn_record)
    write_transcript(
        Path(st.session_state.current_transcript_path), 
        st.session_state.current_transcript_data
    )

    return result

"""
mock_data.py — Mock data dùng để phát triển UI trước khi tích hợp logic thật.
Mỗi hàm trả về dữ liệu giả lập đúng schema thật để UI render được ngay.

Khi tích hợp logic thật:
- Xoá / comment out hàm mock
- Thay bằng lời gọi hàm thật từ chat.py, run_eval.py, versioning.py, v.v.
"""

from __future__ import annotations
from typing import Any


# ---------------------------------------------------------------------------
# MOCK: Transcript (output của chat.py)
# ---------------------------------------------------------------------------

def get_mock_transcripts() -> list[dict[str, Any]]:
    """
    TODO: Thay bằng code đọc thật từ thư mục `transcripts/`.
    Ví dụ:
        transcripts_dir = Path("transcripts")
        return [json.loads(p.read_text()) for p in transcripts_dir.glob("*.transcript.json")]
    """
    return [
        {
            "transcript_id": "v0_openrouter_20260729T090000",
            "version": "v0",
            "artifact_version": "v0+p3a4b5c6d7e8f+t1a2b3c4d5e6f",
            "prompt_hash": "3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b",
            "tools_hash": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
            "provider": "openrouter",
            "model": "anthropic/claude-3.5-sonnet",
            "created_at": "2026-07-29T09:00:00",
            "updated_at": "2026-07-29T09:15:00",
            "turns": [
                {
                    "turn_index": 1,
                    "user": "Tìm các bài viết gần đây của @elonmusk về AI",
                    "status": "answered",
                    "assistant_text": "Tôi đã tìm thấy 5 bài đăng gần đây của @elonmusk về AI. Dưới đây là digest tổng hợp:\n\n**AI Safety (2 bài)**: Elon đề cập đến rủi ro của AGI và kêu gọi regulations...\n\n**xAI & Grok (3 bài)**: Cập nhật về Grok 3, benchmark mới...",
                    "started_at": "2026-07-29T09:01:00",
                    "ended_at": "2026-07-29T09:02:30",
                    "rounds": [
                        {
                            "round": 1,
                            "assistant_text": "Tôi sẽ tìm timeline của @elonmusk trước.",
                            "tool_calls": [{"name": "timeline", "args": {"username": "elonmusk", "max_results": 10}}],
                            "tool_results": [
                                {
                                    "tool": "timeline",
                                    "args": {"username": "elonmusk", "max_results": 10},
                                    "result": {
                                        "tweets": [
                                            {"id": "1001", "text": "AI is the most transformative technology of our time.", "created_at": "2026-07-28"},
                                            {"id": "1002", "text": "Grok 3 is now 10x better at coding tasks.", "created_at": "2026-07-27"},
                                            {"id": "1003", "text": "We need international cooperation on AI safety.", "created_at": "2026-07-26"},
                                        ]
                                    }
                                }
                            ]
                        },
                        {
                            "round": 2,
                            "assistant_text": "Đã có data, giờ tôi sẽ format thành digest.",
                            "tool_calls": [{"name": "format", "args": {"items": ["tweet1", "tweet2"], "style": "digest"}}],
                            "tool_results": [
                                {
                                    "tool": "format",
                                    "args": {"items": ["tweet1", "tweet2"], "style": "digest"},
                                    "result": {"markdown": "## Digest\n\n- AI Safety post...\n- Grok 3 update..."}
                                }
                            ]
                        }
                    ],
                    "tool_events": [
                        {
                            "tool": "timeline",
                            "args": {"username": "elonmusk", "max_results": 10},
                            "result": {"tweets": [{"id": "1001", "text": "AI is transformative"}]}
                        },
                        {
                            "tool": "format",
                            "args": {"items": ["tweet1"], "style": "digest"},
                            "result": {"markdown": "## Digest\n\n- AI Safety..."}
                        }
                    ]
                },
                {
                    "turn_index": 2,
                    "user": "Tìm thêm về xAI trên web",
                    "status": "answered",
                    "assistant_text": "Đây là các thông tin mới nhất về xAI từ web...",
                    "started_at": "2026-07-29T09:05:00",
                    "ended_at": "2026-07-29T09:06:00",
                    "rounds": [
                        {
                            "round": 1,
                            "assistant_text": "Tôi sẽ search web về xAI.",
                            "tool_calls": [{"name": "lookup", "args": {"query": "xAI company latest news 2026"}}],
                            "tool_results": [
                                {
                                    "tool": "lookup",
                                    "args": {"query": "xAI company latest news 2026"},
                                    "result": {
                                        "results": [
                                            {"title": "xAI raises $6B Series B", "url": "https://example.com/1", "snippet": "Elon Musk's xAI..."},
                                            {"title": "Grok 3 released", "url": "https://example.com/2", "snippet": "New benchmark results..."},
                                        ]
                                    }
                                }
                            ]
                        }
                    ],
                    "tool_events": [
                        {
                            "tool": "lookup",
                            "args": {"query": "xAI company latest news 2026"},
                            "result": {"results": [{"title": "xAI news", "url": "https://example.com"}]}
                        }
                    ]
                }
            ]
        },
        {
            "transcript_id": "v1_openrouter_20260729T100000",
            "version": "v1",
            "artifact_version": "v1+pAABBCCDDEEFF+t112233445566",
            "prompt_hash": "AABBCCDDEEFF001122334455667788990011223344556677889900AABBCCDDEEFF00",
            "tools_hash": "112233445566778899001122334455667788990011223344556677889900112233",
            "provider": "openrouter",
            "model": "anthropic/claude-3.5-sonnet",
            "created_at": "2026-07-29T10:00:00",
            "updated_at": "2026-07-29T10:10:00",
            "turns": [
                {
                    "turn_index": 1,
                    "user": "Tìm các bài viết gần đây của @elonmusk về AI",
                    "status": "answered",
                    "assistant_text": "**Cải thiện v1**: Agent giờ gọi đúng `social_search` kết hợp `timeline` thay vì chỉ dùng timeline một mình.\n\nTổng hợp 8 bài đăng liên quan đến AI từ nhiều nguồn...",
                    "started_at": "2026-07-29T10:01:00",
                    "ended_at": "2026-07-29T10:02:00",
                    "rounds": [
                        {
                            "round": 1,
                            "assistant_text": "Tôi sẽ dùng cả timeline và social_search để có kết quả đầy đủ hơn.",
                            "tool_calls": [
                                {"name": "timeline", "args": {"username": "elonmusk", "max_results": 10}},
                                {"name": "social_search", "args": {"query": "elonmusk AI", "max_results": 5}}
                            ],
                            "tool_results": [
                                {
                                    "tool": "timeline",
                                    "args": {"username": "elonmusk", "max_results": 10},
                                    "result": {"tweets": [{"id": "2001", "text": "AGI is closer than you think"}]}
                                },
                                {
                                    "tool": "social_search",
                                    "args": {"query": "elonmusk AI", "max_results": 5},
                                    "result": {"results": [{"text": "xAI breakthrough in reasoning"}]}
                                }
                            ]
                        }
                    ],
                    "tool_events": []
                }
            ]
        }
    ]


# ---------------------------------------------------------------------------
# MOCK: Run JSON (output của run_eval.py)
# ---------------------------------------------------------------------------

def get_mock_run_logs() -> list[dict[str, Any]]:
    """
    TODO: Thay bằng code đọc thật từ thư mục `runs/`.
    Ví dụ:
        runs_dir = Path("runs")
        return [json.loads(p.read_text()) for p in runs_dir.glob("*.json")]
    """
    return [
        {
            "run_file": "runs/v0_base_20260729T090000.json",
            "version": "v0",
            "suite": "base",
            "artifact_version": "v0+p3a4b5c6d7e8f+t1a2b3c4d5e6f",
            "provider": "openrouter",
            "created_at": "2026-07-29T09:00:00",
            "summary": {
                "case_accuracy": 0.60,
                "tool_routing_accuracy": 0.65,
                "argument_accuracy": 0.70,
                "multiturn_accuracy": 0.50,
                "measured_cases": 10,
                "total_cases": 10,
                "provider_error_cases": 0,
            },
            "results": [
                {"case_id": "base_01", "query": "Tìm timeline @elonmusk", "expected_tool": "timeline", "actual_tool": "timeline", "passed": True, "failures": []},
                {"case_id": "base_02", "query": "Tìm paper AI safety", "expected_tool": "papers", "actual_tool": "lookup", "passed": False, "failures": ["wrong_tool: used lookup instead of papers"]},
                {"case_id": "base_03", "query": "Gửi message Telegram", "expected_tool": "clarify", "actual_tool": "send", "passed": False, "failures": ["missing boundary check"]},
                {"case_id": "base_04", "query": "Search bài về GPT-5", "expected_tool": "social_search", "actual_tool": "social_search", "passed": True, "failures": []},
                {"case_id": "base_05", "query": "Đọc nội dung URL này", "expected_tool": "fetch", "actual_tool": "fetch", "passed": True, "failures": []},
            ]
        },
        {
            "run_file": "runs/v1_base_20260729T101500.json",
            "version": "v1",
            "suite": "base",
            "artifact_version": "v1+pAABBCCDDEEFF+t112233445566",
            "provider": "openrouter",
            "created_at": "2026-07-29T10:15:00",
            "summary": {
                "case_accuracy": 0.75,
                "tool_routing_accuracy": 0.80,
                "argument_accuracy": 0.78,
                "multiturn_accuracy": 0.70,
                "measured_cases": 10,
                "total_cases": 10,
                "provider_error_cases": 0,
            },
            "results": [
                {"case_id": "base_01", "query": "Tìm timeline @elonmusk", "expected_tool": "timeline", "actual_tool": "timeline", "passed": True, "failures": []},
                {"case_id": "base_02", "query": "Tìm paper AI safety", "expected_tool": "papers", "actual_tool": "papers", "passed": True, "failures": []},
                {"case_id": "base_03", "query": "Gửi message Telegram", "expected_tool": "clarify", "actual_tool": "clarify", "passed": True, "failures": []},
                {"case_id": "base_04", "query": "Search bài về GPT-5", "expected_tool": "social_search", "actual_tool": "social_search", "passed": True, "failures": []},
                {"case_id": "base_05", "query": "Đọc nội dung URL này", "expected_tool": "fetch", "actual_tool": "lookup", "passed": False, "failures": ["wrong_tool: used lookup instead of fetch"]},
            ]
        },
        {
            "run_file": "runs/v2_base_20260729T111500.json",
            "version": "v2",
            "suite": "base",
            "artifact_version": "v2+p998877665544+t334455667788",
            "provider": "openrouter",
            "created_at": "2026-07-29T11:15:00",
            "summary": {
                "case_accuracy": 0.85,
                "tool_routing_accuracy": 0.90,
                "argument_accuracy": 0.85,
                "multiturn_accuracy": 0.80,
                "measured_cases": 10,
                "total_cases": 10,
                "provider_error_cases": 0,
            },
            "results": []
        }
    ]


# ---------------------------------------------------------------------------
# MOCK: Version log CSV (output của artifacts/version_log.csv)
# ---------------------------------------------------------------------------

def get_mock_version_log() -> list[dict[str, Any]]:
    """
    TODO: Thay bằng code đọc thật từ `artifacts/version_log.csv`.
    Ví dụ:
        import csv
        with open("artifacts/version_log.csv") as f:
            return list(csv.DictReader(f))
    """
    return [
        {
            "version": "v0",
            "author": "team",
            "changed_artifact": "baseline",
            "artifact_version": "v0+p3a4b5c6d7e8f+t1a2b3c4d5e6f",
            "hypothesis": "Baseline — chưa tối ưu",
            "metric_name": "tool_routing_accuracy",
            "metric_before": "",
            "metric_after": "0.65",
            "run_file": "runs/v0_base.json",
        },
        {
            "version": "v1",
            "author": "team",
            "changed_artifact": "system_prompt.md",
            "artifact_version": "v1+pAABBCCDDEEFF+t112233445566",
            "hypothesis": "Thêm ví dụ cụ thể cho tool `papers` để model không nhầm với `lookup`",
            "metric_name": "tool_routing_accuracy",
            "metric_before": "0.65",
            "metric_after": "0.80",
            "run_file": "runs/v1_base.json",
        },
        {
            "version": "v2",
            "author": "team",
            "changed_artifact": "tools.yaml",
            "artifact_version": "v2+p998877665544+t334455667788",
            "hypothesis": "Cải thiện mô tả tool `clarify` để agent hỏi lại trước khi gửi Telegram",
            "metric_name": "tool_routing_accuracy",
            "metric_before": "0.80",
            "metric_after": "0.90",
            "run_file": "runs/v2_base.json",
        },
    ]


# ---------------------------------------------------------------------------
# MOCK: Kết quả chạy agent (output của chat.py run_model_tool_loop)
# ---------------------------------------------------------------------------

def get_mock_agent_response(user_input: str) -> dict[str, Any]:
    """
    TODO: Thay bằng lời gọi thật tới run_model_tool_loop() từ chat.py.
    Ví dụ:
        from chat import run_model_tool_loop
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=openai_tools,
            model=model,
            max_tool_rounds=max_tool_rounds,
        )
        return result

    Schema trả về:
        {
            "status": "answered" | "waiting_for_user" | "max_tool_rounds",
            "assistant_text": str,
            "rounds": [ { "round": int, "assistant_text": str, "tool_calls": [...], "tool_results": [...] } ],
            "tool_events": [ { "tool": str, "args": dict, "result": dict } ]
        }
    """
    import time
    time.sleep(0.5)  # Giả lập latency

    # Simulate dựa trên keyword trong input
    query_lower = user_input.lower()

    if "telegram" in query_lower or "gửi" in query_lower:
        return {
            "status": "waiting_for_user",
            "assistant_text": "⚠️ Bạn có chắc muốn gửi message lên Telegram không? Đây là hành động nhạy cảm. (yes/no)",
            "rounds": [
                {
                    "round": 1,
                    "assistant_text": "Phát hiện hành động nhạy cảm, cần xác nhận.",
                    "tool_calls": [{"name": "clarify", "args": {"question": "Bạn có chắc muốn gửi?", "response_type": "yes_no"}}],
                    "tool_results": [{"tool": "clarify", "args": {}, "result": {"awaiting_user": True, "question": "Bạn có chắc?"}}]
                }
            ],
            "tool_events": [{"tool": "clarify", "args": {"question": "Bạn có chắc?"}, "result": {"awaiting_user": True}}]
        }

    if "timeline" in query_lower or "@" in query_lower:
        username = "elonmusk"
        for word in user_input.split():
            if word.startswith("@"):
                username = word[1:]
        return {
            "status": "answered",
            "assistant_text": f"Đây là 3 bài đăng gần nhất của @{username}:\n\n1. **AI is the most transformative technology** (2026-07-28)\n2. **Grok 4 is coming soon** (2026-07-27)\n3. **xAI partnership with Tesla** (2026-07-26)",
            "rounds": [
                {
                    "round": 1,
                    "assistant_text": f"Lấy timeline của @{username}.",
                    "tool_calls": [{"name": "timeline", "args": {"username": username, "max_results": 5}}],
                    "tool_results": [{"tool": "timeline", "args": {"username": username, "max_results": 5}, "result": {"tweets": [{"id": "1", "text": "AI is transformative"}]}}]
                },
                {
                    "round": 2,
                    "assistant_text": "Format digest.",
                    "tool_calls": [{"name": "format", "args": {"items": ["tweet1"], "style": "digest"}}],
                    "tool_results": [{"tool": "format", "args": {}, "result": {"markdown": "## Digest\n..."}}]
                }
            ],
            "tool_events": [
                {"tool": "timeline", "args": {"username": username, "max_results": 5}, "result": {"tweets": []}},
                {"tool": "format", "args": {}, "result": {"markdown": "## Digest"}}
            ]
        }

    if "paper" in query_lower or "arxiv" in query_lower or "research" in query_lower:
        return {
            "status": "answered",
            "assistant_text": "Tìm thấy 3 paper liên quan:\n\n1. **Attention Is All You Need** (Vaswani et al.)\n2. **GPT-4 Technical Report** (OpenAI)\n3. **Constitutional AI** (Anthropic)",
            "rounds": [
                {
                    "round": 1,
                    "assistant_text": "Tìm paper trên arXiv.",
                    "tool_calls": [{"name": "papers", "args": {"query": user_input, "max_results": 3}}],
                    "tool_results": [{"tool": "papers", "args": {"query": user_input}, "result": {"papers": [{"title": "Attention Is All You Need"}]}}]
                }
            ],
            "tool_events": [{"tool": "papers", "args": {"query": user_input}, "result": {"papers": []}}]
        }

    # Default: web search
    return {
        "status": "answered",
        "assistant_text": f"Đây là kết quả tìm kiếm về '{user_input}':\n\n- **Kết quả 1**: Thông tin chi tiết về chủ đề...\n- **Kết quả 2**: Bài viết liên quan...\n- **Nguồn**: example.com",
        "rounds": [
            {
                "round": 1,
                "assistant_text": "Tìm kiếm web.",
                "tool_calls": [{"name": "lookup", "args": {"query": user_input}}],
                "tool_results": [{"tool": "lookup", "args": {"query": user_input}, "result": {"results": [{"title": "Result 1", "url": "https://example.com"}]}}]
            }
        ],
        "tool_events": [{"tool": "lookup", "args": {"query": user_input}, "result": {"results": []}}]
    }

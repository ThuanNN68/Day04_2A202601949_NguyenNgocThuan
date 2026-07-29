# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
>
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 11:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: B07
- Members: Phạm Đức Thiện, Nguyễn Ngọc Thuận, Trần Công Chiến, Phạm Khắc Duy

| Mã sinh viên | Họ và Tên       | Role                                                                               |
| -------------- | ------------------ | ---------------------------------------------------------------------------------- |
|                | Trần Công Chiến | Leader, Nhiệm vụ xác định bài toán, điều phối team, xây dựng phần UI. |
|                |                    |                                                                                    |

- Provider/model:

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Agent đóng vai trò như một trợ lý nghiên cứu thông minh, có khả năng phân tích yêu cầu của người dùng để tự động tìm kiếm và thu thập các bài báo khoa học liên quan trên mạng. Bên cạnh đó, agent hỗ trợ đọc hiểu, tóm tắt nội dung cốt lõi và đánh giá chất lượng của các nghiên cứu một cách chi tiết và chính xác.

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL và tổng hợp thành digest."

**Link dùng thử (truy cập được trong showdown):**

> Dán public URL nếu người khác cần mở từ máy riêng; localhost cũng được nếu demo trực tiếp trên máy trình chiếu. Streamlit được khuyến nghị, nhưng nhóm có thể dùng bất kỳ framework nào.
>
> URL:

## A2. Tool agent có

> Liệt kê các tool agent đang dùng. Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì                              | Tool mới nhóm thêm? |
| --------- | --------------------------------------------- | ---------------------- |
| clarify   | hỏi lại người dùng khi thiếu thông tin | không                 |
|           |                                               |                        |
|           |                                               |                        |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm giúp tôi 5 bài báo khoa học mới nhất về ứng dụng của **Retrieval-Augmented Generation (RAG)** trong y tế và tóm tắt ngắn gọn đóng góp chính của từng bài.
2. Đọc bài báo [Link/Tên bài báo] và phân tích chi tiết: phương pháp nghiên cứu, tập dữ liệu sử dụng, kết quả đạt được và các hạn chế còn tồn tại.
3. Đánh giá chất lượng và độ tin cậy của bài báo [Link/Tên bài báo] dựa trên tính mới của đề tài, độ chặt chẽ của phương pháp thực nghiệm và uy tín của nơi xuất bản.
4. So sánh ưu/nhược điểm giữa 3 bài báo nổi bật nhất về chủ đề **LLM Quantization** và gợi ý nghiên cứu phù hợp nhất cho bài toán triển khai trên thiết bị di động.

## A4. Kịch bản demo đã rehearse

> Chuẩn bị 3–5 scenario. Mỗi scenario cần cho thấy tool đã làm gì và một thay đổi cụ thể giữa các version.

| Scenario                                                                                                                                                                                                                                                                                                                                                  | Tool trace cần thấy                                                                                                                                                                                           | Câu chuyện cải thiện version                                                                                                                                                                                                                                                                                     | Fallback run/transcript                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Kịch bản 1: Tìm & Đọc nội dung bài báo**- **Turn 1**: "Tìm 5 bài báo arXiv mới nhất liên quan đến RAG evaluation."- **Turn 2**: "Đọc nội dung của bài báo arXiv:1706.03762 trang đầu tiên."                                                                                                                  | -**Turn 1**: `papers(query="RAG evaluation", max_results=5)`- **Turn 2**: `paper_text(arxiv_url="1706.03762", max_pages=1)`                                                                     | **v0**: Dễ gọi nhầm `lookup` thay vì `papers` cho arXiv.**v1**: Gọi đúng `papers` trên arXiv, trích xuất chính xác ID và dùng `paper_text` để đọc trang đầu tiên.                                                                                                           | `transcripts/v0_openai_20260729T141853422535.transcript.json` |
| **Kịch bản 2: Đánh giá chuyên sâu (Tool: paper_review)**- **Turn 1**: "Tải text của bài báo arXiv:1706.03762 để tôi phân tích."- **Turn 2**: "Hãy chạy công cụ đánh giá chi tiết (paper_review) phần Phương pháp (methodology) của bài báo này."                                                        | -**Turn 1**: `paper_text(arxiv_url="1706.03762")`- **Turn 2**: `paper_review(text="...", focus="methodology")`                                                                                  | **v0**: Model tóm tắt chung chung bằng cách tự suy diễn hoặc gọi nhầm `fetch` cho file pdf nội bộ.**v1**: Gọi đúng `paper_review` với tham số `focus="methodology"` để trích xuất cấu trúc thực tế.                                                                        | `transcripts/v0_openai_20260729T142213051827.transcript.json` |
| **Kịch bản 3: So sánh side-by-side (Tool: paper_compare)**- **Turn 1**: "Hãy tải nội dung văn bản của bài báo arXiv:1706.03762."- **Turn 2**: "Hãy tải thêm nội dung văn bản của bài báo arXiv:2212.08073."- **Turn 3**: "So sánh 2 bài báo này dựa trên các tiêu chí: methodology và limitations." | -**Turn 1**: `paper_text(arxiv_url="1706.03762")`- **Turn 2**: `paper_text(arxiv_url="2212.08073")`- **Turn 3**: `paper_compare(papers=[...], criteria=["methodology", "limitations"])` | **v0**: Model không thể so sánh vì thiếu text của 2 paper (gây lỗi ValueError do gọi tool song song mà chưa tải text).**v1**: Ghi nhớ lịch sử hội thoại, tự động chuyển đổi metadata và gọi `paper_compare` để vẽ bảng Markdown so sánh side-by-side từ text đã lưu. | `runs/v0_openai_20260729T143225726028.transcript.json`        |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Prompt/tool change                                                                                                                                                                                                                                          | Hypothesis                                                                                                               | Metric name   | Before | After | Run File                                             |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------- | -----: | ----: | ---------------------------------------------------- |
| v0      | baseline                                                                                                                                                                                                                                                    | Baseline initial setup                                                                                                   | case_accuracy |   0.00 |  0.90 | `runs/v0_B_base_openai_20260729T100558112616.json` |
| v1      | Thêm Section 6 Guardrails vào`system_prompt.md`; siết rule Parallel Execution (chỉ gọi cả 2 khi user nói rõ cả 2 nguồn); thêm Query keyword rule (extract keyword ngắn, bỏ filler); mô tả `tools.yaml` chi tiết hơn với routing hints | Siết rule sẽ fix R03 (model tự gọi thêm`social_search`) và R13 (query bị dịch sang tiếng Việt) → đạt 100% | case_accuracy |   0.90 |  1.00 | `runs/v0_B_base_openai_20260729T122405629969.json` |
| v2      |                                                                                                                                                                                                                                                             |                                                                                                                          |               |        |       |                                                      |
| v3      |                                                                                                                                                                                                                                                             |                                                                                                                          |               |        |       |                                                      |

## B2. Failure analysis

Use actual failures from `results[*].result.failures`.

| Case ID                     | Failure Type                     | Actual Tool Calls                    | What Failed                                                                                                                                 | Fix                                                                                                                                          |
| --------------------------- | -------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| R03_web_news_routing        | wrong_tool (`extra_tool_call`) | `lookup` ✅ + `social_search` ❌ | User chỉ hỏi tin web (`"Tin tức AI hôm nay"`), model tự ý gọi thêm `social_search` vì cho rằng "nổi bật" = cần Twitter     | Siết rule Parallel Execution: chỉ gọi cả 2 khi user**nói rõ** cả 2 nguồn; thêm ví dụ phản ví dụ trực tiếp trong prompt |
| R13_parallel_web_and_tweets | wrong_tool (`wrong_arg_value`) | `lookup(query="tin tức AI")` ❌   | Model dịch câu user sang tiếng Việt đầy đủ thay vì extract keyword ngắn gọn: expected`query="AI"`, got `query="tin tức AI"` | Thêm**Query keyword rule**: luôn extract keyword tiếng Anh ngắn nhất, bỏ filler words như "tin tức", "hôm nay", "mới nhất"  |

## B3. Team eval cases

List the 10 cases added to `data/eval_group.json`:

- 5 single-turn
- 5 multi-turn

This section is for the mandatory team-authored eval set. Optional built-ins do
not belong here.

File template để trống có chủ đích; nhóm phải tự thiết kế đủ 10 case.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
| ------- | ------------- | ---------------------- | ------ |
|         |               |                        |        |

## B4. Live chat evidence

Use `transcripts/*.transcript.json`.

| Scenario/Turn                                                                                                                                                                                                                                                                                                                                     | Version | Tool Calls + Args                                                                                                                                                                                               | Transcript/Run                                                  | Outcome                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Kịch bản 1: Tìm & Đọc paper (Multi-turn):**- **Turn 1**: "bạn giúp tôi tìm paper về cách làm 1 AI agent được kohong"- **Turn 2**: "bạn có thể gửi cho tôi nội dung của bài báo Meaningful human control không"                                                                                       | v0      | -**Turn 1**: `papers(query="AI agent", max_results=5)` - **Turn 2**: `paper_text(arxiv_url="http://arxiv.org/abs/2112.01298v2")`                                                                | `transcripts/v3_openai_20260729T141853422535.transcript.json` | -**Turn 1**: Tìm thấy và hiển thị 5 bài báo khoa học về AI Agent từ arXiv.- **Turn 2**: Dựa vào ngữ cảnh Turn 1, tải và phân tích thành công nội dung của paper "Meaningful human control". |
| **Kịch bản 2: Đánh giá chuyên sâu (Multi-turn):**- **Turn 1**: "Tải text của bài báo arXiv:1706.03762 để tôi phân tích."- **Turn 2**: "Hãy chạy công cụ đánh giá chi tiết (paper_review) phần Phương pháp (methodology) của bài báo này."                                                       | v1      | -**Turn 1**: `paper_text(arxiv_url="1706.03762")`- **Turn 2**: `paper_review(text="...", focus="methodology")`                                                                                  | `transcripts/v0_openai_20260729T142213051827.transcript.json` | -**Turn 1**: Tải thành công text thô của paper.- **Turn 2**: Phân tích và trích xuất cấu trúc Phương pháp nghiên cứu chi tiết của paper qua tool `paper_review`.                             |
| **Kịch bản 3: So sánh side-by-side (Multi-turn):**- **Turn 1**: "Hãy tải nội dung văn bản của bài báo arXiv:1706.03762."- **Turn 2**: "Hãy tải thêm nội dung văn bản của bài báo arXiv:2212.08073."- **Turn 3**: "So sánh 2 bài báo này dựa trên các tiêu chí: methodology và limitations." | v1      | -**Turn 1**: `paper_text(arxiv_url="1706.03762")`- **Turn 2**: `paper_text(arxiv_url="2212.08073")`- **Turn 3**: `paper_compare(papers=[...], criteria=["methodology", "limitations"])` | `transcripts/v3_openai_20260729T143225726028.transcript.json` | -**Turn 1 & 2**: Tải đầy đủ nội dung thô của 2 paper.- **Turn 3**: Thực thi tool `paper_compare` để vẽ bảng Markdown so sánh side-by-side của 2 paper theo đúng tiêu chí.                    |

## B5. Tool capability evidence

Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng.

UI is core deliverable, not bonus. Do not list it here.

| Category                         | Evidence File | What Worked | Risk / Guardrail |
| -------------------------------- | ------------- | ----------- | ---------------- |
| Must-have: tool mới đầu tiên |               |             |                  |
| Optional built-in                |               |             |                  |
| Bonus: tool mới thứ 4 trở đi |               |             |                  |

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

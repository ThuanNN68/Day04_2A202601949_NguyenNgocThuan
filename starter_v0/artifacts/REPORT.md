# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
>
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 11:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: B07
- Members: Phạm Đức Thiện, Nguyễn Ngọc Thuận, Trần Công Chiến, Phạm Khắc Duy

| Mã sinh viên | Họ và Tên         | Role                                                                               |
| -------------- | -------------------- | ---------------------------------------------------------------------------------- |
| 2A202601053    | Trần Công Chiến   | Leader, Nhiệm vụ xác định bài toán, điều phối team, xây dựng phần UI. |
| 2A202601981    | Phạm Đức Thiện   | Viết system prompt, report                                                        |
| 2A202601757    | Phạm Khắc Duy      | viết test_eval                                                                    |
| 2A202601949    | Nguyễn Ngọc Thuận | viết tool                                                                         |

- Provider/model: openai

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

| Tên tool     | Làm được gì                                                                                      | Tool mới nhóm thêm? |
| ------------- | ----------------------------------------------------------------------------------------------------- | ---------------------- |
| clarify       | Hỏi lại người dùng khi thiếu thông tin hoặc yêu cầu chưa rõ ràng                         | Không                 |
| timeline      | Lấy các bài đăng gần đây từ một tài khoản Twitter/X cụ thể theo @handle (qua RapidAPI)  | Không                 |
| social_search | Tìm kiếm bài đăng theo từ khóa/hashtag trên Twitter/X                                         | Không                 |
| lookup        | Tìm kiếm thông tin trên web qua Tavily (hỗ trợ lọc tin tức, general, theo khoảng thời gian) | Không                 |
| fetch         | Đọc toàn bộ nội dung của một URL cụ thể qua Firecrawl                                        | Không                 |
| format        | Định dạng danh sách nội dung đã thu thập thành bản digest/newsletter markdown               | Không                 |
| send          | Gửi tin nhắn văn bản đến kênh Telegram (cần xác nhận người dùng trước khi gửi)        | Không                 |
| policy        | Tìm kiếm tài liệu chính sách nội bộ công ty theo chủ đề                                   | Không                 |
| papers        | Tìm kiếm bài báo khoa học/preprint trên arXiv theo từ khóa                                    | Không                 |
| paper_text    | Tải PDF bài báo arXiv và trích xuất toàn bộ nội dung text để đọc/phân tích             | Không                 |
| paper_review  | Phân tích và đánh giá bài báo từ text thô (Abstract, Methodology, Results, Limitations)     | Có                    |
| paper_compare | So sánh side-by-side từ 2–10 bài báo theo các tiêu chí: methodology, results, limitations…   | Có                    |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm giúp tôi 5 bài báo khoa học mới nhất về ứng dụng của **Retrieval-Augmented Generation (RAG)** trong y tế và tóm tắt ngắn gọn đóng góp chính của từng bài.
2. Đọc bài báo [Link/Tên bài báo] và phân tích chi tiết: phương pháp nghiên cứu, tập dữ liệu sử dụng, kết quả đạt được và các hạn chế còn tồn tại.
3. Đánh giá chất lượng và độ tin cậy của bài báo [Link/Tên bài báo] dựa trên tính mới của đề tài, độ chặt chẽ của phương pháp thực nghiệm và uy tín của nơi xuất bản.
4. So sánh ưu/nhược điểm giữa 3 bài báo nổi bật nhất về chủ đề **LLM Quantization** và gợi ý nghiên cứu phù hợp nhất cho bài toán triển khai trên thiết bị di động.

## A4. Kịch bản demo đã rehearse

> Chuẩn bị 3–5 scenario. Mỗi scenario cần cho thấy tool đã làm gì và một thay đổi cụ thể giữa các version.

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
| -------- | --------------------- | -------------------------------- | ----------------------- |
|          |                       |                                  |                         |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Prompt/tool change                                                                                                                                                                                                                                          | Hypothesis                                                                                                                                    | Metric name   | Before | After | Run File                                             |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -----: | ----: | ---------------------------------------------------- |
| v0      | baseline                                                                                                                                                                                                                                                    | Baseline initial setup                                                                                                                        | case_accuracy |   0.00 |  0.90 | `runs/v0_B_base_openai_20260729T100558112616.json` |
| v1      | Thêm Section 6 Guardrails vào`system_prompt.md`; siết rule Parallel Execution (chỉ gọi cả 2 khi user nói rõ cả 2 nguồn); thêm Query keyword rule (extract keyword ngắn, bỏ filler); mô tả `tools.yaml` chi tiết hơn với routing hints | Siết rule sẽ fix R03 (model tự gọi thêm`social_search`) và R13 (query bị dịch sang tiếng Việt) → đạt 100%                      | case_accuracy |   0.90 |  1.00 | `runs/v_B_base_openai_20260729T122405629969.json`  |
| v2      | Thêm tool bonus`paper_review` và `paper_compare` vào `tools.yaml`; bổ sung routing rules cho 2 tool mới trong `system_prompt.md` (`papers` → `paper_text` → `paper_review` → `paper_compare`)                                       | Thêm tool mới sẽ mở rộng khả năng research pipeline nhưng có thể gây`extra_tool_call` ở M06 khi model chọn sai tool            | case_accuracy |   1.00 |  0.95 | `runs/v2_B_base_openai_20260729T124652257529.json` |
| v3      | Thêm quy tắc**Source Switching & Persistence (STRICT)** trong `system_prompt.md` và bổ sung điều kiện loại trừ nguồn cũ trong `tools.yaml` (`social_search` & `lookup`)                                                            | Khắc phục triệt để lỗi`extra_tool_call` ở test case M06 khi chuyển đổi nguồn trong hội thoại multi-turn → đạt 100% accuracy | case_accuracy |   0.95 |  1.00 | `v3_B_base_openai_20260729T125130073083.json`      |

## B2. Failure analysis

Use actual failures from `results[*].result.failures`.

| Case ID                     | Failure Type                     | Actual Tool Calls                    | What Failed                                                                                                                                 | Fix                                                                                                                                          |
| --------------------------- | -------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| R03_web_news_routing        | wrong_tool (`extra_tool_call`) | `lookup` ✅ + `social_search` ❌ | User chỉ hỏi tin web (`"Tin tức AI hôm nay"`), model tự ý gọi thêm `social_search` vì cho rằng "nổi bật" = cần Twitter     | Siết rule Parallel Execution: chỉ gọi cả 2 khi user**nói rõ** cả 2 nguồn; thêm ví dụ phản ví dụ trực tiếp trong prompt |
| R13_parallel_web_and_tweets | wrong_tool (`wrong_arg_value`) | `lookup(query="tin tức AI")` ❌   | Model dịch câu user sang tiếng Việt đầy đủ thay vì extract keyword ngắn gọn: expected`query="AI"`, got `query="tin tức AI"` | Thêm**Query keyword rule**: luôn extract keyword tiếng Anh ngắn nhất, bỏ filler words như "tin tức", "hôm nay", "mới nhất"  |
| M06_switch_tool             | wrong_tool (`extra_tool_call`) | `lookup` ✅ + `social_search` ❌ | Sau khi user nói "Bỏ Twitter, chuyển sang tìm web", ở turn 3 ("Giữ chủ đề OpenAI") model gọi thừa`social_search`               | Thêm quy tắc**Source Switching & Persistence (STRICT)** trong `system_prompt.md` và `tools.yaml`                                |

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

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
| ------------- | ------- | ----------------- | -------------- | ------- |
|               |         |                   |                |         |

## B5. Tool capability evidence

Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng.

UI is core deliverable, not bonus. Do not list it here.

| Category                         | Evidence File                   | What Worked                                                                                                                                                                      | Risk / Guardrail                                                                                                                                                              |
| -------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Must-have: tool mới đầu tiên | `tools/paper_review/tool.py`  | Trích xuất tự động các phần chính (Abstract, Methodology, Results, Limitations) từ văn bản bài báo để tạo evidence card chuẩn hóa không cần gọi LLM ngoài. | Chỉ trích xuất từ văn bản được cung cấp, không tự suy diễn hoặc bịa đặt thông tin không có trong bài báo; trả về quality_flags nếu thiếu dữ liệu. |
| Optional built-in                | `tools/paper_compare/tool.py` | So sánh side-by-side từ 2–10 bài báo dựa trên các tiêu chí (methodology, evaluation, results, limitations) để tổng hợp bảng đối sánh.                          | Không tự tìm kiếm hay tính toán xếp hạng khoa học; hiển thị minh bạch các tiêu chí bị thiếu dữ liệu ở từng bài báo.                                    |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  - *Parallel Execution Rule*: Siết chặt điều kiện gọi song song `lookup` và `social_search`, chỉ cho phép gọi cả hai khi người dùng yêu cầu rõ ràng cả 2 nguồn trong cùng một tin nhắn (khắc phục lỗi `extra_tool_call` ở R03).
  - *Query Keyword Rule*: Hướng dẫn trích xuất từ khóa ngắn gọn bằng tiếng Anh, loại bỏ filler words như "tin tức", "hôm nay", "mới nhất" (khắc phục lỗi `wrong_arg_value` ở R13).
  - *Source Switching & Persistence (STRICT)*: Quy định khi người dùng chuyển nguồn (ví dụ: "Bỏ Twitter, chuyển sang tìm web"), nguồn cũ phải duy trì trạng thái vô hiệu hóa ở tất cả các lượt sau (khắc phục lỗi M06).
  - *Security Guardrails*: Thêm quy định chống prompt injection, từ chối câu ngoài scope (toán tích phân, viết code Fibonacci) và ngăn tiết lộ danh sách tool nội bộ.

- **Which fixes belonged in `tools.yaml`?**
  - *Chi tiết hóa Description & Routing Hints*: Bổ sung ngữ cảnh sử dụng cho từng tool (ví dụ: `lookup` dùng cho tin web chung, không dùng cho bài báo khoa học hay URL trực tiếp).
  - *Điều kiện loại trừ bổ trợ*: Thêm ràng buộc trực tiếp trong `description` của `social_search` và `lookup` để cấm kết hợp ngầm trừ khi có yêu cầu đồng thời ở lượt hiện tại.

- **Which failure needed manual review instead of automatic grading?**
  - *Các trường hợp thiếu API Key*: Các test case như R01–R07 trả về `RuntimeError` (do thiếu `RAPIDAPI_KEY` / `TAVILY_API_KEY`) nhưng eval tự động vẫn chấm PASS vì chỉ so sánh `tool_calls` và `args`. Cần review thủ công `tool_results` để xác nhận execution thực sự thành công.
  - *Câu phản hồi từ chối / Meta (R08, R09, R14)*: Eval tự động chỉ kiểm tra `no_tool: true`, cần người review đọc `actual_text` để đảm bảo câu trả lời lịch sự, đúng định hướng và không bịa đặt.

- **What would you improve next?**
  - Cấu hình đầy đủ environment variables để kiểm thử toàn bộ luồng live API thực tế.
  - Cải thiện `paper_text` và `paper_review` bằng mô hình RAG / trích xuất ngữ nghĩa nâng cao hơn thay vì trích xuất regex thô từ PDF.
  - Xây dựng bộ test cases phong phú hơn cho `data/eval_group.json` tập trung vào luồng bài báo khoa học (`papers` → `paper_text` → `paper_review` → `paper_compare`).

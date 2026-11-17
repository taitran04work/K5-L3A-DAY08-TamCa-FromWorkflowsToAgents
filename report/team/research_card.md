# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Kim, Liu et al. (Google Research, Google DeepMind, MIT), *Towards a Science of Scaling Agent Systems*, arXiv 2512.08296 v3 (2026), https://arxiv.org/abs/2512.08296. Loại: benchmark có kiểm soát (single, independent, centralized, decentralized, hybrid; cùng tool và token budget) |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Với task suy luận tuần tự, mọi biến thể multi-agent đều làm hiệu năng giảm so với single agent; điều phối tập trung chỉ có lợi rõ trên task song song hóa được |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | LLM thật của ba họ model, trên các benchmark agentic của paper (Finance-Agent, BrowseComp-Plus, PlanCraft, WorkBench…); mô hình dự đoán chỉ giải thích khoảng một nửa phương sai. Không có task hoàn tiền, không có host chặn ghi tiền như lab này |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Claim LogiX là chuỗi tuần tự (claim → order → quote → host). Thêm một investigator (workflow → orchestrator) sẽ không tăng pass rate (giữ ở 1.000) nhưng cost/success tăng khoảng 1.5–2.5 lần do thêm model call lập kế hoạch/tổng hợp và tool call lặp |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: MockLLM, bộ tool đọc + `compute_compensation`, host `issue_refund`, seed 11/22/33/44/55, 14 claim `data/public_claims.jsonl`, `config/pricing.yaml`, evaluator `lab8.benchmark`, SQLite mới cho mỗi trial. Biến duy nhất: có hay không lớp orchestrator + investigator chỉ đọc (workflow vs orchestrator) |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: tốn chi phí điều phối mà không thêm độ đúng (coordination overhead). Đo bằng cost/success và mean tool calls; kiểm thêm pass^5 và variance để chắc không đổi độ đúng lấy độ ổn định |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,orchestrator --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_r1.json`
- Run id / file report: `src/reports/ablation_r1.json` (R-workflow-C-001-s11 … R-orchestrator-C-014-s55, 140 trial)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **Đúng**. Pass rate 1.000 → 1.000, pass^5 1.000 → 1.000, variance 0 → 0. Cost/success 28.79 → 57.58 VND (×2.00, nằm trong khoảng dự đoán 1.5–2.5). Mean tool calls 2.79 → 5.57, mean model calls 1.00 → 2.93. Thêm investigator chỉ thêm chi phí trên task tuần tự này.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. MockLLM không mắc lỗi suy luận nên ablation chỉ đo được phần overhead chi phí, không đo được hiện tượng "multi-agent làm giảm độ đúng" mà paper báo cáo. 14 claim là cỡ mẫu nhỏ.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).

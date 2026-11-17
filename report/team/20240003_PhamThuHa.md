# Báo cáo cá nhân — 20240003_PhamThuHa

## 1. Thông tin thành viên

- Họ tên: Phạm Thu Hà
- MSSV: 20240003
- Email: ha.pt@example.edu.vn
- GitHub: ptha

## 2. Phần việc phụ trách

Shape C `orchestrator` (`src/lab8/shapes/orchestrator.py`), handoff và kiểm tra trace.

## 3. Đóng góp cụ thể

- Commit `aedd1bf`: handoff dựng bằng `make_handoff` với `facts={}` và 4 tool chỉ đọc; trace ghi handoff đã sanitize, không ghi parent context.
- Test: `test_orchestrator_handoff_carries_no_parent_facts`, `test_trace_has_no_secret_or_ticket` (chạy cho cả ba shape).

## 4. Bằng chứng

- `python -m pytest -q -m student -o addopts= -k orchestrator` → 62 passed.
- `src/reports/ablation_r1.json`: orchestrator cost/success 57.58, gấp 2.00 lần workflow.

## 5. Công cụ AI đã dùng

Dùng Claude để giải thích vì sao tóm tắt bằng LLM không tính là redaction. Tự kiểm bằng cách đọc `lab8/handoff.py` (allowlist `ALLOWED_FIELDS`, `FACT_KEYS`) và viết test quét canary.

## 6. Tự đánh giá

Phần khó nhất là quyết định để `facts` rỗng: investigator tự đọc DB qua tool nên không cần mang gì từ parent sang, ít bề mặt lộ dữ liệu hơn.

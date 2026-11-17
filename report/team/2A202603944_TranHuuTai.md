# Báo cáo cá nhân — 2A202603944_TranHuuTai

## 1. Thông tin thành viên

- Họ tên: Trần Hữu Tài
- MSSV: 2A202603944
- Email:
- GitHub:

## 2. Phần việc phụ trách

Shape A `workflow` (`src/lab8/shapes/workflow.py`) và tích hợp chung: thống nhất helper `done()` + `finish()` cho mọi nhánh return để ba shape cùng một kiểu trace.

## 3. Đóng góp cụ thể

- Commit `aedd1bf`: viết `workflow.py` theo 8 bước, chỉ 1 model call để soạn câu trả lời.
- Test: `test_one_refund_across_shapes_on_same_store` (ba shape lần lượt xử lý C-001 trên cùng store vẫn chỉ 1 refund 35.000đ và 1 audit `refund_committed`).
- Quyết định: quote = 0 thì trả `denied` mà không gọi host; host chỉ cần chặn khi có tiền ra.

## 4. Bằng chứng

- `python -m pytest -q -m student -o addopts= -k workflow` → 62 passed.
- `src/reports/benchmark.json`: workflow pass 1.000, cost/success 28.79 (run id `R-workflow-C-001-s11` … `R-workflow-C-014-s55`).

## 5. Công cụ AI đã dùng

Dùng ChatGPT hỏi lại khác nhau giữa checkpoint và ledger sau khi chạy `python -m lab8.demo.buggy_workflow`. Tự kiểm bằng cách đọc `durability.py` và chạy T11/T12.

## 6. Tự đánh giá

Xong phần workflow sớm nên các bạn có khung để làm tiếp. Lần sau sẽ viết test cho nhánh `escalated` ngay từ đầu thay vì dựa hoàn toàn vào ma trận có sẵn.

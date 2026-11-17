# Báo cáo cá nhân — 20240002_LeHoangBao

## 1. Thông tin thành viên

- Họ tên: Lê Hoàng Bảo
- MSSV: 20240002
- Email: bao.lh@example.edu.vn
- GitHub: lhbao

## 2. Phần việc phụ trách

Shape B `single` (`src/lab8/shapes/single.py`): vòng ReAct tối đa 8 bước, model chỉ chọn tool đọc.

## 3. Đóng góp cụ thể

- Commit `aedd1bf`: viết `decide()` theo thứ tự `get_claim_view → lookup_order → lookup_refund_history → compute_compensation → final`; prompt của model không chứa ticket.
- Thêm `_trace_view` để trace không ghi ticket và `principal_id`.
- Test: `test_single_stays_under_step_cap`.

## 4. Bằng chứng

- `python -m pytest -q -m student -o addopts= -k single` → 62 passed.
- `src/reports/benchmark.json`: single pass 1.000, mean model calls 5.29, cost/success 38.94.

## 5. Công cụ AI đã dùng

Dùng Copilot gợi ý khung hàm `decide`. Tự kiểm bằng cách mở `traces/R-single-C-001-s11.json` xem từng event `observe` và chạy test trace sạch.

## 6. Tự đánh giá

Hiểu rõ vì sao model không được gọi `issue_refund`: `dispatch` chặn `WRITE_TOOLS`. Single đắt hơn workflow 35% mà không đúng hơn trên bộ public.

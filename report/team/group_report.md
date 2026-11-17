# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: TamCa
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): `aedd1bf`

## 2. Mục tiêu và cách tiếp cận

Bài toán: xử lý claim hoàn phí vận chuyển của LogiX-VN bằng bốn kiến trúc có cùng chữ ký `run_claim`, rồi chọn kiến trúc ít tự chủ nhất mà vẫn đúng. Điểm nhóm thống nhất ngay từ CP1: số tiền, approval và chống ghi trùng là việc của **code** (`compute_compensation` và host `durability.issue_refund`); model chỉ đọc và soạn chữ. Chữ trong ticket là dữ liệu, không phải lệnh.

Chia việc (nhóm 4 người): Anh viết workflow trước làm bản chuẩn và lo tích hợp; Bảo và Hà dựa trên luồng của workflow để viết single và orchestrator song song; Dũng chạy crash suite, benchmark và viết ADR. Thứ tự: workflow → single → orchestrator → đo cả 4 shape (swarm có sẵn).

## 3. Giải pháp

**A — workflow** (`src/lab8/shapes/workflow.py`). Bước cố định: `get_claim_view` → thiếu `order_id` thì `needs_info` → `lookup_order` (allowlist field), không thấy hoặc sai chủ thì `escalated` → `compute_compensation` từ order row → quote 0 thì `denied`, không gọi host → quote > 0 thì gọi `durability.issue_refund(conn, claim_id, quote_đầy_đủ, crash_at=crash_at)`. Host từ chối → `denied` (host đã ghi audit `policy_denied`), conflict số tiền → `failed`, thành công → `resolved`. MockLLM chỉ được gọi một lần để soạn câu trả lời.

**B — single** (`single.py`). Dùng `run_react` với `max_steps=8`. Hàm `decide` đóng vai model: mỗi bước tính một model call, chỉ được chọn tool đọc theo thứ tự `get_claim_view → lookup_order → lookup_refund_history → compute_compensation`, rồi trả `final` kèm quote. Prompt của model không chứa ticket, nên câu "ignore policy" hay số ngày trễ khai khống trong ticket không vào được quyết định. Sau vòng lặp, **code của shape** gọi host; `issue_refund` nằm trong `WRITE_TOOLS` nên dù model có chọn cũng bị `dispatch` từ chối.

**C — orchestrator** (`orchestrator.py`). Orchestrator đọc claim view, dựng handoff bằng `make_handoff` với `facts={}` và `allowed_tools=[lookup_order, lookup_policy, lookup_refund_history, compute_compensation]` (đều chỉ đọc). Investigator chạy qua `run_readonly_investigators`, trả order view và quote. Chỉ orchestrator gọi `issue_refund`.

**Vì sao truyền quote đầy đủ.** Host tự trừ phần đơn đã được hoàn bởi claim khác (T13, T14). Nếu shape tự trừ trước thì host trừ thêm lần nữa, khách bị hoàn thiếu. `lookup_refund_history` chỉ được ghi vào trace để giải thích.

**Crash.** Cả ba shape truyền `crash_at` vào host và không bắt `InjectedCrash`. Dòng ledger và audit `refund_committed` nằm chung một transaction, khóa `refund:{claim_id}`, nên chạy lại sau crash là `idempotent_replay`.

**Trace.** Dùng `lab8.trace.Trace`; mọi nhánh return đều đi qua `finish()` nên luôn có file `traces/<run_id>.json`. Event: `claim`, `order` / `investigator` / `observe`, `quote`, `handoff` (C), `react_stop` (B), `host_call`, `host_result`, `decision`. Không ghi ticket, `principal_id`, `parent_secret`, header, order row thô.

## 4. Kết quả

Bộ public: 14 claim × seed 11, 22, 33, 44, 55 = 70 trial/shape, SQLite mới cho từng trial (`src/reports/benchmark.json`).

| Shape | Pass rate | pass^5 | Seed min–max | Variance | Cost/success (VND mô phỏng) | Mean / p95 steps | Model calls TB |
| --- | ---: | ---: | --- | ---: | ---: | --- | ---: |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.79 | 5.07 / 6 | 1.00 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 38.94 | 6.93 / 8 | 5.29 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 57.58 | 6.00 / 7 | 2.93 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 | 3.00 |

- Swarm fail đúng 1 trial: C-002 seed 55, `status resolved != denied`. Ở seed chia hết cho 5, swarm tin số ngày trễ khách ghi trong ticket thay vì order row nên hoàn tiền cho claim lẽ ra bị từ chối. Ba shape của nhóm đều `denied` ở trial này (test `test_ticket_delay_is_ignored_seed55`).
- Crash safety: `20/20` (`src/reports/crash.json`).
- Ma trận student: `248 passed` (`python -m pytest -q -m student -o addopts=`); cổng host: `63 passed` (gồm 9 test nhóm thêm trong `tests/test_team_shapes.py`).
- `python -m lab8.check_submission`: 0 FAIL.
- Chưa tự kiểm trên `student_drop/` vì bộ này chưa được phát.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

- **Trace lộ ticket ở bản single đầu tiên.** Bản nháp ghi nguyên kết quả `get_claim_view` vào event `observe`, trong đó có ticket và `principal_id`. Test `test_trace_has_no_secret_or_ticket` bắt được lỗi này. Cách sửa: hàm `_trace_view` chỉ giữ `found`, `claim_id`, `order_id` cho tool đó.
- **Tự trừ tiền đã hoàn.** Một bản nháp của orchestrator trừ `refunded_vnd` trước khi gọi host, làm T13/T14 đỏ. Đọc lại docstring `durability.issue_refund` và sửa về quote đầy đủ.
- **Bắt nhầm `InjectedCrash`.** Bản đầu bọc `issue_refund` trong `try/except Exception` để luôn trả `failed`; T12 báo crash không xảy ra. Bỏ khối `except` để exception đi thẳng ra ngoài.
- **Windows.** Git cảnh báo `CRLF will be replaced by LF` với file JSON trong `src/reports/`; đây chỉ là cảnh báo, nội dung không đổi.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Pass rate 1.000 của ba shape cho thấy shape không giao quyết định cho model, chứ không chứng minh model thật sẽ cho kết quả như vậy. Bộ public chỉ có 14 claim; kết luận "workflow là đủ" có thể đổi nếu bộ hidden có claim cần đọc ticket phi cấu trúc (ví dụ mô tả hư hỏng chưa xác minh) hoặc cần tra nhiều nguồn song song. Hướng tiếp: chạy `student_drop/` khi có, đếm riêng số lần host từ chối theo lý do, và thử bonus đo single với model thật trên cùng bộ seed.

## 8. Tài liệu tham khảo

- Đề bài và contract của lab: `README.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`.
- Kim, Liu et al., *Towards a Science of Scaling Agent Systems*, arXiv 2512.08296 (2026), https://arxiv.org/abs/2512.08296.

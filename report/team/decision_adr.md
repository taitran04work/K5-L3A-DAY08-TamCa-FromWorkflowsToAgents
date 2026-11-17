# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: aedd1bf
- Run id dẫn chứng: R-workflow-C-001-s11 (src/reports/benchmark.json, 70 trial workflow từ R-workflow-C-001-s11 đến R-workflow-C-014-s55)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 (14 claim public × seed 11,22,33,44,55)
- Cost per success (mô phỏng, VND): 28.79
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0 (ma trận student 248/248 passed, gồm T-secret và T-approval; test_trace_has_no_secret_or_ticket)

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Trên cùng 14 claim public, cùng 5 seed và cùng bảng giá (`src/reports/benchmark.json`), cả ba shape nhóm viết đều đạt pass 1.000, pass^5 1.000, variance 0. Khác biệt duy nhất là chi phí: workflow 28.79 VND/success, single 38.94 (+35%), orchestrator 57.58 (×2.0), swarm 49.57 nhưng còn rớt C-002 ở seed 55 (pass^5 0.929). Claim của LogiX là chuỗi bước tuần tự, mọi quyết định tiền đã do code (`compute_compensation` + host) nắm; model không thêm thông tin nào làm đổi kết quả. Vì vậy nhóm chọn shape ít tự chủ nhất mà vẫn đạt: **workflow** (1 model call/claim, chỉ để soạn câu trả lời).

## Có đáng đổi lấy multi-agent không

Không, với dữ liệu hiện tại. Orchestrator trả gấp đôi chi phí và thêm một ranh giới handoff phải bảo vệ mà không tăng pass rate; swarm vừa đắt hơn vừa dao động theo seed. Quyết định sẽ đảo lại nếu: (1) ticket có thông tin phi cấu trúc thật sự cần model đọc (ví dụ ảnh hư hỏng, mô tả cần phân loại) mà order row không có; (2) mỗi claim cần tra nhiều nguồn độc lập có thể chạy song song (nhiều kho, nhiều hãng vận chuyển), khi đó investigator mới có lợi; (3) bộ hidden cho thấy workflow fail trên nhánh mà luật cứng không bao được. Khi đó nhóm sẽ thử single trước orchestrator vì single chỉ đắt hơn 35%.

## Trace và bằng chứng

Trace của workflow ghi các event: `claim` (claim_id, found, order_id), `order` (kết quả `lookup_order` đã qua allowlist `ORDER_FIELDS`), `quote` (amount, reason, clause_ids, parts), `host_call` (số quote đầy đủ gửi host), `host_result` (ok, reason, conflict), `decision` (status, proposal_amount, reason). Cố ý **không** ghi: nguyên văn ticket (chữ khách có thể chứa SĐT, địa chỉ, câu prompt injection), `principal_id`, `parent_secret`, `raw_headers_json`, `approval_id`, order row thô (có SĐT, địa chỉ, tên hàng, ghi chú nội bộ). Shape không in gì ra stdout và không ghi file nào khác ngoài `traces/<run_id>.json`, nên scanner quét đủ mọi output. Nếu trace nằm ngoài chỗ scanner quét được thì không chứng minh được là sạch; vì thế nhóm giữ một file duy nhất theo contract và có test `test_trace_has_no_secret_or_ticket` quét canary, header và ticket cho cả ba shape.

## Giới hạn

MockLLM không phải model sản xuất: pass rate 1.000 phản ánh việc shape không giao quyết định cho model, không chứng minh model thật sẽ ổn. Cost là VND mô phỏng theo `config/pricing.yaml`, không phải hóa đơn API. Latency để `unavailable`. Bộ public chỉ có 14 claim; nhóm chưa chạy `student_drop/`. Không sửa JSON trong `src/reports/`.

# Báo cáo cá nhân — 2A202606785_NguyenDinhTien

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đình Tiến
- MSSV: 2A202606785
- Email:
- GitHub:

## 2. Phần việc phụ trách

Ledger/crash và evaluation: crash suite, benchmark 4 shape, ablation R1, ADR, research card, báo cáo nhóm.

## 3. Đóng góp cụ thể

- Commit `9fba976`: sinh `src/reports/benchmark.json`, `crash.json`, `ablation_r1.json` bằng đúng lệnh trong `src/reports/README.md`.
- Test: `test_ticket_delay_is_ignored_seed55` (C-002 seed 55, trial làm swarm fail; ba shape của nhóm đều `denied`).
- Viết `decision_adr.md` và `research_card.md`.

## 4. Bằng chứng

- `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety 20/20`.
- `python -m lab8.check_submission` → 0 FAIL.

## 5. Công cụ AI đã dùng

Dùng ChatGPT tóm tắt paper arXiv 2512.08296 khi điền research card. Tự kiểm bằng cách đọc abstract gốc và chỉ ghi kết luận có trong paper.

## 6. Tự đánh giá

Học được cách so kiến trúc công bằng: cùng corpus, cùng seed, cùng bảng giá, chỉ đổi một biến. Swarm rớt pass^5 chỉ vì 1 trial nhưng đó đúng là loại lỗi nguy hiểm (hoàn tiền sai).

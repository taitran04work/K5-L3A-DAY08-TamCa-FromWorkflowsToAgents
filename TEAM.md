# Team

## Thông tin nhóm

- Tên nhóm: TamCa
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TamCa-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: repo `K5-L3A-DAY08-TamCa-FromWorkflowsToAgents`, nhánh `main`, commit code chốt `aedd1bf`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Trần Minh Anh | 20240001 | anh.tm@example.edu.vn | tmanh | Workflow + integration |
|   2 | Lê Hoàng Bảo | 20240002 | bao.lh@example.edu.vn | lhbao | Single agent (ReAct) |
|   3 | Phạm Thu Hà | 20240003 | ha.pt@example.edu.vn | ptha | Orchestrator + handoff + trace |
|   4 | Võ Quốc Dũng | 20240004 | dung.vq@example.edu.vn | vqdung | Ledger/crash + evaluation, báo cáo |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Minh Anh | Workflow + integration | aedd1bf (`lab8/shapes/workflow.py`) | `tests/test_team_shapes.py::test_one_refund_across_shapes_on_same_store` |
| Lê Hoàng Bảo | Single agent | aedd1bf (`lab8/shapes/single.py`) | `tests/test_team_shapes.py::test_single_stays_under_step_cap` |
| Phạm Thu Hà | Orchestrator + handoff | aedd1bf (`lab8/shapes/orchestrator.py`) | `tests/test_team_shapes.py::test_orchestrator_handoff_carries_no_parent_facts`, `test_trace_has_no_secret_or_ticket` |
| Võ Quốc Dũng | Ledger/crash + evaluation | 9fba976 (`src/reports/*.json`, ADR, research card) | `tests/test_team_shapes.py::test_ticket_delay_is_ignored_seed55` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Báo cáo cá nhân: `report/team/20240001_TranMinhAnh.md`, `20240002_LeHoangBao.md`, `20240003_PhamThuHa.md`, `20240004_VoQuocDung.md`.

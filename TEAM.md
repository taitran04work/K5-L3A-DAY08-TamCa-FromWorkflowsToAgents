# Team

## Thông tin nhóm

- Tên nhóm: TamCa
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TamCa-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: repo `K5-L3A-DAY08-TamCa-FromWorkflowsToAgents`, nhánh `main`, commit code chốt `aedd1bf`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Trần Hữu Tài | 2A202603944 |  |  | Workflow + integration |
|   2 | Nguyễn Thành Công | 2A202603967 |  |  | Single agent (ReAct) |
|   3 | Đồng Văn Quyến | 2A20260564 |  |  | Orchestrator + handoff + trace |
|   4 | Nguyễn Đình Tiến | 2A202606785 |  |  | Ledger/crash + evaluation, báo cáo |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Hữu Tài | Workflow + integration | aedd1bf (`lab8/shapes/workflow.py`) | `tests/test_team_shapes.py::test_one_refund_across_shapes_on_same_store` |
| Nguyễn Thành Công | Single agent | aedd1bf (`lab8/shapes/single.py`) | `tests/test_team_shapes.py::test_single_stays_under_step_cap` |
| Đồng Văn Quyến | Orchestrator + handoff | aedd1bf (`lab8/shapes/orchestrator.py`) | `tests/test_team_shapes.py::test_orchestrator_handoff_carries_no_parent_facts`, `test_trace_has_no_secret_or_ticket` |
| Nguyễn Đình Tiến | Ledger/crash + evaluation | 9fba976 (`src/reports/*.json`, ADR, research card) | `tests/test_team_shapes.py::test_ticket_delay_is_ignored_seed55` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Báo cáo cá nhân: `report/team/2A202603944_TranHuuTai.md`, `2A202603967_NguyenThanhCong.md`, `2A20260564_DongVanQuyen.md`, `2A202606785_NguyenDinhTien.md`.

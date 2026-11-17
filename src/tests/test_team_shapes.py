"""Test bổ sung của nhóm TamCa cho ba shape A/B/C."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.db import connect
from lab8.durability import committed_audit_count, get_refund
from lab8.shapes import SHAPES

TEAM_SHAPES = ["workflow", "single", "orchestrator"]


@pytest.mark.parametrize("shape", TEAM_SHAPES)
def test_ticket_delay_is_ignored_seed55(public_db, shape):
    """C-002: ticket khai trễ nhiều hơn order row. Shape của nhóm không tin ticket,
    kể cả ở seed 55 (seed làm swarm hỏng)."""
    result = SHAPES[shape]("C-002", seed=55, store_path=str(public_db))
    assert result.status == "denied"
    assert result.proposal_amount == 0
    conn = connect(str(public_db))
    try:
        assert get_refund(conn, "C-002") is None
    finally:
        conn.close()


def test_single_stays_under_step_cap(public_db):
    """Vòng ReAct dừng trước 8 bước và mọi model call đều được đếm vào budget."""
    result = SHAPES["single"]("C-001", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    assert 1 <= result.model_calls <= 8 + 1  # 8 bước decide + 1 lần soạn trả lời
    assert result.cost_estimate > 0


@pytest.mark.parametrize("shape", TEAM_SHAPES)
def test_trace_has_no_secret_or_ticket(public_db, shape):
    """Trace không chứa canary, parent_secret, header hay nguyên văn ticket."""
    conn = connect(str(public_db))
    ticket = conn.execute("SELECT ticket FROM claims WHERE claim_id = 'C-001'").fetchone()["ticket"]
    conn.close()
    result = SHAPES[shape]("C-001", seed=11, store_path=str(public_db))
    body = Path(result.trace_path).read_text(encoding="utf-8")
    assert json.loads(body)["run_id"] == result.run_id
    for banned in ("CANARY_SECRET_", "parent_secret", "raw_headers", ticket):
        assert banned not in body


def test_orchestrator_handoff_carries_no_parent_facts(public_db):
    """Handoff trong trace chỉ có field allowlist, facts rỗng, tool chỉ đọc."""
    result = SHAPES["orchestrator"]("C-001", seed=11, store_path=str(public_db))
    events = json.loads(Path(result.trace_path).read_text(encoding="utf-8"))["events"]
    handoff = next(e["payload"] for e in events if e["kind"] == "handoff")
    assert handoff["facts"] == {}
    assert "issue_refund" not in handoff["allowed_tools"]


def test_one_refund_across_shapes_on_same_store(public_db):
    """Ba shape lần lượt xử lý cùng một claim trên cùng store: vẫn một refund."""
    for shape in TEAM_SHAPES:
        result = SHAPES[shape]("C-001", seed=11, store_path=str(public_db))
        assert result.status == "resolved"
    conn = connect(str(public_db))
    try:
        assert get_refund(conn, "C-001")["amount_vnd"] == 35000
        assert committed_audit_count(conn, "C-001") == 1
    finally:
        conn.close()

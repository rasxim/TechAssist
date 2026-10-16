"""Database tests. Use TEST_DATABASE_URL, or DATABASE_URL (Supabase) if that is the only one set;
skipped when neither is set. Each test works in its own temporary schema, dropped afterwards,
so the real tables in `public` are never touched."""

import os
import uuid

import pytest

from kb import config, db  # importing config loads .env
from kb.inventory import build_inventory
from kb.validate import run_checks

from .conftest import build_workbook

TEST_URL = os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL")
pytestmark = pytest.mark.skipif(not TEST_URL, reason="no TEST_DATABASE_URL or DATABASE_URL set")


@pytest.fixture
def conn():
    schema = f"kb_test_{uuid.uuid4().hex[:8]}"
    connection = db.connect(TEST_URL)
    connection.execute(f"create schema {schema}")
    connection.execute(f"set search_path to {schema}")
    connection.commit()
    db.migrate(connection)
    yield connection
    connection.rollback()
    connection.execute(f"drop schema {schema} cascade")
    connection.commit()
    connection.close()


def counts(conn):
    tables = ["kb_sources", "kb_issues", "kb_procedures", "kb_issue_procedures", "kb_reference_rows", "kb_links"]
    return {t: conn.execute(f"select count(*) from {t}").fetchone()[0] for t in tables}


def test_import_then_validate_passes(conn, workbook, gid_map):
    db.apply_inventory(conn, build_inventory(workbook, gid_map))
    failed = [c for c in run_checks(conn, workbook) if not c.ok]
    assert not failed, failed


def test_reimport_creates_no_duplicates(conn, workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    db.apply_inventory(conn, inv)
    first = counts(conn)
    db.apply_inventory(conn, build_inventory(workbook, gid_map))
    assert counts(conn) == first


def test_removed_row_becomes_inactive_not_deleted(conn, tmp_path, gid_map):
    db.apply_inventory(conn, build_inventory(build_workbook(tmp_path / "v1.xlsx"), gid_map))
    v2 = build_workbook(tmp_path / "v2.xlsx", drop_row="How do I reset Duo?")
    db.apply_inventory(conn, build_inventory(v2, gid_map))
    status = conn.execute("select status from kb_issues where question = 'How do I reset Duo?'").fetchone()[0]
    assert status == "inactive"
    assert all(c.ok for c in run_checks(conn, v2))


def test_changed_text_on_published_procedure_waits_for_review(conn, tmp_path, gid_map):
    db.apply_inventory(conn, build_inventory(build_workbook(tmp_path / "v1.xlsx"), gid_map))
    conn.execute("update kb_procedures set status = 'published' where kind = 'steps'")
    conn.commit()
    v2 = build_workbook(tmp_path / "v2.xlsx", answer_override="1. New step")
    db.apply_inventory(conn, build_inventory(v2, gid_map))
    content, pending = conn.execute("select content, pending_content from kb_procedures where kind = 'steps'").fetchone()
    assert content.startswith("1. Upload your job")
    assert pending == "1. New step"

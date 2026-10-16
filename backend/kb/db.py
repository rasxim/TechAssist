"""Database writes for the knowledge base. Every import runs in one transaction."""

import json
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb

from .config import REPO_ROOT
from .inventory import Inventory

MIGRATIONS_DIR = REPO_ROOT / "supabase" / "migrations"
WORKBOOK_PROCEDURE_PREFIXES = ("cell:", "tab:")


def connect(url: str) -> psycopg.Connection:
    return psycopg.connect(url, autocommit=False)


def migrate(conn: psycopg.Connection, migrations_dir: Path = MIGRATIONS_DIR) -> list[str]:
    """Apply any migration files not applied yet, in filename order."""
    with conn.transaction():
        conn.execute(
            "create table if not exists kb_schema_migrations (filename text primary key, applied_at timestamptz not null default now())"
        )
        conn.execute("alter table kb_schema_migrations enable row level security")
        done = {row[0] for row in conn.execute("select filename from kb_schema_migrations")}
    applied = []
    for path in sorted(migrations_dir.glob("*.sql")):
        if path.name in done:
            continue
        with conn.transaction():
            conn.execute(path.read_text(encoding="utf-8"))
            conn.execute("insert into kb_schema_migrations (filename) values (%s)", (path.name,))
        applied.append(path.name)
    return applied


def apply_inventory(conn: psycopg.Connection, inv: Inventory) -> str:
    """Upsert the inventory. Records missing from this workbook become inactive; nothing is deleted
    except rows the importer fully derives (links, reference rows, auto issue-procedure links)."""
    with conn.transaction():
        run_id = conn.execute(
            "insert into kb_import_runs (workbook_name, workbook_hash, counts, warnings) values (%s, %s, %s, %s) returning id",
            (inv.workbook_name, inv.workbook_hash, Jsonb(inv.counts()), Jsonb(inv.warnings)),
        ).fetchone()[0]

        source_ids = _upsert_sources(conn, inv)
        issue_ids = _upsert_issues(conn, inv, source_ids)
        procedure_ids = _upsert_procedures(conn, inv, source_ids)
        _replace_reference_rows(conn, inv, procedure_ids)
        _replace_links(conn, inv, issue_ids, procedure_ids)
        _replace_auto_issue_procedures(conn, inv, issue_ids, procedure_ids)

        conn.execute("update kb_import_runs set finished_at = now() where id = %s", (run_id,))
    return str(run_id)


def _upsert_sources(conn, inv: Inventory) -> dict[str, str]:
    ids = {}
    for s in inv.sources.values():
        from_workbook = s.source_type in ("workbook_cell", "workbook_tab")
        # Workbook sources are refreshed on every import; web and private sources are owned by the fetch stage.
        ids[s.source_key] = conn.execute(
            """
            insert into kb_sources (source_key, source_type, access, title, url, sheet_name, cell_ref,
                                    fetch_status, content_hash, snapshot_text, retrieved_at)
            values (%(key)s, %(type)s, %(access)s, %(title)s, %(url)s, %(sheet)s, %(cell)s,
                    case when %(wb)s then 'ok' else 'not_fetched' end, %(hash)s, %(snap)s,
                    case when %(wb)s then now() end)
            on conflict (source_key) do update set
                source_type   = excluded.source_type,
                access        = excluded.access,
                title         = excluded.title,
                url           = excluded.url,
                sheet_name    = excluded.sheet_name,
                cell_ref      = excluded.cell_ref,
                fetch_status  = case when %(wb)s then 'ok' else kb_sources.fetch_status end,
                content_hash  = case when %(wb)s then excluded.content_hash else kb_sources.content_hash end,
                snapshot_text = case when %(wb)s then excluded.snapshot_text else kb_sources.snapshot_text end,
                retrieved_at  = case when %(wb)s then now() else kb_sources.retrieved_at end,
                is_active     = true,
                updated_at    = now()
            returning id
            """,
            {
                "key": s.source_key, "type": s.source_type, "access": s.access, "title": s.title, "url": s.url,
                "sheet": s.sheet_name, "cell": s.cell_ref, "wb": from_workbook,
                "hash": s.content_hash if from_workbook else None, "snap": s.snapshot_text if from_workbook else None,
            },
        ).fetchone()[0]
    conn.execute("update kb_sources set is_active = false, updated_at = now() where not (source_key = any(%s))", (list(ids),))
    return ids


def _upsert_issues(conn, inv: Inventory, source_ids) -> dict[str, str]:
    ids = {}
    for i in inv.issues:
        ids[i.slug] = conn.execute(
            """
            insert into kb_issues (slug, question, inline_notes, issue_kind, source_id, source_cell, sheet_row, review_flags)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
            on conflict (slug) do update set
                question     = excluded.question,
                inline_notes = excluded.inline_notes,
                issue_kind   = coalesce(kb_issues.issue_kind, excluded.issue_kind),
                source_id    = excluded.source_id,
                source_cell  = excluded.source_cell,
                sheet_row    = excluded.sheet_row,
                review_flags = excluded.review_flags,
                status       = case when kb_issues.status = 'inactive' then 'draft' else kb_issues.status end,
                updated_at   = now()
            returning id
            """,
            (i.slug, i.question, i.inline_notes, i.issue_kind, source_ids[i.source_key], i.source_cell, i.sheet_row, i.review_flags),
        ).fetchone()[0]
    conn.execute(
        "update kb_issues set status = 'inactive', updated_at = now() where status <> 'inactive' and not (slug = any(%s))",
        (list(ids),),
    )
    return ids


def _upsert_procedures(conn, inv: Inventory, source_ids) -> dict[str, str]:
    ids = {}
    for p in inv.procedures:
        # Changed text on a draft is replaced; on an approved/published procedure it waits in
        # pending_content for review, and the live version stays as it is.
        ids[p.procedure_key] = conn.execute(
            """
            insert into kb_procedures (procedure_key, kind, title, content, warnings, source_id, source_section, review_flags)
            values (%(key)s, %(kind)s, %(title)s, %(content)s, %(warnings)s, %(source)s, %(section)s, %(flags)s)
            on conflict (procedure_key) do update set
                title           = excluded.title,
                source_id       = excluded.source_id,
                source_section  = excluded.source_section,
                review_flags    = excluded.review_flags,
                content         = case when kb_procedures.status in ('draft', 'inactive') then excluded.content else kb_procedures.content end,
                warnings        = case when kb_procedures.status in ('draft', 'inactive') then excluded.warnings else kb_procedures.warnings end,
                kind            = case when kb_procedures.status in ('draft', 'inactive') then excluded.kind else kb_procedures.kind end,
                pending_content = case when kb_procedures.status in ('draft', 'inactive') or kb_procedures.content = excluded.content
                                       then null else excluded.content end,
                status          = case when kb_procedures.status = 'inactive' then 'draft' else kb_procedures.status end,
                updated_at      = now()
            returning id
            """,
            {
                "key": p.procedure_key, "kind": p.kind, "title": p.title, "content": p.content, "warnings": p.warnings,
                "source": source_ids[p.source_key], "section": p.source_section, "flags": p.review_flags,
            },
        ).fetchone()[0]
    conn.execute(
        """
        update kb_procedures set status = 'inactive', updated_at = now()
        where status <> 'inactive' and (procedure_key like 'cell:%%' or procedure_key like 'tab:%%')
          and not (procedure_key = any(%s))
        """,
        (list(ids),),
    )
    return ids


def _replace_reference_rows(conn, inv: Inventory, procedure_ids) -> None:
    tab_ids = [pid for key, pid in procedure_ids.items() if key.startswith("tab:")]
    conn.execute("delete from kb_reference_rows where procedure_id = any(%s)", (tab_ids,))
    with conn.cursor() as cur:
        cur.executemany(
            "insert into kb_reference_rows (procedure_id, row_key, position, fields, source_cell) values (%s, %s, %s, %s, %s)",
            [(procedure_ids[r.procedure_key], r.row_key, r.position, Jsonb(r.fields), r.source_cell) for r in inv.reference_rows],
        )


def _replace_links(conn, inv: Inventory, issue_ids, procedure_ids) -> None:
    conn.execute(
        """
        delete from kb_links
        where (owner_type = 'issue')
           or (owner_type = 'procedure' and owner_id in (
                select id from kb_procedures where procedure_key like 'cell:%%' or procedure_key like 'tab:%%'))
        """
    )
    owners = {"issue": issue_ids, "procedure": procedure_ids}
    with conn.cursor() as cur:
        cur.executemany(
            """
            insert into kb_links (owner_type, owner_id, cell_ref, display_text, url, link_kind, followed)
            values (%s, %s, %s, %s, %s, %s, %s)
            """,
            [(l.owner_type, owners[l.owner_type][l.owner_key], l.cell_ref, l.display_text, l.url, l.link_kind, l.followed) for l in inv.links],
        )


def _replace_auto_issue_procedures(conn, inv: Inventory, issue_ids, procedure_ids) -> None:
    conn.execute("delete from kb_issue_procedures where origin = 'auto'")
    with conn.cursor() as cur:
        cur.executemany(
            """
            insert into kb_issue_procedures (issue_id, procedure_id, position, role, origin)
            values (%s, %s, %s, %s, 'auto')
            on conflict (issue_id, procedure_id) do nothing
            """,
            [(issue_ids[ip.issue_slug], procedure_ids[ip.procedure_key], ip.position, ip.role) for ip in inv.issue_procedures],
        )


def inventory_to_json(inv: Inventory) -> str:
    from dataclasses import asdict

    data = asdict(inv)
    data["sources"] = list(data["sources"].values())
    return json.dumps(data, indent=2, ensure_ascii=False)

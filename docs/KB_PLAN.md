# Knowledge Base & Ingestion Plan (approved 2026-10-15)

Goal: an employee types an informal problem and gets complete, step-by-step instructions inside TechAssist, without opening external documentation. Steps are shown verbatim from the knowledge base; no LLM writes or rephrases them.

## Decisions

- **Starting index:** the `Common Questions` worksheet.
- **Other tabs:** links from Common Questions into other tabs of the workbook are followed; links found *inside* those tabs are recorded but not followed.
- **Private Google Docs:** in scope. An authorized employee exports them (File → Download → Markdown) into gitignored `kb_data/private/`. No Google auth code.
- **Conflicts:** the cheat sheet is the ultimate source of truth.
- **No LLM** in the pipeline. Sections are extracted deterministically by heading; a human maps issues to procedures in `curation.yaml`.
- **Publishing:** nothing reaches employees until it is approved (`draft → approved → published`).
- **Tickets:** not stored (Qualtrics is the record). A later migration adds a minimal per-case record with no client details, for dashboard counts.

## Pipeline

`python -m kb <stage>` from `backend/`:

| Stage | What it does |
|---|---|
| `inventory` | Read the workbook → issues, sources, links, reference tables (draft) |
| `fetch` | Public pages via httpx, saved as snapshots with hash and date; private docs read from `kb_data/private/` |
| `extract` | Split sources into verbatim sections → draft procedures |
| `review` | Write `kb_data/review/report.md` for the reviewer |
| `publish` | Apply `curation.yaml`; only approved procedures are published |
| `validate` | Integrity, verbatim, completeness and access checks; exits non-zero on failure |
| `refresh` | Re-fetch; changed content goes to `pending_content` and back to review while the published version stays live |

Each import runs in one database transaction. Re-running never creates duplicates: records are matched on stable keys, and records missing from a newer workbook become `inactive` (never deleted).

## Schema

`supabase/migrations/001_kb_schema.sql` creates:

- `kb_sources`
- `kb_issues`
- `kb_procedures`
- `kb_issue_procedures` (many-to-many)
- `kb_reference_rows`
- `kb_links`
- `kb_import_runs`

Row-level security is on for every table, with no policies. Only the backend and pipeline, using the service role or a direct Postgres connection, can read or write. Full-text search and pgvector columns come in later migrations.

## Validation

- **Nothing lost:** Common Questions rows = issues; workbook hyperlinks = `kb_links`; every record has a source; importing twice gives identical counts.
- **Nothing invented:** every procedure's text appears verbatim in its saved source.
- **Complete:** every published issue has at least one published procedure that is more than a link; everything else is `incomplete`.
- **Safe:** warnings preserved; RLS on; anonymous role has no access.

## Milestones

1. Schema + workbook import + validate
2. Public docs: fetch + extract + review report
3. Private docs (manual export)
4. Curation + publish + coverage report
5. Refresh

## Known manual-input items

| Item | Reason |
|---|---|
| A49 (secure erase) | Tab only links to more private docs, which are not followed |
| A43 (data transfer) | Tab only links to vendor pages, which are not followed |
| A8 (MAC addresses) | Tab only links to third-party sites, which are not followed |
| A11, A22, A27, A35, A41, A42 | Need the private-doc exports |

Data issues to check in review:

- B46 and B47 have identical answers; B47 looks like a copy-paste error.
- A19's link has a stray `)`.
- A10's question cell contains connection settings.

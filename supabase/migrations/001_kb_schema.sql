-- TechAssist knowledge base schema (Milestone 1).
-- Design: docs/KB_PLAN.md. Full-text search and pgvector columns come in later migrations.

create table kb_import_runs (
    id            uuid primary key default gen_random_uuid(),
    workbook_name text not null,
    workbook_hash text not null,
    counts        jsonb not null default '{}'::jsonb,
    warnings      jsonb not null default '[]'::jsonb,
    started_at    timestamptz not null default now(),
    finished_at   timestamptz
);

-- Every place content came from: a workbook cell, a workbook tab, a web page or a private doc.
create table kb_sources (
    id            uuid primary key default gen_random_uuid(),
    source_key    text not null unique,
    source_type   text not null check (source_type in ('workbook_cell', 'workbook_tab', 'web_page', 'private_doc')),
    access        text not null check (access in ('public', 'restricted', 'local')),
    title         text,
    url           text,
    sheet_name    text,
    cell_ref      text,
    fetch_status  text not null default 'not_fetched' check (fetch_status in ('ok', 'unavailable', 'not_fetched')),
    content_hash  text,
    snapshot_text text,
    retrieved_at  timestamptz,
    is_active     boolean not null default true,
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now()
);

-- One row per Common Questions entry.
create table kb_issues (
    id                 uuid primary key default gen_random_uuid(),
    slug               text not null unique,
    question           text not null,
    inline_notes       text,
    issue_kind         text check (issue_kind in ('troubleshooting', 'how_to', 'policy', 'referral', 'reference', 'resource')),
    qualtrics_category text,
    source_id          uuid not null references kb_sources (id),
    source_cell        text not null,
    sheet_row          integer not null,
    status             text not null default 'draft' check (status in ('draft', 'published', 'incomplete', 'inactive')),
    review_flags       text[] not null default '{}',
    review_notes       text,
    created_at         timestamptz not null default now(),
    updated_at         timestamptz not null default now()
);

-- The instructions employees see. `content` is verbatim source text.
create table kb_procedures (
    id                     uuid primary key default gen_random_uuid(),
    procedure_key          text not null unique,
    kind                   text not null check (kind in ('steps', 'reference_table', 'policy', 'referral')),
    title                  text not null,
    content                text not null,
    applies_to             text[],
    warnings               text[] not null default '{}',
    requires_authorization text,
    escalation             text,
    source_id              uuid not null references kb_sources (id),
    source_section         text,
    status                 text not null default 'draft' check (status in ('draft', 'approved', 'published', 'inactive')),
    pending_content        text,
    pending_hash           text,
    review_flags           text[] not null default '{}',
    approved_at            timestamptz,
    approved_by            text,
    created_at             timestamptz not null default now(),
    updated_at             timestamptz not null default now()
);

-- Many-to-many: an issue can need several procedures, a procedure can answer several issues.
-- origin 'auto' rows are proposed by the importer and rebuilt on every run; 'curated' rows come from curation.yaml.
create table kb_issue_procedures (
    issue_id     uuid not null references kb_issues (id) on delete cascade,
    procedure_id uuid not null references kb_procedures (id) on delete cascade,
    position     integer not null default 0,
    role         text not null default 'primary' check (role in ('primary', 'alternative', 'prerequisite', 'supplementary')),
    origin       text not null default 'auto' check (origin in ('auto', 'curated')),
    primary key (issue_id, procedure_id)
);

-- Rows of lookup tabs (BIOS keys, warranty sites, ...), attached to a reference_table procedure.
create table kb_reference_rows (
    id           uuid primary key default gen_random_uuid(),
    procedure_id uuid not null references kb_procedures (id) on delete cascade,
    row_key      text not null,
    position     integer not null,
    fields       jsonb not null,
    source_cell  text not null,
    unique (procedure_id, row_key)
);

-- Every hyperlink seen in the workbook, kept for traceability.
-- followed = false for links found inside other tabs (recorded, never fetched).
create table kb_links (
    id           uuid primary key default gen_random_uuid(),
    owner_type   text not null check (owner_type in ('issue', 'procedure')),
    owner_id     uuid not null,
    cell_ref     text not null,
    display_text text,
    url          text not null,
    link_kind    text not null check (link_kind in ('internal_tab', 'workbook_sheet', 'public_doc', 'private_doc', 'tool', 'external')),
    followed     boolean not null,
    unique (owner_type, owner_id, cell_ref, url)
);

create index kb_issue_procedures_procedure_idx on kb_issue_procedures (procedure_id);
create index kb_links_owner_idx on kb_links (owner_type, owner_id);

-- Access control: internal data. RLS on with no policies means only the service role
-- (backend + pipeline) and the table owner can read or write.
alter table kb_import_runs      enable row level security;
alter table kb_sources          enable row level security;
alter table kb_issues           enable row level security;
alter table kb_procedures       enable row level security;
alter table kb_issue_procedures enable row level security;
alter table kb_reference_rows   enable row level security;
alter table kb_links            enable row level security;

-- Supabase grants the browser-facing roles table access by default; take it away.
-- Guarded so the migration also runs on plain Postgres (used for local tests).
do $$
begin
    if exists (select 1 from pg_roles where rolname = 'anon') then
        revoke all on kb_import_runs, kb_sources, kb_issues, kb_procedures,
                      kb_issue_procedures, kb_reference_rows, kb_links from anon;
    end if;
    if exists (select 1 from pg_roles where rolname = 'authenticated') then
        revoke all on kb_import_runs, kb_sources, kb_issues, kb_procedures,
                      kb_issue_procedures, kb_reference_rows, kb_links from authenticated;
    end if;
end
$$;

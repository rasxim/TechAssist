# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

TechAssist is a real internal support workflow application for Lafayette College Tech Lounge employees.

Read `docs/PRODUCT_SPEC.md` before making architectural or product changes — it is the authoritative product spec (workflows, data model, state machine, phased build order, V1 scope).

Read `docs/DESIGN.md` before designing or implementing any frontend work — it is the visual source of truth, along with the reference images in `design-references/`.

## Core product principle

TechAssist is NOT a chatbot.

The primary workflow is:

```
Describe → Follow Steps → Solved / Need Help → Done
```

The Tech Lounge cheat sheet is the authoritative source of troubleshooting information. Never generate unsupported troubleshooting procedures — prefer escalation over guessing. The employee remains in control of final actions (especially sending a Slack escalation).

## Development philosophy

This project must be understandable and deployable. The developer is learning agentic AI while building it. Therefore:

- explain architecture before implementing major components
- use the simplest reasonable solution
- do not over-engineer
- do not introduce LangChain, LangGraph, CrewAI, AutoGen, or multi-agent architecture unless clearly justified
- distinguish LLM reasoning from deterministic application logic
- use structured outputs and validation where appropriate
- inspect existing code before changing it
- make incremental changes
- add tests for important behavior
- never hardcode credentials
- never invent product requirements
- prioritize reliability over architectural cleverness

## Coding workflow

Before significant implementation:

1. Read relevant documentation.
2. Inspect existing code.
3. Explain the proposed architecture.
4. Identify the smallest useful milestone.
5. Implement it.
6. Test it.
7. Explain what changed and why.

Do not attempt to build the entire application at once.

## Current status

- The Groq practice script (`main.py`) has been removed; no backend code exists yet.
- `Tech Lounge Cheat Sheet.xlsx` has been inspected: 10 tabs, ~150 rows total, a mix of natural-language Q&A, structured lookup tables, and link-only rows. Retrieval should be hybrid by content type via a single `search_knowledge_base(query)` function: deterministic lookup for structured tables, semantic/keyword/hybrid search for the Q&A tab (no embeddings needed yet at this size — try keyword/fuzzy first), and plain pass-through for link-only rows. See `docs/PRODUCT_SPEC.md` for detail.
- Several "Common Questions" answers are just links to external `help.lafayette.edu` articles or internal Google Docs rather than inline steps. **Decision changed (2026-10-15):** the knowledge base stores the actual procedure text, extracted verbatim from those pages (private docs via manual export), so employees never have to open external pages. See `docs/KB_PLAN.md`.
- TechAssist does not replace Qualtrics in V1 — it generates Qualtrics-ready field values (client info, description, troubleshooting steps actually performed, resolution) for the employee to manually copy in and submit themselves. See the case data model and field mapping in `docs/PRODUCT_SPEC.md`.
- The `.xlsx` is kept out of git (internal Lafayette document) and should stay gitignored, loaded from a local path rather than committed.
- Stack is Python/FastAPI (backend) + Next.js/React (frontend, less firm) + Supabase/Postgres (chosen for the knowledge base) + Groq — treat as a strong default per `docs/PRODUCT_SPEC.md`.
- Tickets are not stored (Qualtrics is the system of record); only a small per-case record without client details is kept for dashboard counts.

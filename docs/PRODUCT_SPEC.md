# TechAssist — Product Spec

TechAssist is an internal workflow application for Lafayette College Tech Lounge employees.

The author is a student employee in the Tech Lounge, and this product is based on a real workflow and real problems personally experienced there. This is not meant to be a portfolio-only demo, generic chatbot, or over-engineered agent experiment — it is meant to be something that could realistically be deployed and used by other Tech Lounge student employees.

This is also intended as a first serious agentic AI application, used to learn the architecture properly while building it — not another vibe-coded project where large amounts of generated code are accepted without being understood.

## The problem

When a student comes to the Tech Lounge with a technical issue, the employee currently has to manually understand the issue, search through an internal Tech Lounge cheat sheet, follow the procedure, manually document what happened in a form, and manually escalate through Slack if the issue cannot be resolved.

This workflow is fragmented and inconsistent. TechAssist should streamline the whole process.

The core employee workflow:

```
Describe Issue
→ Find Relevant Procedure
→ Follow Troubleshooting Steps
→ Solved OR Need Help
→ Generate Documentation / Escalate
→ Done
```

This should feel like a professional internal support tool, NOT like chatting with an AI. The AI should mostly be invisible infrastructure.

## Core problems to solve

### 1. Finding the right troubleshooting procedure

The Tech Lounge has an internal cheat sheet containing procedures for common technical problems. Currently, student employees have to manually search through it.

Example issue: *"A student's MacBook won't connect to Lafayette Wi-Fi. They tried reconnecting but it says unable to join network."*

The employee should be able to either speak this naturally into TechAssist using a microphone or type it. TechAssist should understand the messy natural-language description, search the Tech Lounge cheat sheet, retrieve the most relevant procedure, and display the steps clearly. The employee should not need to manually search through the documentation.

The Tech Lounge cheat sheet is the authoritative source of truth. TechAssist must NEVER invent troubleshooting procedures just because an LLM thinks something is likely to work. If the knowledge base does not contain a supported procedure, TechAssist should recommend escalation rather than guess.

### 2. Standardizing case/ticket documentation

TechAssist does **not** replace the existing system of record. The Tech Lounge already submits tickets through a Qualtrics form ("Tech Lounge Ticket"), and that remains the system used to submit tickets in V1. TechAssist's job is to generate clean, Qualtrics-ready field values that the employee reviews and manually copies into Qualtrics themselves — not to submit anything on their behalf.

After troubleshooting, either the issue is solved or it is not. Either way, TechAssist generates values for the real Qualtrics ticket fields:

- Client First & Last Name
- Client Lafayette NetID
- Client Phone Number
- Issue Category
- Existing Help Desk ticket number, if applicable
- Description of the issue
- Troubleshooting Steps Taken / Steps taken to resolve the issue
- Were you able to resolve this issue? (`Yes` / `Yes – with assistance from User Services` / `No – Please Follow Up With Client`)

TechAssist should generate values for these fields where possible. **Never invent a value** — if a field is unknown, leave it blank or mark it internally as missing.

There is no separate 5W (WHAT/WHO/WHY/...) ticket format — that was an earlier placeholder. The Qualtrics form itself is the structure. The "who is affected / observed symptom / device / error / context / timing" ideas from that earlier draft still matter, but only as an internal completeness checklist for what the generated **Description of the issue** should naturally cover — it should read as one concise professional paragraph, not labeled sections:

> "Student reported that their MacBook Air running macOS Sonoma could not connect to Lafayette Wi-Fi in Skillman Library. The device displayed the error 'Unable to join network.' The issue occurred each time the student attempted to connect."

**Troubleshooting Steps Taken** must list only steps the worker actually performed — never steps TechAssist suggested but that weren't carried out:

> "Verified Lafayette credentials, forgot and rejoined the Lafayette network, restarted Wi-Fi, and restarted the MacBook. The student successfully connected after rejoining the network."

**Symptom vs. diagnosis:** ticket text must describe observed behavior, not a guessed cause. Prefer "User cannot print to Lab Printer A" over "The printer is broken"; prefer "Student received 'Unable to join network' when connecting to Lafayette Wi-Fi" over "The authentication server is down." The LLM must not invent a cause unless approved Tech Lounge documentation clearly supports it.

The ticket-preview screen should mirror the Qualtrics form field-by-field (one block per field, each with its own Copy button, plus a Copy All) so the employee can review everything before copying it over. The exact official field set may change later after confirming requirements with the Tech Lounge supervisor. The important product problem is that student employees currently do not document cases consistently — TechAssist should make case documentation standardized and higher quality.

### 3. Standardizing escalation through Slack

If the employee cannot solve the issue, they select NEED HELP / ESCALATE. Escalation is usually needed when:

- the employee does not understand the issue
- the issue cannot be solved using the cheat sheet
- the documented procedure does not work
- the issue is Duo-related
- the issue requires permissions or access the student employee does not have
- the employee needs help from ITS or a supervisor

Currently, employees sometimes send poor Slack messages such as "I need help with this student." Instead, TechAssist should generate a structured escalation message, for example:

```
Tech Lounge Escalation

Student:
[Name]

Issue:
Unable to connect to Lafayette Wi-Fi

Device:
MacBook Air

Error:
"Unable to join network"

Steps attempted:
1. Checked Wi-Fi settings
2. Forgot network
3. Reconnected
4. Restarted device

Result:
Still unable to connect.

Request:
Assistance troubleshooting the student's network authentication issue.
```

Before generating the escalation, TechAssist should identify whether critical information is missing and ask only for important missing information — no unnecessary conversational back-and-forth.

Eventually, TechAssist should be able to send this message directly through Slack. However, the workflow should always be:

```
Generate escalation → Show preview → Employee reviews → Employee approves → Send Slack message
```

Never automatically send an escalation without employee approval.

Escalating does not replace filing a ticket. When the issue is unresolved, TechAssist generates **both** the Qualtrics ticket content (with resolution set to "No – Please Follow Up With Client") **and** the Slack escalation preview — the employee reviews and acts on both, not one or the other.

### 4. Case tracking / dashboard

TechAssist should keep basic track of cases handled. Potential useful information: number of cases handled, number solved, number escalated, recent cases, issue categories, timestamps.

The application may eventually have a minimal dashboard with widgets such as: primary Describe Issue / microphone widget, cases resolved, quick resources, recent cases. Quick Resources may include links such as the Tech Lounge Cheat Sheet, Student Handbook, ITS documentation, and other internal Tech Lounge resources.

This should NOT turn into a complex analytics dashboard. The primary purpose of the application is still helping the employee handle the student standing in front of them.

## User experience philosophy

The product should NOT be a chatbot. Do not build: a giant chat interface, chat bubbles, an AI avatar, a glowing AI orb, a generic "How can I help you?" assistant, unnecessary AI branding, excessive conversational turns, or generic SaaS dashboard clutter.

The employee's mental model should be: *"I have a problem. I describe it. I follow the steps. I either solve it or escalate it."*

The AI should feel like invisible infrastructure. The primary flow remains:

```
Describe → Follow Steps → Solved / Need Help → Done
```

The final UI will be minimal, sleek, dark, professional, and voice-first, but UI implementation is not a focus until explicitly requested.

## Input

The employee has two input options: voice and typing. Voice is the primary interaction — the employee presses a microphone and naturally describes the student's problem. Voice should be converted to text before entering the core AI workflow.

```
Voice → Speech-to-text → Text
Typing → Text
```

Both then enter the same backend workflow. Speech recognition should not be tightly coupled to the agent architecture — the agent should operate primarily on text.

## Knowledge base / retrieval

The Tech Lounge cheat sheet is the authoritative source of troubleshooting information. The likely approach is RAG, but a complicated vector architecture should not be assumed before inspecting the actual cheat sheet.

The cheat sheet has been inspected (a 10-tab Excel workbook, ~150 rows total) and it is not one uniform kind of content — it's a mix of:

1. Natural-language Q&A / support references (e.g. the "Common Questions" tab)
2. Structured lookup tables (e.g. BIOS keys by brand, MAC addresses by device, warranty links by brand, software availability)
3. Links to other documentation (many "Common Questions" answers just point to an external `help.lafayette.edu` article rather than containing inline steps)

Given that mix, retrieval should be **hybrid by content type**, not one single technique applied uniformly:

- Natural-language questions → semantic and/or keyword/hybrid search, returning the most relevant approved entry. At this size (~50 short Q&A rows) this likely does not need embeddings infrastructure — simple keyword/fuzzy scoring should be tried first, with embeddings only added if that proves insufficient.
- Structured tables → deterministic lookups (e.g. match brand/device name directly), not semantic search.
- Link-only rows → treated as an index/routing layer for V1: surface the topic and the link as-is, don't fetch or scrape the linked page. If the linked documents become available as content later, they can become retrievable sources in their own right.

The simplest reliable retrieval approach should be preferred, and do not blindly stringify the whole workbook into fixed-size chunks and embed everything — that ignores the structure that's actually there.

```
Employee description
→ normalize / interpret query
→ determine whether this is a natural-language question or a structured lookup
→ retrieve from the Tech Lounge knowledge base using the matching strategy
→ optional reranking
→ provide retrieved context to LLM
→ generate grounded troubleshooting steps
```

A likely tool: `search_knowledge_base(query)` — the orchestrator calls this one function and doesn't need to know whether the answer came from a deterministic lookup or a semantic match. It may return title, relevant content, source, relevance score, and metadata.

The Tech Lounge cheat sheet remains the authoritative source. If no supported procedure is found, TechAssist should say so and recommend escalation rather than guess.

Retrieval quality is more important than making the system look agentic. Retrieval should be evaluated separately from final LLM output. Eventually, build a small test dataset of representative Tech Lounge issues (Wi-Fi not connecting, Duo push not appearing, password problems, projector connection problems, printing problems, account access problems) and define what documentation should ideally be retrieved for each.

## Agentic AI architecture

This should be a legitimate agentic AI application, but without unnecessary agent complexity. Do NOT begin by creating a Router Agent, Retrieval Agent, Ticket Agent, Slack Agent, Supervisor Agent, Validation Agent, or multiple autonomous agents talking to each other — that would be over-engineering for V1.

Start with one orchestrating LLM/agent that can call explicit tools where needed:

```
Employee → TechAssist orchestrator → decides what operation is required
→ calls tool → Python executes tool → tool result returned → LLM produces structured output
```

Possible tools: `search_knowledge_base(query)`, `generate_ticket(case)`, `prepare_slack_escalation(case)`, `send_slack_escalation(message)`. Some of these may not actually need to be LLM tools and may be better implemented as normal deterministic Python functions — make that decision based on engineering needs, not on trying to maximize the number of "agents" or "tools".

## What should be LLM-driven vs. deterministic

Use normal deterministic application code for: database writes, IDs, timestamps, authentication, permissions, case status, state transitions, schema validation, Slack API calls, logging, retries, error handling.

Use LLM reasoning where natural-language understanding is actually useful: interpreting messy user issue descriptions, extracting useful issue information, query rewriting, grounded summarization, converting structured case data into clean ticket language, converting structured case data into a clean escalation message.

Do not let the LLM control things that normal software should control.

## Case data model

A structured representation of a Tech Lounge case, grounded in the actual Qualtrics ticket fields (not over-designed beyond what's actually useful):

```
client_name
client_netid
client_phone
issue_category
existing_ticket_number

initial_user_description
device_type
hostname
asset_tag
operating_system
exact_error_message

physical_location
network_context
software_application
browser_or_portal

issue_onset
issue_frequency
relevant_context

retrieved_sources
recommended_steps
steps_actually_attempted

resolution_status
resolution_summary

escalation_required
escalation_reason

qualtrics_description
qualtrics_troubleshooting_steps
```

The model must never invent case facts — if something is unknown, keep it unknown (leave the field blank / mark it missing internally, never guess).

A few fields need calling out specifically:

- **`resolution_status`** is the literal 3-way Qualtrics enum — `Yes` / `Yes – with assistance from User Services` / `No – Please Follow Up With Client`. This is distinct from the simple "Solved vs. Need Help" branch the employee picks mid-workflow: a case can be escalated and still end up "Yes – with assistance," so the two should not be collapsed into one field.
- **`recommended_steps` vs. `steps_actually_attempted`** are different fields on purpose. `recommended_steps` comes from retrieval (what the cheat sheet suggests); `steps_actually_attempted` is only what the employee confirms they actually did. Only the latter may ever feed `qualtrics_troubleshooting_steps`.
- **`qualtrics_description`** and **`qualtrics_troubleshooting_steps`** are the two LLM-authored fields, since they go straight into an institutional record: `qualtrics_description` must be grounded only in `initial_user_description` + retrieved context + known device/error/location fields; `qualtrics_troubleshooting_steps` must be grounded only in `steps_actually_attempted`, never `recommended_steps` that weren't confirmed performed.

### Field → Qualtrics form mapping

| Internal field | Qualtrics field |
|---|---|
| `client_name` | Client First & Last Name |
| `client_netid` | Client Lafayette NetID |
| `client_phone` | Client Phone Number |
| `issue_category` | Issue Category |
| `existing_ticket_number` | Existing Help Desk ticket number, if applicable |
| `qualtrics_description` | Description of the issue |
| `qualtrics_troubleshooting_steps` | Troubleshooting Steps Taken / Steps taken to resolve the issue |
| `resolution_status` | Were you able to resolve this issue? |

`client_name`, `client_netid`, and `client_phone` are captured directly from what the employee types/says — they are plain data entry, not something retrieved or generated.

## Possible case state machine

```
NEW → UNDERSTANDING → SEARCHING → TROUBLESHOOTING → SOLVED
                                                    → ESCALATION_PENDING → ESCALATED → CLOSED
```

State transitions should primarily be controlled by application logic. The LLM should not arbitrarily manage application state.

## Technical direction

- **Backend:** Python, FastAPI
- **Frontend:** Next.js, React
- **Database:** Supabase / PostgreSQL if persistent storage becomes necessary
- **LLM:** Currently experimenting with Groq; current model while learning is `openai/gpt-oss-20b`
- **Env:** `GROQ_API_KEY` via `python-dotenv` or equivalent; never hardcode secrets; never commit `.env` files
- Slack integration will come later

## Author's current experience / progress

Basic Python knowledge already in place. Already practiced making LLM API calls using Groq and understands the basic tool-calling loop:

```
User → LLM → LLM requests tool → Python executes function → tool result returned to LLM → LLM produces final answer
```

Already built a simple example tool (`get_hours()`) and handled `tool_calls` from the API response, understanding that the LLM does not execute Python itself — it requests the tool and the application code executes it.

Previously built a RAG project for Lafayette using a Lafayette catalog PDF, LlamaParse, Chroma, Sentence Transformers, BAAI/bge-small-en-v1.5, BAAI/bge-reranker-base, Groq, and student profile context — but that project was heavily vibe-coded and often not well understood. TechAssist is meant to be different: every major architectural component should be understood.

## Learning goal

This project has two equally important goals: (1) build and deploy a useful real product, and (2) learn agentic AI and AI application engineering properly. The entire application should not simply be generated. When introducing an important component, explain: what problem it solves, why it belongs in the architecture, what goes into it, what comes out of it, whether it should be deterministic or LLM-driven, what alternatives exist, and why this approach is chosen.

## Important engineering rules

1. **Do not over-engineer.** Prefer the simplest implementation that reliably solves the problem. Do not introduce infrastructure because it looks impressive.
2. **No premature agent frameworks.** Do not introduce LangChain, LangGraph, CrewAI, AutoGen, or similar frameworks unless there is a clear reason later — understand the underlying mechanics first.
3. **Inspect before editing.** Before changing code: inspect the repository, understand what already exists, identify what is useful vs. practice code, and make the smallest reasonable change. Do not rewrite working code unnecessarily.
4. **Build incrementally.** Do not build the whole product at once — work one milestone at a time.
5. **Explain architecture.** Before major code changes, explain the proposed architecture clearly.
6. **Use structured outputs.** Where important, prefer validated structured data instead of relying entirely on free-form LLM text (issue interpretation, retrieval result structure, ticket data, escalation data).
7. **Reliability over cleverness.** A simple system that reliably solves most Tech Lounge cases is better than an impressive multi-agent architecture that is difficult to debug.
8. **Never invent troubleshooting procedures.** Troubleshooting must be grounded in Tech Lounge documentation. If there is no verified procedure, recommend escalation.
9. **Never invent case facts.** Do not fill in unknown student, device, error, or troubleshooting information.
10. **Employee remains in control.** Important external actions require employee review and approval, especially Slack escalation.
11. **Keep deployment in mind.** Avoid hardcoded local file paths, machine-specific assumptions, hidden manual steps, secrets in code, or architecture that only works on one machine.
12. **Add tests for important behavior.** Especially retrieval, schema validation, case state transitions, ticket formatting, escalation formatting, tool behavior, and unsupported issue handling.

## Security / privacy

This is an internal university application — security is not an afterthought. Never expose API keys or Slack tokens, hardcode secrets, send secrets to the frontend, or log sensitive credentials. Use environment variables. Avoid storing unnecessary student information — only collect what's needed to support or document the case, and avoid unnecessarily sending personally identifiable information into LLM prompts. Flag institutional privacy requirements before production deployment if they become important.

## Observability

Eventually, it should be possible to inspect why the AI system behaved the way it did. Useful logs may include: original user input, speech transcript, interpreted issue, normalized retrieval query, retrieved documents, retrieval scores, model output, tool calls, tool outputs, latency, errors, final status, and whether the case was solved or escalated. This is especially important for debugging retrieval and agent behavior.

## Version 1 scope

V1 should include:

1. Employee describes issue by voice or typing
2. TechAssist searches Tech Lounge documentation
3. TechAssist returns verified troubleshooting steps
4. Employee follows steps
5. Employee selects Solved or Need Help
6. TechAssist generates standardized, Qualtrics-ready ticket content (field-by-field, matching the real Tech Lounge Qualtrics ticket form)
7. If unresolved, TechAssist additionally generates a standardized Slack escalation message
8. Employee reviews the ticket content (and escalation message, if generated)
9. Employee approves Slack send (if escalating)
10. Employee manually copies the ticket fields into Qualtrics and submits it themselves
11. Basic case tracking

V1 should NOT include unnecessary extras. Do not integrate directly with Qualtrics in V1, and do not automate form submission — copy/paste ticket generation is enough.

TechAssist is not trying to replace every Tech Lounge system — it's an intelligent workflow layer that sits between the employee, the cheat sheet/documentation, Qualtrics, and Slack, reducing searching, reducing repeated typing, standardizing documentation, and improving escalations.

**Keep for V1:** issue intake, knowledge retrieval, troubleshooting guidance, structured case state, Qualtrics-ready output, Slack escalation preview/send, basic case tracking.

**Do not build:** direct Qualtrics integration, automatic ticket submission, autonomous troubleshooting, multi-agent complexity, unnecessary analytics, generic chatbot UX.

## Development order

1. Clean repository setup
2. Obtain and understand Tech Lounge cheat sheet
3. Build the simplest reliable `search_knowledge_base(query)`
4. Evaluate retrieval quality with representative queries
5. Generate grounded troubleshooting instructions
6. Create structured case model
7. Generate standardized solved-case ticket
8. Generate standardized escalation message
9. Add Slack integration with employee approval
10. Expose backend through FastAPI
11. Build frontend workflow
12. Add persistence / case history / dashboard information
13. Production hardening: authentication, permissions, logging, testing, error handling, monitoring, deployment

Do not blindly follow this roadmap if inspection reveals a better order, but preserve the principle of incremental development.

## Immediate priority

Transitioning from practice code into the actual TechAssist project: set up the repository, Claude instructions, files, and project structure first. After that, the first major technical milestone is reliable retrieval from the Tech Lounge cheat sheet — inspect the actual cheat sheet first and recommend the simplest approach before assuming a complex vector database is required.

## Definition of success

TechAssist is successful if a real Tech Lounge employee can use it during a real student interaction to: quickly describe a problem, immediately get the relevant documented procedure, follow the steps, mark the issue solved or unresolved, generate consistent documentation, generate a useful escalation if necessary, and complete the whole interaction faster and more consistently than the current manual process.

Not "use as much AI as possible." Not "build the most complicated agent." Not "make an impressive architecture diagram." Solve the actual Tech Lounge workflow.

## North star

Whenever considering adding a feature, framework, abstraction, agent, or integration, ask: *"Does this make it faster, easier, more reliable, or more consistent for a Tech Lounge employee to help the student currently standing in front of them?"* If the answer is no, it is probably not important for V1.

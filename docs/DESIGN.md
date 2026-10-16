# TechAssist — Frontend Design Specification

## Design Goal

TechAssist should feel like a polished internal tool used by Lafayette College Tech Lounge employees.

The visual style should be:

- dark
- sleek
- professional
- restrained
- minimal without feeling empty
- functional rather than decorative

Avoid:

- generic SaaS styling
- chatbot interfaces
- AI avatars or glowing orbs
- excessive gradients
- glassmorphism
- neon effects
- excessive colors
- oversized cards
- oversized typography
- generic shadcn styling

AI should feel like invisible infrastructure.

Core flow:

Describe Issue → Find Procedure → Troubleshoot → Solved / Need Help → Ticket / Escalation → Done

---

## Reference Images

Reference images are the visual source of truth.

Store them in:

`/design-references/`

Pages:

- `dashboard.png`
- `understanding.png`
- `troubleshooting.png`
- `resolved.png`
- `escalation.png`
- `history.png`

Do not reinterpret these images as inspiration.

Match their:

- layout
- proportions
- spacing
- card dimensions
- typography hierarchy
- colors
- alignment
- information density

---

## Target Viewport

Primary desktop target:

`1536 × 1024`

Optimize desktop first.

Do not compromise desktop fidelity to support smaller screens during the initial implementation.

---

## Color System

```css
--background: #070A0E;
--background-secondary: #090D13;

--surface: #0C1118;
--surface-raised: #10161F;
--surface-hover: #131A24;

--border: rgba(255,255,255,0.08);
--border-strong: rgba(255,255,255,0.12);

--text-primary: #F3F4F6;
--text-secondary: #9CA3AF;
--text-muted: #68707D;

--maroon: #8A1538;
--maroon-hover: #9E1B45;
--maroon-dark: #64102A;

--success: #59C9A5;
--warning: #D69A45;
--danger: #D65A6F;
```

Use Lafayette maroon for primary actions and active states.

Use green only for solved states.

Use amber only for escalated/warning states.

Avoid adding new colors unless necessary.

---

## Typography

Preferred font:

`Geist`

Fallback:

`Inter`

Approximate scale:

- Page title: 28–32px
- Large metric: 36–48px
- Widget title: 16–20px
- Body: 14–16px
- Metadata: 12–13px

Avoid oversized marketing-style typography.

The interface should feel compact and operational.

---

## Layout

Approximate desktop dimensions:

- Sidebar: 80–88px
- Page padding: 20–24px
- Header: 90–105px
- Grid gaps: 18–20px
- Card radius: 14–16px

Avoid excessive empty space.

The application should feel like a usable workstation, not a concept poster.

---

## Cards

Cards should use:

- dark surfaces
- subtle 1px borders
- 14–16px radius
- minimal shadows

Avoid:

- large glows
- strong transparency
- glass effects
- colorful card backgrounds

---

## Sidebar

Use a compact icon-only sidebar.

Navigation:

- Home
- Cases
- Resources
- Settings

Active state:

- subtle maroon background
- brighter icon

Inactive state:

- muted gray

Use tooltips for icons.

Keep the sidebar visually quiet.

---

## Header

Left:

- TechAssist
- Lafayette College Tech Lounge

Right:

- employee greeting
- optional date/time
- Staff Online indicator

Keep the header minimal.

---

# Dashboard

The Dashboard is the primary visual baseline.

Layout:

```text
┌───────────────────────┬──────────────────┐
│                       │ Cases Today      │
│ Start a New Case      ├──────────────────┤
│                       │ Recent Cases     │
│                       │                  │
└───────────────────────┴──────────────────┘

┌──────────────────────────────────────────┐
│ Quick Resources                          │
└──────────────────────────────────────────┘
```

Approximate proportions:

- Left: 60%
- Right: 40%
- Gap: 18–20px

---

## Start a New Case

Structure:

```text
Start a New Case

Describe the student's issue using your voice or type it below.

[ microphone ]

Tap to record

[ Describe the issue... ]
```

Voice is primary.

Typing is secondary.

Do not split them into competing major widgets.

---

## Microphone

Target diameter:

`140–150px`

Style:

- matte Lafayette maroon
- white microphone icon
- subtle border
- minimal shadow
- almost no glow

Idle:

- static
- no pulse
- no aura

Recording:

- restrained ring animation
- `Listening...`

Processing:

- muted appearance
- `Finding the right steps...`

The microphone should look like a professional button, not an AI object.

---

## Cases Today

Show only useful shift context:

- total cases
- solved
- escalated

A small progress ring is acceptable.

Avoid unnecessary analytics.

---

## Recent Cases

Show approximately 3–5 cases.

Each row:

- issue
- device
- status
- relative time

Example:

```text
Wi-Fi connection issue
MacBook · Solved                          2m ago
```

Keep rows compact.

---

## Quick Resources

Include:

- Tech Lounge Cheat Sheet
- Student Handbook
- ITS Documentation
- Tech Lounge Slack

Use compact resource cards or rows.

Each should contain:

- icon
- title
- short description
- arrow/link

---

# Workflow Stepper

Stages:

`Understand → Find Solution → Troubleshoot → Complete`

Use:

- thin connector
- small numbered nodes
- maroon active state
- checked completed state
- muted inactive state

Keep it secondary to page content.

---

# Understanding Page

Show:

- original transcript
- editable issue description
- detected information
- retrieval/search progress

Example:

```text
Understanding the issue...

"Student's MacBook cannot connect to Lafayette Wi-Fi..."

Detected Information

Device: MacBook
Category: Network
Error: Unable to join network

Searching Tech Lounge procedures...
```

Avoid AI-thinking effects.

---

# Troubleshooting Page

Layout:

```text
Recommended Procedure        Case Details

1. Step
2. Step
3. Step

[ Need Help / Escalate ] [ Mark as Solved ]
```

Procedure:

- numbered
- concise
- easy to scan
- clearly shows current/completed steps
- shows source

Case Details may contain:

- device
- operating system
- exact error
- location
- network

Only display known information.

---

# Solved / Qualtrics Preview

TechAssist does not submit Qualtrics in V1.

The employee reviews the generated content and manually copies it into Qualtrics.

Display:

- Client First & Last Name
- Client Lafayette NetID
- Client Phone Number
- Issue Category
- Existing Ticket Number
- Description of the Issue
- Troubleshooting Steps Taken
- Resolution

Resolution options:

- Yes
- Yes – with assistance from User Services
- No – Please Follow Up With Client

Each field should have a Copy button.

Also provide:

- Copy All
- Back to Troubleshooting
- Complete Case

The screen should look like a polished preview, not a recreation of Qualtrics.

---

## Ticket Content

Do not display:

- WHO
- WHAT
- WHERE
- WHEN
- WHY

Those are internal completeness principles only.

Write natural support documentation.

Example:

> Student reported that their MacBook Air running macOS Sonoma could not connect to Lafayette Wi-Fi in Skillman Library. The device displayed the error "Unable to join network."

Troubleshooting should contain only steps actually performed.

Never include steps merely suggested by TechAssist.

---

# Escalation Page

Flow:

`Generate → Review → Edit → Approve → Send`

Display a Slack preview containing relevant information such as:

- Student
- Issue
- Device
- Error
- Steps Attempted
- Result
- Request

Actions:

- Edit Message
- Send to Slack

Use amber to indicate unresolved status.

Use maroon for the primary send action.

Never send automatically.

---

# Case History

Use a compact table.

Columns:

- Date
- Issue
- Device
- Status

Optional:

- Search
- Status filter
- Date filter

Do not turn this page into an analytics dashboard.

---

# Buttons

Primary:

- maroon
- white text
- 10–12px radius

Secondary:

- dark surface
- subtle border
- white/gray text

Prefer explicit labels:

- Mark as Solved
- Need Help / Escalate
- Send to Slack
- Complete Case
- Copy All

Avoid vague labels when possible.

---

# Inputs

Use:

- dark background
- subtle border
- white text
- muted placeholder
- visible focus state
- compact height

Do not style inputs like chatbot composers.

---

# Status

Solved:

- subtle green tint
- green indicator
- green text

Escalated:

- subtle amber tint
- amber indicator
- amber text

Keep badges compact.

---

# Icons

Use Lucide React.

Keep icon size and stroke consistent.

Icons should support the interface, not dominate it.

---

# Motion

Use subtle functional transitions only.

Recommended:

`150–250ms`

Acceptable:

- hover transitions
- recording ring
- progress updates
- small fades

Avoid:

- bouncing
- parallax
- dramatic scaling
- glowing animations

---

# Visual QA

For every page:

1. inspect the reference image
2. render at `1536 × 1024`
3. capture a screenshot
4. compare against the reference
5. identify the largest differences
6. fix them
7. repeat

Fix in this order:

1. page geometry
2. component dimensions
3. alignment
4. spacing
5. typography
6. colors
7. borders/shadows
8. details

Do not polish small details while dimensions are incorrect.

---

# Approved Baseline Rule

Once a page is approved, do not redesign it while implementing another page.

The Dashboard becomes the baseline for:

- sidebar
- header
- colors
- spacing
- typography
- cards
- borders
- buttons
- status styles

New pages should extend the established design system.

---

# Implementation Rules

Before frontend changes:

1. read this file
2. inspect the relevant reference image
3. inspect the existing implementation
4. preserve approved components

Do not:

- add backend logic unless requested
- introduce random colors
- introduce new visual patterns unnecessarily
- use generic shadcn styling as the product identity
- redesign approved pages

Use mock data during frontend development.

The final product should look like a professional internal application Lafayette College could realistically deploy.

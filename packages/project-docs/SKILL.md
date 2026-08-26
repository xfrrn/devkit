---
name: project-docs
description: Guide a vague software-project idea into a development-ready documentation baseline, or keep requirements, architecture, contracts, plans, progress, and ADRs aligned while a project is being developed. Use before development starts or during active software development.
metadata:
  author: xfrrn
  version: "1.3.0"
---

# Project Docs

Maintain the smallest useful set of project documents. Keep product intent,
implementation facts, contracts, plans, history, and decisions consistent
without creating empty documentation for its own sake.

## Select the lifecycle workflow

### 1. Preparing a new project

Use **Initialize** when meaningful implementation has not started. Read
[references/initialization-interview.md](references/initialization-interview.md),
guide the user from their initial idea through the blocking product and design
questions, then create a development-ready baseline.

### 2. Actively developing a project

When meaningful source code already exists or the user says development is in
progress, read
[references/development-maintenance.md](references/development-maintenance.md)
and infer the needed operation:

- **Formalize**: derive missing documentation from current repository evidence.
- **Update**: synchronize documents affected by a requirement or implementation change.
- **Audit**: report gaps, contradictions, stale content, and duplicated facts.
- **ADR**: record one important, expensive-to-reverse, or disputed decision.
- **Progress**: append a meaningful progress entry and update milestone status.

The user's stated stage overrides inference from the repository. A scaffold or
empty module alone does not mean development has started.

For Initialize, Formalize, Update, or Audit, read
[references/document-map.md](references/document-map.md) to select affected
documents. For a full audit or final consistency pass, also read
[references/quality-checklist.md](references/quality-checklist.md).

## Ground every statement

For an existing repository, inspect the smallest useful evidence set: its
README and docs, manifests, entry points, configuration, API definitions,
database schema or migrations, tests, and CI/deployment files. Do not infer
implementation facts from directory names when code or configuration can
verify them.

Treat information as one of:

- **Fact**: supported by user input, code, configuration, tests, or accepted docs.
- **Decision**: an intentional choice recorded by its owner or an accepted ADR.
- **Assumption**: a reasonable but unconfirmed working belief.
- **Unknown**: information still needed.

Mark non-facts explicitly with `[假设]`, `[待确认]`, or `[暂定]`. Never fill a
template by turning an example or assumption into a project fact.

For Initialize, a short project description is enough to begin: extract what
the user already supplied, then lead the missing discovery. For other modes,
ask one consolidated set of blocking questions when essential context is
missing. Proceed with visible assumptions only for non-blocking gaps.

## Create only what is useful

Templates live under `assets/docs/`. The core baseline is:

```text
docs/
├── 00-project-brief.md
├── 01-requirements.md
└── 02-system-design.md
```

Add Domain Model, API Contract, Data Design, Security, Roadmap, Testing,
Progress Log, or ADRs only when the project or request has corresponding
content. Existing issue trackers, OpenAPI files, schemas, migrations, or other
accepted sources may remain authoritative; link them instead of duplicating
them.

To initialize the core baseline, run:

```text
scripts/init_project_docs.py --target <project>
```

Use `--all` only when the user explicitly wants every template. The script
must not write outside the target project or overwrite existing files unless
the user explicitly requests replacement.

## Work in dependency order

For a new project, derive content in this order where applicable:

```text
Project Brief → Requirements → Domain Model → System Design
              → API/Data → Security → Testing → Roadmap → Progress
```

Numeric filenames are a stable reading order, not a requirement to create or
fill every file.

Keep each fact in one authoritative place:

- scope and goals: Brief/Requirements;
- business terms and rules: Domain Model;
- interface fields: OpenAPI or API Contract;
- actual database shape: schema/migrations;
- architecture rationale: ADRs;
- current plan: Roadmap;
- actual history: Progress Log.

Use cross-references elsewhere. Add stable identifiers such as `FR-001`,
`AC-001`, `M0`, or `ADR-001` only when they improve real traceability.

## Mode-specific rules

### Progress

- Append entries under `YYYY-MM-DD`; do not rewrite history.
- Record outcomes, blockers, deviations, and the next concrete action.
- Keep future plans in Roadmap and low-value implementation details out.

### ADR

- Use the next sequential number.
- Do not silently rewrite accepted ADRs.
- Replace a decision with a new ADR and mark the old one `Superseded by ADR-XXX`.

## Writing standard

- Use the project's language.
- Be concise, specific, and testable.
- Use diagrams only when they explain a real project relationship.
- Do not invent dates, owners, targets, legal conclusions, or capabilities.
- Use ISO dates (`YYYY-MM-DD`) and statuses `Draft`, `In Review`, `Approved`, or `Deprecated`.

Before finishing, verify that scope, domain terms, API/data shapes, security
controls, tests, roadmap state, and progress history do not contradict one
another.

Report created and updated files, assumptions and unresolved questions,
detected contradictions or risks, and the next useful step. Do not paste files
that already exist in the workspace.

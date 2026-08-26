---
name: project-docs
description: Create, formalize, update, or audit maintainable software-project documentation, including requirements, architecture, API/data/security design, roadmaps, progress logs, and ADRs. Use when documentation must be grounded in repository evidence and kept consistent across changes.
metadata:
  author: xfrrn
  version: "1.1.0"
---

# Project Docs

Maintain the smallest useful set of project documents. Keep product intent,
implementation facts, contracts, plans, history, and decisions consistent
without creating empty documentation for its own sake.

## Select the mode

- **Initialize**: create a minimal baseline for a new project.
- **Formalize**: derive current documentation from an existing repository.
- **Update**: change only documents affected by a requirement or implementation change.
- **Audit**: report gaps, contradictions, stale content, and duplicated facts.
- **ADR**: record one important, expensive-to-reverse, or disputed decision.
- **Progress**: append a meaningful progress entry and update milestone status.

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

When essential context is missing, ask one consolidated set of blocking
questions if interaction is available. Otherwise proceed with visible
assumptions and a `待确认问题` section.

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

### Existing repositories

- Describe what exists, not an idealized architecture.
- Call out divergence between implementation and intended design.
- Do not claim completion from an interface, stub, or empty module.
- Preserve valid user-written documentation and formatting.

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

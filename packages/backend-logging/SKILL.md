---
name: backend-logging
description: Implement, audit, or upgrade a production-ready logging system in any language or framework. Use when a project needs color-coded and column-aligned terminal logs, structured NDJSON logs, log levels, request or trace context, error serialization, redaction, or replacement of print and console statements.
metadata:
  author: xfrrn
  version: "1.1.0"
---
# Backend Logging

Build one structured event pipeline with two renderers:

- **Pretty Terminal** for local development and interactive tools.
- **NDJSON** for production, containers, collectors, and persistent diagnostics.

Application code emits one event. Format selection belongs in logger bootstrap,
never in business code.

Pretty Terminal quality is a primary acceptance criterion. For an interactive
TTY, color-coded levels, stable column alignment, Unicode-aware width handling,
and clean error rendering are required behavior rather than optional polish.

## Select the operation

- **Implement**: establish the first coherent logger.
- **Upgrade**: improve an existing logger without replacing sound infrastructure.
- **Audit**: report gaps without changing code unless requested.
- **Extend**: instrument one HTTP, worker, job, database, external-call, CLI, or desktop path.

Keep the requested scope. Do not turn logging work into a metrics, tracing,
dashboard, collector, or full observability migration unless explicitly asked.

## Inspect before choosing a stack

Read the smallest useful evidence set:

- manifests, lockfiles, runtime and framework versions;
- entry points and configuration loading;
- current logger dependencies, wrappers, middleware, and direct print calls;
- HTTP, worker, database, external-client, and final error boundaries;
- request IDs, tracing, async context, MDC, scopes, or equivalent propagation;
- `.env.example`, deployment/container files, and tests that capture logs;
- terminal targets, supported operating systems, and whether messages may contain CJK text.

Classify each target process as a service, worker, CLI, desktop/local runtime,
or reusable library. This determines defaults and sinks.

Choose the least disruptive implementation:

1. extend the capable logger already used;
2. otherwise use the ecosystem's standard structured logging API;
3. add one mature dependency only when needed for the contract;
4. write a small handler/formatter only when existing options are insufficient.

Never run two competing application logger stacks in parallel. Read
[references/language-adapters.md](references/language-adapters.md) for ecosystem
choices.

Do not accept a default Pretty formatter merely because it is built in. Inspect
its actual output. Replace or configure it when level colors, columns, Unicode
alignment, object rendering, error layout, or non-TTY behavior fail this Skill.

## Enforce one event contract

Read [references/logging-contract.md](references/logging-contract.md). The
canonical JSON shape starts with:

```json
{"ts":"2026-08-26T05:42:18.604Z","level":"info","msg":"Request completed"}
```

Important events also carry a stable `event` name and useful correlation data:

```json
{"ts":"2026-08-26T05:42:18.604Z","level":"info","msg":"Request completed","event":"http.request.completed","service":"api","logger":"http.access","request_id":"req_01K3N7VZ7HY5TQH6E4K4X8NFKG","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","ctx":{"method":"GET","route":"/v1/posts/:id","status":200,"duration_ms":38.4}}
```

Use the project's configuration system to provide equivalent controls:

```text
LOG_LEVEL=debug|info|warn|error
LOG_FORMAT=auto|pretty|json
LOG_COLOR=auto|always|never
LOG_PRETTY_MODE=auto|full|compact|minimal
```

Only `LOG_LEVEL` and `LOG_FORMAT` are mandatory when the project already has an
equivalent color and terminal-layout mechanism. Preserve existing variable names
when they provide the same semantics.

`LOG_FORMAT=auto` means Pretty only for an interactive TTY outside
production/staging; otherwise JSON. `LOG_COLOR=auto` enables color only for a
capable interactive terminal. Respect `NO_COLOR`, `FORCE_COLOR`, and
`TERM=dumb`. JSON never contains ANSI. Select the renderer once during
bootstrap.

## Implementation workflow

### 1. Map the current state

Identify logger initialization, direct print calls, duplicate access logs,
context sources, final error owners, high-value events, sensitive data at risk,
and current terminal formatting defects. In a large repository, migrate only
the requested paths and report the remaining gap.

For Pretty output, capture representative current lines and note:

- whether levels have distinct colors;
- whether time, level, scope, message, and context align vertically;
- whether ANSI escapes corrupt padding;
- whether Chinese or other wide characters shift later columns;
- whether objects and errors unexpectedly expand into many lines;
- whether redirected output still contains color codes.

### 2. Create one bootstrap boundary

Consolidate level filtering, format selection, color selection, timestamps,
service/environment/version fields, redaction, error normalization, and renderer
selection. Modules obtain named or child loggers from this boundary; avoid a
broad wrapper that merely duplicates the native API.

### 3. Bind correlation context

Use the runtime's native child/bound logger, async-local/context variable,
request scope, MDC, logging scope, span, or explicit context object. Attach
available `request_id`, `trace_id`, `span_id`, service, environment, version,
and logger/component name.

Do not introduce tracing only to manufacture trace fields. Test that context
survives relevant async boundaries and is cleared afterward.

### 4. Implement the Pretty Terminal renderer

Read [references/terminal-style.md](references/terminal-style.md) and
[assets/terminal-theme.json](assets/terminal-theme.json). The target shape is:

```text
13:42:18.604  INFO   http.access           Request completed               method=GET route=/v1/posts/:id status=200 duration=38.4ms request_id=req_...
13:42:20.087  WARN   db.query              Slow query                      operation=list_posts duration=842.7ms rows=24
13:42:21.311  ERROR  publisher.x           Publish failed                  account_id=acc_7 attempt=2
              ╰─ TimeoutError: upstream timed out after 10s
                 at publisher/client.ts:184
```

The following are non-negotiable for a color-capable interactive TTY:

- level labels have stable semantic colors: DEBUG cyan, INFO green, WARN yellow,
  ERROR/FATAL red;
- time, level, scope, message, and context appear in a fixed order;
- level, scope, and message columns use stable display widths;
- padding and truncation ignore ANSI and use Unicode terminal display width, not
  bytes or language string length;
- normal events occupy one physical line;
- context key order is deterministic;
- error details are indented and visually subordinate to the structured first
  line;
- `NO_COLOR` removes ANSI while preserving the same readable layout.

Use two ordinary spaces between columns. Do not use tabs, Emoji, banners,
per-event boxes, whole-line coloring, random scope colors, rainbow value types,
or multi-line object dumps.

A library default that produces uneven columns or weak color separation must be
configured or replaced with a focused formatter. Do not weaken the visual
contract to avoid a small renderer implementation.

Preview the reference theme when useful:

```bash
python packages/backend-logging/scripts/preview_terminal_theme.py --force-color
python packages/backend-logging/scripts/preview_terminal_theme.py --no-color
```

The preview script is a visual reference, not the target project's production
logger.

### 5. Implement the JSON renderer

Emit UTF-8 NDJSON: one compact JSON object per physical line. Use UTC RFC 3339
timestamps, lower-case levels, JSON-native values, no ANSI, and the same event
and context used by Pretty. Do not serialize `ctx` or `error` into JSON strings.

Services normally write to process streams and let the runtime handle
collection and rotation. Add rotating local JSON files only when a desktop or
local-runtime requirement explicitly needs persistent diagnostics.

### 6. Instrument ownership boundaries

Prefer outcome events over step-by-step narration. Add the relevant subset:

- service start and graceful shutdown;
- one HTTP completion event per request;
- job/task completion, retry exhaustion, and terminal failure;
- external-call failure and slow-call events;
- database failure and slow-query events without SQL parameters;
- meaningful authentication/authorization outcomes without credentials;
- important business outcomes needed to operate the system.

Do not log every function entry, loop item, successful query, or ordinary 4xx as
`warn`. Log an exception once at the boundary that owns retry, response,
termination, or recovery. Preserve the original control flow.

### 7. Redact centrally and document usage

Redact credential, session, cookie, token, secret, and private-key fields in the
logging pipeline. Request/response bodies, full query strings, PII, prompts,
document bodies, transcripts, and file contents are excluded by default.

Update the smallest appropriate existing configuration and README section with
format defaults, color behavior, levels, context usage, error usage, and
prohibited fields.

## Validate before completion

Read [references/quality-checklist.md](references/quality-checklist.md). Run the
project's relevant build, lint, type check, and tests. Add focused tests for:

- Pretty golden/snapshot output with all supported levels;
- fixed column positions after ANSI is stripped;
- distinct level-color SGR semantics in color mode;
- English, Chinese, and mixed-width alignment;
- long scope/message truncation with `…`;
- normal one-line events and indented error details;
- JSON parsing and canonical fields;
- `NO_COLOR`, `TERM=dumb`, and non-TTY behavior;
- redaction;
- error serialization;
- context propagation and cleanup;
- absence of duplicate final error/access logs.

Validate a captured JSON sample:

```bash
python packages/backend-logging/scripts/check_json_logs.py app.ndjson
```

Use `--require-event` when every captured record is expected to be an
operational event. The schema is available at `assets/log-event.schema.json`.

Do not report completion unless:

- Pretty and JSON share one event pipeline;
- color-capable TTY output visibly distinguishes levels;
- columns remain aligned after ANSI is removed and with mixed CJK/ASCII text;
- color-disabled Pretty remains clean and aligned;
- every JSON line parses independently and contains no ANSI;
- sensitive values are redacted;
- context propagation is verified;
- relevant project tests pass or failures are reported precisely.

## Report the result

State changed files, selected logger and rationale, Pretty/JSON selection,
terminal palette and column widths, canonical fields and redaction,
instrumented and intentionally omitted boundaries, validation commands, and
remaining migration gaps. Include one representative color-enabled Pretty
sample description, one no-color Pretty line, and one JSON event; do not paste
files already written to the workspace.

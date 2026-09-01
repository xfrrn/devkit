# Test Selection by Change and Risk

Use this reference when a change crosses multiple boundaries, has elevated
risk, or the correct test level is not obvious.

## Keep the dimensions separate

Test labels describe different dimensions and may overlap:

- **Level**: unit, component, integration, contract, end-to-end.
- **Purpose**: functional, acceptance, regression, smoke.
- **Quality attribute**: performance, security, reliability, compatibility,
  accessibility, or visual correctness.

A single API integration test can be functional, acceptance, and regression
evidence at the same time. Do not create separate suites merely to satisfy
every label.

## Selection matrix

| Change surface | Start with | Expand when |
|---|---|---|
| Pure calculation, parser, validation, state transition | Unit or table-driven behavior test | Shared utility, many consumers, or broad input contract changed |
| Bug fix | Regression test reproducing the reported root cause | Sibling callers share the fixed path |
| Refactor | Existing affected tests | Public shape, serialization, timing, or side effects may have changed |
| Public API, RPC, event, file format | Contract test plus focused producer/consumer behavior | Multiple consumers or backward compatibility matters |
| Database query or repository | Integration test against the project's isolated database setup | Transaction, locking, indexing, or cross-service behavior changed |
| Schema migration | Forward migration and data-invariant test | Project supports downgrade/rollback, mixed versions, or large existing datasets |
| External API client | Request construction, response mapping, timeout, rate-limit, and malformed-response tests | Configured sandbox exists or provider contract changed |
| Queue, worker, scheduler | Job behavior, retry, idempotency, and terminal failure | Delivery ordering, duplicate delivery, or broker integration changed |
| Concurrency, cache, clock, randomness | Deterministic race/expiry/invalidation tests at the narrowest useful boundary | Shared mutable state, throughput, or runtime race detection is relevant |
| CLI | Argument parsing, exit code, stdout/stderr, and filesystem effects | Packaging or cross-platform behavior changed |
| Backend startup or configuration | Config validation, build, and smoke startup | Deployment image, environment contract, or dependency wiring changed |
| UI component behavior | Component/functional test covering states and keyboard interaction | Routing, persistence, authentication, or backend boundaries are involved |
| Critical user journey | Existing E2E test or one focused journey | The change affects login, checkout, destructive actions, or primary workflows |
| Visual styling or responsive layout | Render and inspect affected states; use existing visual snapshots when trusted | Shared tokens, layouts, breakpoints, themes, or many screens changed |
| Authentication or authorization | Positive and negative permission cases at the real enforcement boundary | Roles, tenancy, session lifecycle, or policy storage changed |
| Money, quota, inventory, irreversible data | Invariant and failure-path tests plus affected integration suite | Rounding, retries, idempotency, concurrency, or reconciliation changed |
| Dependency or toolchain update | Build, affected tests, and smoke check | Runtime, generated output, lockfile resolution, or supported platforms changed |
| Documentation or comments only | No executable test by default | Examples compile/run, generated docs change, or docs are the product |

## Risk escalation

### Local and reversible

Run the focused behavior test and cheap affected checks. Examples include an
internal helper or isolated presentation change.

### Shared or boundary-facing

Run the focused test, affected package regression suite, and the relevant
contract or integration check. Include known consumers of a shared API or
utility.

### High risk

For authentication, money, migrations, destructive data, concurrency,
availability, or release paths, include the broader regression suite and
explicit failure/invariant coverage. Use a real sandbox only when the project
already provides one and the run is authorized.

## Regression scope

Regression is not automatically the full repository suite. Expand from the
changed behavior through actual dependency paths:

```text
changed behavior
  → direct tests
  → callers and consumers
  → module/package suite
  → boundary suites
  → full repository only when exposure or cost justifies it
```

A cheap full suite may be the simplest choice. An expensive suite should not
run merely because it exists; state when and why it was omitted.

## Specialized quality checks

Use these only when requirements or change risk activate them:

- **Performance**: a stated budget, observed regression, hot path, query/index
  change, or load-sensitive release. Prefer the existing benchmark harness.
- **Security**: changed trust boundary, identity, authorization, input parsing,
  secret handling, or dependency risk. Focus on the changed control; a broad
  security audit is a separate request.
- **Reliability**: retries, timeouts, failover, partial success, cancellation,
  resource cleanup, or recovery changed.
- **Compatibility**: supported runtime, browser, operating system, protocol,
  or stored-data version changed.
- **Accessibility**: interactive UI, semantics, focus order, keyboard access,
  labels, contrast, or motion changed. Use existing automated checks and
  inspect behavior that automation cannot prove.
- **Visual regression**: appearance is part of the acceptance criteria and a
  stable rendering environment exists. Review image differences rather than
  accepting snapshots automatically.

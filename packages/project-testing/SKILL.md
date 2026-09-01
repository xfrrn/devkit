---
name: project-testing
description: Run, add, diagnose, or audit the smallest relevant software tests for code changes and bug fixes. Use whenever implementing or modifying code and before reporting development work complete; adapt test levels and commands to the changed behavior, project stack, risk, and existing conventions. Do not use for read-only explanations or documentation-only edits unless testing is requested.
metadata:
  author: xfrrn
  version: "1.0.0"
---

# Project Testing

Prove changed behavior with the smallest relevant checks, then expand only
when the change's exposure or risk requires it. The repository's accepted
commands, requirements, and existing test conventions are authoritative.
Do not replace a capable test stack merely to standardize projects.

## Select the operation

- **Verify**: after an implementation change, run the relevant validation.
  This is the default during development work.
- **Add**: create or update focused tests for new behavior or a bug fix.
- **Diagnose**: explain a failing, flaky, hanging, or undiscovered test and
  fix it only when the user requested a fix.
- **Audit**: report coverage gaps, unsafe test dependencies, and missing
  quality gates without changing files unless requested.

A read-only request remains read-only. Running non-mutating diagnostics is
allowed when it supports the requested report.

## Inspect before selecting tests

Read the smallest useful evidence set:

- repository guidance, README, contribution docs, and any testing strategy;
- manifests, lockfiles, workspace definitions, test configuration, build
  wrappers, and CI workflows;
- the current diff, changed behavior, callers, consumers, and public
  boundaries affected by the change;
- nearby tests, fixtures, helpers, snapshots, and test-data conventions;
- required services, environment variables, containers, credentials, and
  whether the command can mutate external state.

Prefer commands explicitly defined by the project. If the repository does
not define a canonical command, or contains multiple ecosystems or a
monorepo, read [references/stack-adapters.md](references/stack-adapters.md).
Do not install dependencies before checking whether the existing runtime,
standard library, or installed test framework already covers the need.

## Classify the change

Classify both its surface and risk before choosing a test:

- **Surface**: pure logic, bug fix, refactor, API or event contract, database
  or migration, external integration, async or concurrent work, UI, CLI,
  configuration, build, dependency, or documentation.
- **Risk**: local and reversible; shared or boundary-facing; or high-risk
  behavior involving authentication, authorization, money, irreversible
  data, migrations, concurrency, availability, or release paths.

Use this minimum mapping:

| Change | Minimum useful evidence |
|---|---|
| Business logic or validation | Focused unit or functional test plus nearby regression tests |
| Bug fix | One regression test that reproduces the root cause, then the affected suite |
| Refactor without behavior change | Existing affected regression suite; add tests only for an observed gap |
| API, schema, or event contract | Focused behavior test plus contract and relevant integration tests |
| Database or migration | Isolated migration/integration test and data invariants |
| External service boundary | Client behavior, timeout/error mapping, and contract test; sandbox test only when configured |
| UI behavior | Component/functional test and critical-path E2E when the interaction crosses boundaries |
| Visual-only UI change | Existing visual regression or a rendered visual check; do not pretend unit tests prove appearance |
| Configuration, dependency, or startup | Relevant build/type check plus smoke test |
| Auth, money, concurrency, or destructive data path | Focused tests, affected integration tests, and the broader regression suite |

Read [references/test-selection.md](references/test-selection.md) when a
change crosses multiple surfaces, has elevated risk, or the appropriate test
level is unclear. For an ordinary local change with an obvious existing test,
do not load either reference unnecessarily.

## Run a risk-based test ladder

1. Run the narrowest test that directly proves the changed behavior.
2. Run the affected module or package suite when sibling behavior can regress
   or the suite is cheap.
3. Add contract, integration, migration, UI, or smoke checks when the change
   crosses the corresponding boundary.
4. Run the full repository suite for shared foundations, high-risk changes,
   release work, or when it is already a cheap project gate.

Run relevant formatting, lint, type, and build checks when configured, but
report them separately: they are quality gates, not substitutes for behavior
tests. Do not run every available suite after every small edit.

## Write tests that protect behavior

- Assert observable outcomes and stable contracts, not private implementation
  details.
- For a bug, place one regression test at the lowest stable boundary that
  reproduces the root cause. Confirm it fails before the fix when practical
  and safe, but never overwrite user work merely to demonstrate failure.
- Cover meaningful normal, boundary, and failure behavior introduced by the
  change. Do not create one test per line or speculative edge case.
- Reuse the project's fixtures and helpers. Add an abstraction only when it
  removes real repetition in the tests being written now.
- Keep tests deterministic: control time and randomness, isolate files and
  databases, and replace network boundaries with existing fakes or contract
  fixtures unless a real integration environment is explicitly intended.
- Use snapshots or golden files only for stable, reviewable output. Inspect
  updates; never refresh snapshots blindly to make a failure disappear.
- Follow existing coverage thresholds. Do not write meaningless tests solely
  to increase a percentage.

## Run tests safely

Default to local, isolated, synthetic test data. Do not send traffic to
production, shared accounts, paid APIs, or destructive migration targets
without explicit authorization. Never expose real secrets, tokens, cookies,
or personal data in commands, fixtures, logs, or reports.

Use project timeouts when available and avoid unbounded watch mode. A command
that discovers zero tests is not a passing run. A skipped, filtered, or
quarantined test remains unverified and must be reported.

## Diagnose failures honestly

- Start with the first root failure rather than editing every downstream
  symptom.
- Distinguish product defects, incorrect expectations, environment/setup
  failures, and flaky tests before changing code.
- Do not weaken assertions, delete tests, or alter expected output solely to
  obtain a green run.
- If flakiness is plausible, rerun the same failing test at most once to
  gather evidence. A pass on retry is a flaky signal, not proof of success.
- Separate failures caused by the current change from known or demonstrably
  pre-existing failures. Do not claim a baseline failure is fixed unless it
  was actually verified.

## Report the evidence

Before reporting development work complete, state:

- tests added or changed and the behavior they protect;
- exact commands run and their pass, fail, skip, or zero-test result;
- which test levels and affected areas were covered;
- relevant checks not run and why;
- failures, flaky evidence, environment blockers, and remaining risk.

Use **Passed**, **Failed**, or **Inconclusive** accurately. Never say "all
tests pass" when only a targeted subset ran.

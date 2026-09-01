# Test Stack Adapters

Use this reference only when the repository does not expose one clear test
command, or when work spans multiple languages, packages, or build systems.

## Choose the command source

Prefer evidence in this order:

1. repository and directory-level agent instructions;
2. documented developer commands and contribution guidance;
3. CI jobs that currently gate the affected code;
4. manifest scripts, build wrappers, workspace tasks, and test configuration;
5. the ecosystem's native command using already-installed tooling.

Do not introduce a new task runner or test framework simply to create a
uniform command. Preserve the repository's package manager, lockfile, runtime,
wrapper, test layout, feature flags, and environment conventions.

## Common ecosystems

| Evidence | Focused path | Broader path | Important adaptation |
|---|---|---|---|
| Node.js / TypeScript manifests and lockfile | Existing test script with the configured runner's file/name filter | Package or workspace test script | Use the lockfile's package manager; inspect script argument forwarding before appending filters |
| Python `pyproject.toml`, `tox.ini`, `noxfile.py`, `pytest.ini`, or existing `unittest` tests | Existing pytest node/file target or direct unittest module/file | Configured pytest/tox/nox task or unittest discovery | Use the project's environment manager; do not add pytest when stdlib unittest is the established stack |
| Go module/workspace | Changed package and focused `-run` selection when useful | Affected modules, then `go test ./...` when warranted | Run race detection for concurrency risk or existing gates, not every trivial edit |
| Rust Cargo workspace | Changed crate, module, or named test | Affected crate/workspace test command | Preserve feature flags, target selection, and workspace defaults used by CI |
| Java/Kotlin Gradle or Maven project | Wrapper task for the affected module/test | Module suite, then repository wrapper task | Prefer `gradlew`/`mvnw`; do not rely on a different globally installed version |
| .NET solution/project | Affected test project or configured filter | Relevant solution/workspace `dotnet test` | Preserve target framework, configuration, and existing runsettings |
| Ruby or PHP project | Existing Bundler/Composer-backed focused test command | Existing project suite | Use the locked dependency command and the framework already present |
| C/C++ CMake, CTest, Meson, or native build | Configured target/test in the existing build directory or preset | Project test target | Reuse presets and generated build directories; do not invent compiler flags |
| Swift/Xcode project | Affected scheme/test target | Relevant scheme or test plan | Use configured destinations; starting simulators or signing flows may require explicit setup |
| Web UI with component/E2E tooling | Affected component/spec | Existing UI package and critical E2E suites | Use the installed browser runner; do not add Playwright/Cypress or regenerate snapshots by default |
| Monorepo workspace | Existing affected-package command or changed package script | Workspace dependency-aware task, then full suite if needed | Respect package boundaries and cache tools; verify that an "affected" command did not select zero tests unexpectedly |

These are routing hints, not commands to copy blindly. Inspect the target
repository's scripts and tool help before choosing flags.

## Boundary adapters

### Databases and migrations

Use the project's existing ephemeral database, container, transaction, or
fixture setup. Verify data invariants and repeatability where applicable. Do
not point tests at a developer's shared or production database.

### External APIs

Default to existing fakes, recorded fixtures, local emulators, or contract
tests. Use a provider sandbox only when configuration and authorization are
explicit. Never use real credentials merely because they are present in the
environment.

### Browsers and user interfaces

Use component tests for local behavior and E2E only for meaningful journeys
that cross application boundaries. For visual work, render the affected
states and inspect screenshots or existing visual diffs. A DOM assertion does
not prove layout, contrast, clipping, or responsive behavior.

### Services, workers, and containers

Reuse documented local orchestration. Prefer a focused service or worker test
over starting the entire stack. If required services are unavailable, report
the integration result as inconclusive rather than silently substituting a
different environment.

## Interpret command results

Record the command, exit code, and test counts when available. Treat these as
inconclusive or failed evidence rather than success:

- zero tests discovered or every selected test filtered out;
- missing runtime, dependency, service, browser, or environment variable;
- watch mode waiting indefinitely;
- only snapshots updated without assertions being reviewed;
- a command that exercised a different package, target, or configuration than
  the changed code.

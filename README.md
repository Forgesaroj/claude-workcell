# Workcell

A coordinator and worker workflow for parallel software development. Workcell turns a broad request into scoped assignments, tracks each handoff, and requires independent verification before changes are integrated.

The included plugin adapter uses Claude Code's plugin format. The coordination protocol itself is designed to stay portable across agent runtimes.

## Why Workcell

Parallel coding agents can make progress faster when their tasks are independent. They can also create overlapping edits, duplicate work, unverified claims, and forgotten temporary resources. Workcell gives the coordinator a repeatable way to define ownership, measure results, and integrate only checked work.

## What is included

- **Coordinator skill** for scoping work, creating dispatches, checking results, and recording integration decisions.
- **Worker profile** for one bounded assignment and a reproducible handoff.
- **Dispatch template** covering baseline, allowed and excluded paths, controls, acceptance checks, and stop conditions.
- **Operating guide** defining roles, task states, evidence labels, and practical parallelization rules.
- **Example ledger** for tracking task IDs, owners, baselines, candidates, and coordinator results.

There is no daemon, database, API service, or background scheduler in this repository.

## Roles and workflow

- **Owner:** sets the outcome, constraints, protected behavior, and approval boundaries.
- **Coordinator:** checks the repository state, splits independent work, owns the ledger, verifies submissions, and integrates approved changes.
- **Worker:** completes one assignment within its file fence and returns evidence. It cannot expand its own scope or declare its work independently verified.

A task moves through:

`proposed → ready → running → submitted → verified → integrated → sealed`

A task can become `blocked` at any stage. Verified, integrated, and released are separate states.

## How work is divided

A dispatch should name the exact baseline commit, one outcome, one owner, allowed and excluded paths, dependencies, a baseline measurement, acceptance checks, and stop conditions. Concurrent workers should own different files or use isolated worktrees. Dependent work stays sequential.

The coordinator checks the candidate commit itself, confirms the regression case and valid-neighbor controls, records failures and skipped checks honestly, and rechecks the combined result after integration. See [the operating model](plugins/workcell/docs/operating-model.md) and [the dispatch template](plugins/workcell/templates/dispatch.md).

## Validate a dispatch packet

Before handing work to a worker, copy the [dispatch template](plugins/workcell/templates/dispatch.md), fill it in, and check its structure:

```sh
python3 scripts/validate_dispatch.py .workcell/dispatches/WC-014.md
```

The [completed example](examples/dispatch.valid.md) shows the expected fields. The validator checks packet completeness, including the baseline SHA, file fence, acceptance evidence, and unresolved placeholders. It does not enforce permissions or approval boundaries; those must be enforced by the host runtime and repository settings.

Run the unit tests with `python3 -m unittest discover -s tests -v`. GitHub Actions runs both checks on pushes and pull requests.

## Install

From a Claude Code terminal, register this repository as a marketplace and install the plugin:

```sh
claude plugin marketplace add Forgesaroj/claude-workcell
claude plugin install workcell@workcell-marketplace
```

Start a new session and invoke the coordinator skill:

```text
/workcell:workcell Coordinate an audit of the import pipeline. Keep it read-only. Split independent areas among workers, record the baseline and file fences, then return a prioritized report. Do not change code or GitHub issues.
```

To load the plugin directly while developing it:

```sh
claude --plugin-dir ./plugins/workcell
```

The plugin uses the orchestration features available in the active session. Where multi-session teams are unavailable, it can produce dispatch packets for sessions started separately.

For a project-local ledger, copy `plugins/workcell/.workcell.example/` into the target project as `.workcell/`. Edit the owner, protected paths, approval policy, and test commands before using it.

## Session and automation limits

The plugin does not open or wake a closed terminal tab. Session creation, resumption, and scheduling depend on the host runtime. In Claude Code, Agent Teams can coordinate teammates from an interactive lead session; the feature is experimental and has documented limitations. Read [runtime compatibility](plugins/workcell/docs/runtime-compatibility.md) before enabling it.

Starting work when no session is running requires a separate runner with authentication, persistent job state, cancellation, retries, observability, budget limits, workspace isolation, and an approval policy. That is outside the current project.

## Safety

- Prompt instructions guide behavior; they are not a security boundary.
- Enforce access with host permissions, protected branches, least-privilege credentials, and isolated worktrees.
- Workers do not merge, push, publish, or delete resources unless the owner authorizes that action.
- Never put credentials, customer data, or private project instructions in public task packets.
- Report cleanup targets by exact name. Do not automatically delete databases or worktrees.

Review the plugin before installing it. Components run with the permissions of the installing user.

## Current status

Workcell is an early, prompt-driven coordination kit. The repository includes workflow instructions and templates; it does not include a tested unattended orchestration runtime. Validate the plugin in a disposable project before using it on important code.

## Repository details

**Description:** Coordinator-worker workflow for parallel software development, with scoped tasks and evidence-based verification.

**Suggested GitHub topics:** `agent-orchestration`, `multi-agent`, `coding-agents`, `developer-tools`, `software-development`, `workflows`

The GitHub About description and topics are repository settings; this section provides the values to use there.

## Contributing

See [CONTRIBUTING.md](plugins/workcell/CONTRIBUTING.md). File focused issues with reproduction steps and expected behavior. Do not submit private project data or copied proprietary source.

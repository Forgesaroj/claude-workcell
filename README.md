# Workcell

A reusable coordinator and worker workflow for session-based software development agents. The included plugin adapter targets Claude Code; the task protocol is kept portable.

Workcell turns a large engineering request into bounded work packets, assigns independent workers, and requires a coordinator to verify and integrate their results. It is designed for teams that want parallel progress without losing ownership of scope, evidence, or shared project state.

> Workcell is an independent community project. It is not affiliated with or endorsed by Anthropic.

## What it does

- Defines a coordinator and worker workflow for Claude Code.
- Creates explicit task packets with a baseline, file fence, dependencies, stop conditions, and acceptance checks.
- Encourages isolated worktrees and disjoint ownership to reduce collisions.
- Requires workers to report evidence, verification results, changed paths, and a commit or handoff point.
- Requires the coordinator to independently verify work before integration and closure.
- Records task state in project files so a fresh session can recover progress.

## What it does not do

The plugin does not run a daemon, secretly control Claude, or wake a closed Claude Code session. Skills provide reusable instructions; they only run when Claude Code loads or invokes them. Claude Code Agent Teams can start teammates from an interactive lead session, but Agent Teams are experimental, disabled by default, and have documented limitations around resumption, task coordination, and shutdown. See [runtime compatibility](plugins/workcell/docs/runtime-compatibility.md).

If you need work to start while no Claude session is running, you need a separate scheduler or runner that launches Claude Code or the Agent SDK, plus credentials, resource limits, and an approval policy. That automation is intentionally outside this starter plugin.

## Install

In a Claude Code shell, add this public repository as a marketplace, substituting its owner and repository name:

```sh
claude plugin marketplace add <owner>/<repository>
claude plugin install workcell@workcell-marketplace
```

Start a new session and run:

```text
/workcell:workcell Coordinate an audit of the import pipeline. Keep the audit read-only. Split independent areas among workers, record the baseline and fences, then return a prioritized report. Do not change code or GitHub issues.
```

For local development before publishing:

```sh
claude --plugin-dir ./plugins/workcell
```

The plugin uses the current session's available orchestration tools. Without Agent Teams, it falls back to focused subagents or produces worker packets for sessions you start yourself.

## Local project state

Copy `plugins/workcell/.workcell.example/` to `.workcell/` in the project where you use the plugin. Edit the owner, protected paths, approval policy, and test commands before assigning work.

```text
.workcell/
  README.md             # local rules, owner, protected operations
  ledger.md             # task IDs, state, worker, baseline, integration result
  dispatches/           # immutable worker task packets
  reports/              # worker handoffs and coordinator verification
```

See [the operating model](plugins/workcell/docs/operating-model.md) and [the dispatch template](plugins/workcell/templates/dispatch.md).

## Safety defaults

- Workers do not merge, push, publish, alter task state, or broaden their own file fence.
- Use separate worktrees or branches for concurrent edits.
- The coordinator verifies the exact candidate commit; a worker's claim is not proof.
- Any unexpected overlap, destructive operation, sensitive data, or accounting/security invariant breach stops the task for owner review.
- Cleanup reports resources by exact name. Automated cleanup must not delete databases or worktrees without an explicit owner action.
- Never put credentials, customer data, or private project instructions in public task packets.
- Prompt instructions are not a security boundary. Enforce access with Claude Code permissions, protected branches, least-privilege credentials, and isolated worktrees.

## Compatibility and maturity

This is an initial, prompt-driven coordination kit, not a tested autonomous orchestration runtime. It does not claim that arbitrary projects can safely run unattended. Validate it on a disposable repository before applying it to production code.

## Contributing

See [contributing](plugins/workcell/CONTRIBUTING.md). File focused issues with reproduction steps and expected behavior. Avoid submitting private project data or copied proprietary content.

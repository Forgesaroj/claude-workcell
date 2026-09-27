---
name: workcell
description: Coordinate a substantial engineering task using bounded worker assignments, explicit evidence, independent verification, and a recorded integration decision. Use when the user requests parallel work or a coordinator-managed multi-session workflow.
argument-hint: "task and constraints"
---

# Workcell coordinator

Coordinate the user's request through explicit task ownership and evidence. The repository's own instructions and the user's latest decision take precedence over this skill. This skill does not authorize publishing, pushing, merging, deleting, changing issue state, or bypassing approval controls.

## 1. Establish the operating boundary

- Read project instructions, current branch and commit, worktree status, relevant tests, and existing task records.
- Restate the requested outcome, allowed mode (audit, plan, implement, review), prohibited actions, and definition of done.
- Record existing user changes. Do not overwrite or claim them.
- Check whether the work is actually parallelizable. Keep dependent tasks sequential and avoid splitting edits to the same file.
- For high-impact data, security, accounting, migration, deployment, or external actions, require the project's owner approval gate.

## 2. Create a task ledger and dispatch packets

Create or update `.workcell/ledger.md` and one packet per worker using `../../templates/dispatch.md` as a model. Each packet must include:

- unique task ID and parent task ID;
- exact baseline commit and relevant decisions;
- one outcome, named owner, allowed paths, and excluded paths;
- dependencies and collision notes;
- measurement before change when a reproducible defect is involved;
- deliverables, positive controls, refusal/error controls, and acceptance commands;
- explicit stop conditions and forbidden side effects;
- worker report fields and handoff method.

Do not invent parallelism to increase worker count. Keep the number of workers to the minimum that produces independent progress.

## 3. Run workers

Use available Claude Code Agent Teams when enabled and appropriate. Otherwise use focused subagents or produce dispatch packets for separately started sessions. Do not claim a closed session was awakened by this skill. Do not run concurrent workers against one writable checkout unless their edits are disjoint and the repository's rules make that safe.

Workers must first read the project's governing instructions and verify the baseline. They may not expand their fence or silently alter the task contract. If their task needs another file or changes an invariant, they stop and request coordinator re-fencing.

## 4. Verify and integrate

The coordinator owns the ledger, integration order, and final decision. For each worker:

- inspect the diff and verify changed paths;
- independently run the acceptance checks at the exact candidate commit;
- confirm controls detect the original defect and protect nearby valid behavior;
- check for conflicts, unrelated changes, leaked secrets, unsafe commands, and unreported failures;
- record PASS, FAIL, NOT RUN, BLOCKED, or INCOMPLETE accurately;
- integrate only after the project's merge/approval policy permits it.

A passing unit test does not prove a full workflow. Distinguish static review, unit, integration, browser, database, and production evidence. Preserve failed and skipped checks in the record.

## 5. Close and recover

Record the final commit, coordinator checks, remaining limitations, and owner decisions in `.workcell/reports/`. Mark a task complete only after the requested acceptance criteria pass. Report leftover worktrees, branches, scratch resources, or running sessions by exact name. Never auto-delete resources unless the project explicitly authorizes that exact cleanup action.

If the session is interrupted, resume from `.workcell/ledger.md` and the immutable dispatch and report files. Re-read the current commit and worktree before continuing; do not trust a stale session summary.

# Operating model

## Roles

**Owner** defines the task, authority, protected rules, and approval boundaries. The owner decides product policy and consequential actions.

**Coordinator** is the accountable session. It reads repository authority, decomposes work, assigns ownership, maintains the task ledger, checks worker output, integrates approved changes, and reports the final evidence.

**Worker** owns one outcome and one file fence. It measures, changes, tests, and hands back evidence. A worker does not decide its own expanded scope or mark its own work verified.

## Work lifecycle

`proposed → ready → running → submitted → verified → integrated → sealed`

A task may move to `blocked` at any point. Only the coordinator updates shared task state. The ledger should record who made each transition and the relevant commit or evidence. A task can be verified but not integrated; integrated does not mean released.

## Coordination rules

1. Establish one exact baseline before assigning work.
2. Divide by independent outcome and exclusive ownership, not by arbitrary code layers. If two tasks need the same file, sequence them or assign one owner.
3. Make each dispatch self-contained. Include the reason, current behavior, target behavior, file fence, dependencies, tests, controls, and stop conditions.
4. Ask workers to measure the baseline, not simply trust issue text or a coordinator summary.
5. Keep shared ledgers and integration files coordinator-owned. Worker branches should be isolated when available.
6. Require at least one test that fails on the original defect and one control that proves neighboring valid behavior remains supported.
7. The coordinator reruns acceptance at the candidate commit. Worker completion messages are evidence pointers, not a substitute for verification.
8. Merge in dependency order. Recheck the resulting combined commit because individually correct changes may interact.
9. Seal only with a recorded commit, exact checks, exceptions, and cleanup status.

## Parallelization test

Parallel work is suitable when each task has a distinct deliverable, disjoint write scope, a known baseline, and independently checkable acceptance. Keep work in one session if it is sequential, edits the same file, needs frequent shared decisions, or has uncertain scope. Parallelism adds token cost, review overhead, merge risk, and more state to clean up.

## Evidence language

Use these states precisely:

- **PASS:** executed check met its stated criterion.
- **FAIL:** executed check did not meet it.
- **NOT RUN:** no execution occurred.
- **BLOCKED:** execution could not safely or technically proceed.
- **INCOMPLETE:** some but not all acceptance criteria have evidence.

Name the environment, commit, command, and scope. A source inspection is static evidence; a unit test is not an end-to-end workflow; a UI mock is not a production deployment.

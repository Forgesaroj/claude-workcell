# Dispatch: <task-id> — <short outcome>

- Parent task:
- Worker:
- State: proposed | ready | running | blocked | submitted | verified | integrated | sealed
- Created by:
- Baseline commit:
- Branch/worktree:

## Outcome
One checkable user or engineering outcome.

## Authority and constraints
- User-approved mode:
- Governing project instructions / decisions:
- Protected behavior and data:
- Actions requiring owner approval:

## Scope fence
- Allowed paths:
- Excluded paths:
- Dependencies:
- Known concurrent owners / collision risks:

## Baseline measurement
- Starting state and reproduction:
- Current result:
- Evidence and limits:

## Deliverables
1. 

## Acceptance
- [ ] Defect-detecting positive case:
- [ ] Valid-neighbor control:
- [ ] Refusal/error/rollback case:
- [ ] Exact commands and expected outcomes:
- [ ] Coordinator's independent check:

## Stop conditions
Stop without widening scope if a required path is excluded, the baseline differs, a safety invariant is at risk, or an approval-gated action becomes necessary. Report what blocked the task.

## Worker handoff
- Summary:
- Changed paths:
- Candidate commit / patch:
- Checks: PASS / FAIL / NOT RUN / BLOCKED / INCOMPLETE
- Risks and unverified areas:
- Cleanup resources by exact name:

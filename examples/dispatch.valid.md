# Dispatch: WC-014 — Add request timeout coverage

- Parent task: WC-010
- Worker: runtime-tests
- State: ready
- Created by: coordinator
- Baseline commit: 4b825dc642cb6eb9a060e54bf8d69288fbee4904
- Branch/worktree: worktrees/wc-014

## Outcome
Add regression coverage proving timed-out requests return a clear error without leaking a worker process.

## Authority and constraints
- User-approved mode: implementation and local test execution
- Governing project instructions / decisions: repository CONTRIBUTING.md
- Protected behavior and data: public response schema
- Actions requiring owner approval: changes to package dependencies

## Scope fence
- Allowed paths: tests/runtime/**
- Excluded paths: src/api/**, package manifests
- Dependencies: WC-012 merged
- Known concurrent owners / collision risks: no other worker owns tests/runtime/**

## Baseline measurement
- Starting state and reproduction: timeout regression is not covered
- Current result: existing runtime test suite passes
- Evidence and limits: `python3 -m unittest discover -s tests -v`; this does not cover production traffic

## Deliverables
1. Add regression test for timeout response and worker cleanup.

## Acceptance
- [x] Defect-detecting positive case: regression test fails before the fix and passes after it
- [ ] Valid-neighbor control: verify a request under the timeout still succeeds
- [ ] Refusal/error/rollback case: verify malformed timeout settings fail clearly
- [ ] Exact commands and expected outcomes: `python3 -m unittest discover -s tests -v` exits 0
- [ ] Coordinator's independent check: coordinator reruns the suite on the candidate commit

## Stop conditions
Stop without widening scope if the baseline differs, a protected path needs changes, or dependency work is required. Report the blocker.

## Worker handoff
- Summary: add regression coverage for timeout cleanup
- Changed paths: tests/runtime/test_timeout.py
- Candidate commit / patch: pending
- Checks: NOT RUN
- Risks and unverified areas: production traffic behavior is not covered
- Cleanup resources by exact name: none

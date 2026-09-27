# Claude Code compatibility and session boundaries

Workcell is a prompt-and-files protocol packaged as a Claude Code plugin. It does not itself create operating-system processes or reach into another terminal tab.

Claude Code currently offers several distinct mechanisms:

- **Skills** package reusable instructions and can be invoked by name.
- **Subagents** work in a single session with a separate context and report back to the caller.
- **Agent Teams** coordinate multiple Claude Code instances with a lead, shared task list, and messaging. The lead must be an interactive session, and this feature is experimental and disabled by default.
- **CLI resume** continues a session using Claude Code's supported command-line interface. It is not a general-purpose external wake-up API.

The project protocol is designed to sit above these mechanisms. It uses dispatch files, task IDs, explicit file ownership, verification records, and handoff reports to keep work understandable if a session stops or context is compacted.

Before enabling Agent Teams in a real project:

1. Check the current official documentation and installed Claude Code version.
2. Read the documented limitations for resumption, shutdown, and task coordination.
3. Enable the experimental environment setting only if the project owner accepts the feature and its cost.
4. Try a disposable repository with two non-overlapping tasks, a deliberate worker interruption, a verification failure, and a coordinator restart.
5. Keep secrets and production credentials out of worker contexts unless required and approved.

For unattended scheduling, build and evaluate a separate runner using a supported runtime (such as the Agent SDK or a carefully constrained CLI invocation). It needs authentication, job persistence, cancellation, retries, observability, budget/time limits, workspace isolation, permission controls, and owner approval for consequential actions. Do not treat a skill, hook, or task ledger as a scheduler.


## Security boundary

The coordinator and worker prompts are process guidance, not enforcement. They cannot guarantee a worker stays within a file fence or prevent a shell command from reaching other paths. Use Claude Code permission controls, branch protection, least-privilege credentials, and isolated worktrees for enforcement. Keep secrets out of prompts and task records unless access is necessary and authorized. Review plugin code before installation because plugins execute with the installing user’s privileges.

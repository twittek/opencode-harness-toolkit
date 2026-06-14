# Self-Verification Policy

This policy defines how agents must verify their own work before reporting completion.

The goal is to prevent premature completion claims and to ensure that the final result matches the user's original request.

## Core rule

Every task must end with a self-verification pass before the final response.

Do not report completion until the result has been checked against the original requirement.

## Required verification questions

Before the final response, answer these questions internally and reflect the relevant outcome in the response:

```text
1. Requirement match
   Did the result satisfy the user's original request?

2. Scope control
   Did I modify only the intended files or content?

3. Policy compliance
   Did I follow AGENTS.md and relevant harness policies?

4. Checks and tests
   Did I run available checks, tests or validation steps?
   If not, did I explain why they were not run?

5. Side effects
   Did I avoid unintended changes, generated noise, secret exposure or unsafe actions?

6. Remaining risks
   Are there assumptions, incomplete areas or open risks the user should know about?

7. Final response honesty
   Is the final response clear about what was changed, what was verified and what remains uncertain?
```

## Verification output

For implementation, file editing or harness changes, include a concise verification summary in the final response.

Recommended format:

```text
Verification:
- Requirement match: ...
- Files changed: ...
- Checks run: ...
- Open risks: ...
```

Keep the summary short unless the user asks for details.

## What counts as verification

Verification may include:

```text
- reading the changed files again
- checking the generated structure
- running syntax checks
- running tests
- running linters
- running smoke tests
- comparing the result to the stated acceptance criteria
- checking that no unrelated files were changed
- checking that generated artifacts are linked correctly
```

Use the strongest available verification that is reasonable for the task.

## When checks are unavailable

If no automated checks are available, explicitly say that only manual/structural verification was performed.

Example:

```text
Checks run: no automated test script was available; verified changed files and required sections manually.
```

Do not invent test results.

## Requirement traceability

For non-trivial work, map the result back to the request.

Example:

```text
User request:
- add self-verification behavior

Implemented:
- self-verification-policy.md
- AGENTS.md rule
- lifecycle command guidance
- README documentation
```

## Failure handling

If self-verification finds a mismatch:

```text
1. Fix it before reporting completion when possible.
2. If fixing is not possible, report the mismatch clearly.
3. Do not claim the task is complete.
```

## Prohibited behavior

Agents must not:

```text
- claim success without checking the result
- hide failed checks
- silently skip relevant validation
- report tests as passed when they were not run
- ignore scope drift
- modify unrelated files without calling it out
```

## Lifecycle command behavior

### /harness-init

After generating the harness, verify:

```text
- required files exist
- OpenCode config shape is valid
- lifecycle commands are registered
- policies are present
- no forbidden OpenCode config keys are introduced
- generated guidance matches the interview input
```

### /harness-check

After producing findings, verify:

```text
- findings are evidence-based
- severity is justified
- no stale or unrelated artifacts were treated as active context
- recommendations are actionable
```

### /harness-update

After applying updates, verify:

```text
- active findings were addressed
- modified files are consistent with each other
- changelog/version information is updated when required
- checks or structural validation were run
```

### /harness-retro

After collecting feedback, verify:

```text
- feedback was captured without over-interpreting
- findings distinguish facts from suggestions
- follow-up actions are clear
```

### /harness-mcp

After MCP planning or config changes, verify:

```text
- risk category is documented
- approval state is clear
- no MCP server is installed or configured without approval
- rollback guidance exists for applied changes
```

## Final response rule

Final responses should be concise but must not omit important verification status.

Prefer:

```text
Done. I changed X and verified Y. Remaining risk: Z.
```

Avoid:

```text
Done.
```

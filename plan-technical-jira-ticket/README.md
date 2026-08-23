# plan-technical-jira-ticket

Turns a single, well-scoped technical Jira ticket (tech debt, a refactor, a performance fix, a
config or infra change) into an implementation plan grounded in the codebase(s) it touches, not a
restatement of the ticket in different words. It fetches the ticket plus everything that might
carry context the ticket body lacks: linked issues, remote links, attachments, a parent epic. It
checks the ticket's claims, and the local checkout's freshness, against real code instead of trust
in either at face value. Then it recaps its understanding once, in a single gate, before it spends
any effort on exploration. The scope is deliberately narrow. It surfaces rather than plans epics,
bug reports, and multi-integration feature tickets, because each of those needs a different
process from "plan one well-defined technical change".

Files:
- `SKILL.md` — the whole flow (resolve and classify, gather context, understand, recap, ground in
  code, write the plan, hand off). A single file. Nothing here is one-time or opt-in the way
  `next-improvement`'s companion files are, so there is nothing to separate. Every step runs on
  every ticket.

## Cost

This is a heavier skill, not a quick lookup. It fetches the ticket plus its linked issues, remote
docs, and parent epic, then explores and checks claims against real code in every repo confirmed
in scope (Step 5). Expect noticeably more tool calls and tokens than a single-shot question, in
exchange for a plan grounded in the current codebase rather than a restated ticket. The skill
itself surfaces this to the user before Step 1 starts.

## What it writes

**No files in your project.** The plan lives in the conversation (or in Claude Code's plan file,
which the harness manages, not this skill).

- **A comment on the Jira ticket**, offered once you approve the plan. This leaves your machine
  and is visible to anyone with access to the ticket. It is the preferred next step, not a
  mandatory one. A plan that exists only in the conversation is gone when the session ends. One
  on the ticket survives for whoever takes it next. The skill confirms the content with you
  before it posts, and never posts automatically because a plan now exists.

If you would rather go straight to implementation, that is fine and the comment is skipped. Code
the plan produces is ordinary work in your repo. This skill stops at an approved plan and does not
change how you write code after that.

## Requires

- **A Jira MCP server, configured and authenticated** — a hard dependency. Every step from ticket
  resolution onward relies on Jira MCP tools (`getJiraIssue`, `search`,
  `getJiraIssueRemoteIssueLinks`, and so on). Without one, the skill can only say so and point at
  whatever MCP setup docs exist in the environment (for example an `atlassian-mcp` skill, if
  installed). Configure this before you expect this skill to trigger usefully.
- **git**, in whatever repo(s) the skill explores — a soft dependency. Used for the
  checkout-freshness and existing-work checks in Step 5. If git is missing, the directory is not
  a git repo, or no remote is configured, the skill notes that limitation in the plan rather than
  a failure.
- **Claude Code's plan mode** — optional. Used for the approval flow in Step 6 if available.
  Otherwise the skill presents the plan inline and waits for a go-ahead.

## When it triggers

Claude reaches for this skill when you give it a ticket number and ask it to plan, scope,
decompose, or find the approach for that kind of technical work:

- "Plan out SD-4821, it's the tech debt ticket about the old retry logic."
- "What would it take to do PROJ-456?"
- Pasting a Jira URL and asking what the change actually involves.

## Example: straightforward run

```
You: Plan out SD-4821, it's a tech debt ticket about the old retry logic.

Claude: [fetches SD-4821, checks status/assignee (To Do, unassigned) and links
         (none blocking), confirms it's tech debt rather than a bug or feature,
         pulls a linked Confluence doc for design detail]
        Here's what I'm taking this ticket to mean: replace the manual retry loop
        in the sync job with the shared retry helper the rest of the codebase uses.
        Looks scoped to just this repo — right so far?

You: Yes, that's right.

Claude: [confirms the local checkout is current, checks for any branch already
         referencing SD-4821 (none), explores the sync job and how the shared
         retry helper is used elsewhere]
        Plan: replace the loop in sync_job.py with RetryHelper (same pattern as
        export_job.py), add a unit test for the backoff behaviour, verify against
        the existing integration tests. Covers both acceptance criteria on the
        ticket. Want me to go ahead?

You: Approved, go ahead.

Claude: [implements per the plan]
```

## Example: a scope gate firing

```
You: Can you plan JIRA-991?

Claude: [fetches JIRA-991] This reads as a bug report — it describes users seeing
        stale cached data, not a known change to make. Want a bug-investigation
        process instead, or is the root cause already known, in which case this
        is really just "invalidate the cache on write"?

You: Root cause is known, just implement the cache invalidation.

Claude: [proceeds with a plan scoped to that specific, already-diagnosed change]
```

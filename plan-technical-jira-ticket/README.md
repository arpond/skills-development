# plan-technical-jira-ticket

Turns a single, well-scoped technical Jira ticket (tech debt, a refactor, a performance fix, a
config/infra change) into an implementation plan grounded in the actual codebase(s) it touches,
rather than just restating the ticket in different words. It fetches the ticket plus everything
that might carry context the ticket body doesn't — linked issues, remote links, attachments, a
parent epic — verifies the ticket's claims (and the local checkout's freshness) against real code
rather than trusting either at face value, and recaps its understanding once in a single gate
before spending any effort exploring. Deliberately narrow in scope: it surfaces rather than plans
epics, bug reports, and multi-integration feature tickets, since each of those needs a different
process than "plan one well-defined technical change."

Files:
- `SKILL.md` — the whole flow (resolve/classify, gather context,
  understand, recap, ground in code, write the plan, hand off). Single file — nothing here is
  one-time or opt-in the way `next-improvement`'s companion files are, so there's nothing to split
  out; every step runs on every ticket.

## Cost

This is a heavier-weight skill, not a quick lookup — it fetches the ticket plus its linked
issues/remote docs/parent epic, then explores and verifies claims against real code in every repo
confirmed in scope (Step 5). Expect noticeably more tool calls and tokens than a single-shot
question, in exchange for a plan actually grounded in the current codebase rather than a restated
ticket. The skill itself surfaces this to the user before Step 1 starts.

## What it writes

**No files in your project.** The plan lives in the conversation (or in Claude Code's plan file,
which the harness manages, not this skill).

- **A comment on the Jira ticket**, offered once the plan is approved — this leaves your machine
  and is visible to anyone with access to the ticket. It's the preferred next step rather than a
  mandatory one: a plan that only exists in the conversation is gone when the session ends, while
  one on the ticket survives for whoever picks it up. The content is confirmed with you before
  posting, never posted automatically just because a plan now exists.

If you'd rather go straight to implementing, that's fine and the comment is skipped. Code the plan
produces is ordinary work in your repo — this skill stops at an approved plan and doesn't change
how code gets written after that.

## Requires

- **A Jira MCP server, configured and authenticated** — this is a hard dependency. Every step
  from resolving the ticket onward relies on Jira MCP tools (`getJiraIssue`, `search`,
  `getJiraIssueRemoteIssueLinks`, and so on); without one, the skill can't do anything beyond
  saying so and pointing at whatever MCP setup docs exist in the environment (e.g. an
  `atlassian-mcp` skill, if installed). Set this up before expecting this skill to trigger
  usefully.
- **git**, in whatever repo(s) get explored — soft dependency. Used for the checkout-freshness and
  existing-work checks in Step 5. If it's missing, not a git repo, or has no remote configured,
  the skill notes that limitation in the plan rather than failing outright.
- **Claude Code's plan mode** — optional. Used for the approval flow in Step 6 if available;
  falls back to presenting the plan inline and waiting for a go-ahead otherwise.

## When it triggers

Claude reaches for this skill when you give it a ticket number and ask it to plan, scope, break
down, or figure out the approach for that kind of technical work:

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

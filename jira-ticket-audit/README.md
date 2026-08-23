# jira-ticket-audit

Audits a single Jira ticket for ambiguity, internal inconsistency, gaps (missing acceptance
criteria, edge cases, non-functional detail), oversized or over-complex scope, and missing links to
sibling tickets in its epic. It fetches the ticket and its surrounding context (comments, linked
issues, parent epic, epic siblings) through the Jira MCP tools and reports per-dimension findings
with evidence quoted from the ticket. This is a review of the ticket's writing and scope, not of
the codebase it describes.

Complements [`plan-technical-jira-ticket`](../plan-technical-jira-ticket/README.md). This skill
judges whether a ticket is *fit to hand to an engineer* before anyone starts. That skill takes a
ticket already judged sound and grounds an implementation plan in the codebase.

Files:
- `SKILL.md` — the whole flow (resolve, gather context, assess five dimensions, report). Every
  step runs on every audit. Nothing here is one-time or opt-in.
- `references/stage-expectations.md` — a per-Jira-project lookup of what a ticket realistically
  contains at its current workflow stage. It stops the skill from reporting administrative
  placeholders (a blank "Codebases" field, an unresolved "should this pass UAT?" flag) as gaps
  before a team's own process would normally resolve them. It grows over time: the skill asks
  once per new project key it meets and offers to append the answer here.

## Cost

Lighter than `plan-technical-jira-ticket`: no codebase exploration, no checkout-freshness checks.
It still fetches the ticket plus its comments, linked issues, parent epic, and epic siblings
(through a JQL query). Expect a handful of Jira MCP calls per audit, not a single lookup.

## What it writes

**By default, nothing.** The skill answers a single-ticket audit in the conversation. Both writes
below happen only if you ask, or if you audit several tickets at once. The skill shows each in
full and waits for confirmation before it writes.

- **`TICKET-AUDIT-<KEY>.md`** — a report file, in the directory where the skill runs.
- **A comment on the Jira ticket itself** — this one leaves your machine and is visible to anyone
  with access to the ticket. The skill asks which you want (file, comment, or both) rather than
  an assumption.

It reads far more than it writes: the ticket, its comments, linked issues, the parent epic and its
siblings. On a later audit of the same ticket it looks for a prior report in *both* places above.
A search of only one could miss findings already reached and derive them again.

The skill also carries `references/stage-expectations.md` inside its own folder. It may update
that file with per-project workflow conventions it learns. That is inside the installed skill, not
your project.

## Requires

- **A Jira MCP server, configured and authenticated** — a hard dependency. Every step relies on
  Jira MCP tools (`getJiraIssue`, `search`, `searchJiraIssuesUsingJql`,
  `getJiraIssueRemoteIssueLinks`, and, only if the skill posts a report to the ticket,
  `addCommentToJiraIssue`). Without one, the skill can only say so and point at whatever MCP
  setup docs exist in the environment (for example an `atlassian-mcp` skill, if installed).

## When it triggers

Claude reaches for this skill when asked to audit, review, or sanity-check a ticket's own content,
as opposed to a plan for its implementation:

- "Audit SD-1234 before we pick it up."
- "Does this ticket make sense? Check it for gaps."
- "Is PROJ-456 ready to work on?"

## Example

```
You: Audit SD-2210 before we hand it to someone.

Claude: [fetches SD-2210, its comments, parent epic SD-2200, and SD-2200's other
         children]
        Ambiguity: issues found — the description says "improve error handling"
        without saying which errors or what the improved behavior should be.
        Inconsistency: none found.
        Gaps: issues found — AC covers the success path only; the description
        itself mentions a timeout case that has no corresponding AC.
        Complexity: right-sized.
        Epic linkage: missing link — SD-2214 (a sibling under SD-2200) touches
        the same retry config and isn't cross-referenced from either ticket.

        Want me to write this up as a report, or is the conversational summary
        enough?
```

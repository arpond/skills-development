---
name: commit-message-check
description: Mandatory pre-commit gate for any git commit message drafted on Andrew Pond's behalf, in any repo. Loads the live rules from the user's global CLAUDE.md and walks through a literal checklist — ticket-key prefix, subject mood/length, whether a body is even needed, a strip-test on every body bullet, and a scan for AI-authorship references — before the message is ever shown to the user or passed to `git commit`. Invoke this every time a commit message is about to be drafted, presented, or executed: before running `git commit` or `git commit --amend`, when asked to "give me a commit message" or "write the commit", or right before typing one out in a Bash/PowerShell call. Also invoke it if the user pushes back on a message you've shown them ("that's not right", "check this against conventions", "why did you skip x") — that pushback is a signal the checklist wasn't actually applied, not just a style nitpick. Do not skip this because the change "looks simple" or the draft "already looks like intent" — that exact self-assessment has been wrong before (recurred in pharos, treematches, acorn, and titan) and is the reason this skill exists instead of relying on memory alone.
---

# Commit message check

This is a checklist skill, not an advisory one: the point is to make re-deriving and rechecking a
commit message mechanical, so it doesn't depend on remembering the rules correctly under time
pressure mid-task. The failure this skill exists to prevent isn't "not knowing the rules" — it's
drafting a message from whatever's fresh in context (the technical vocabulary of the change just
made) and presenting it without ever running the check. That's happened enough times, across enough
repos, that "I'll remember to check" isn't a safe assumption anymore. Actually walk through the
steps below, in order, every time.

## Step 0 — Read the source of truth fresh

Read the user's global `CLAUDE.md` (the "Commit message conventions" section — typically at
`~/.claude/CLAUDE.md`, i.e. the user's home directory on whichever machine this is running on,
never a hardcoded path from a different machine/account) now, in full, even if you've read it
before this session. Don't work from a paraphrased memory of it — the rules get updated, and a
stale mental copy is exactly what let this recur previously. If that section doesn't exist, stop
and ask the user rather than improvising conventions from general commit-message knowledge.

## Step 1 — Repo type and ticket-key prefix

- Look for `SD-####`-style or other Jira-style ticket keys in recent history (`git log --oneline
  -10`), or recall whether the user has already confirmed this is a findmypast repo.
- **Findmypast repo** → prefix required:
  - Real ticket key known → use it (e.g. `SD-2721:`).
  - No ticket, and the work is small/maintenance (typo, formatting, small fix, dependency bump) →
    `SD-000:`.
  - No ticket, and the work is a real, non-trivial feature/fix → stop and ask the user for the
    ticket key. Don't default to `SD-000:` just because asking feels like friction — the
    conventions doc is explicit that this is the wrong call for non-trivial work.
- **Not a findmypast repo** (checked history, genuinely no ticket pattern, user hasn't said either
  way) → no prefix.
- **Genuinely can't tell** (e.g. too few commits to judge, or a mixed/inconclusive history) → this
  is a third state, not a coin flip. Don't silently default to "no prefix" just because nothing
  confirmed "yes" — say what you checked and ask the user directly which convention applies.

## Step 2 — Subject line

Check the drafted subject against each of these individually — don't eyeball the whole line at
once and call it good:

- Imperative, present tense (`Add`, `Fix`, `Remove` — not `Added`, `Fixed`, `Adding`).
- Capitalized right after the prefix colon (or at the start, if there's no prefix).
- No trailing period.
- One line, well under 72 characters.
- Names the object of the verb. A bare `Fix`, `Refactor`, or `WIP` fails this even on an
  iteration commit inside a bigger ticket — these get read individually later (bisect, blame,
  cherry-pick), not just squash-merged away.

If anything here fails, rewrite the subject before touching the body — a body can't rescue a bad
subject.

## Step 3 — Does this even need a body?

Default assumption: no. Only add one if the *why* genuinely isn't recoverable from the subject
alone. When in doubt, leave it out — the pattern in Andrew's own history is bodies getting trimmed
down over time, not expanded, so a lean instinct here is the right one.

## Step 4 — If a body is written, strip-test every bullet

- Format is always `-`-bulleted. Never a prose paragraph, no matter how short.
- For each bullet, actually run this sequence (in your own reasoning, not silently skipped):
  1. List every proper noun, class name, function name, library name, header name, or config key
     that appears in it.
  2. Delete them from the sentence.
  3. Read what's left — does it still stand alone as a complete rationale?
  4. If yes, keep it. If no, it was describing the mechanism rather than the intent — rewrite it
     as pure "why," then run the test again on the new version.
- The diff already shows the mechanism; the message's only job is the part the diff can't show —
  why the change happened.

**Worked example** — drafting a fix to how a shared UI component forwards refs:

> Not compliant (mechanism, prose): "Radix's internal Slot/Portal machinery attaches a ref to
> whatever child is rendered inside `<Dialog.Portal>`, but these were plain function components
> rather than `React.forwardRef`, so any ref never reached the DOM node."
>
> Compliant (bulleted, survives the strip-test): "- Without it, consumers hit a console warning
> and any ref passed through it was silently dropped instead of reaching the element." — remove
> "console warning"/"ref"/"element" and it still reads as a complete reason for the change; no
> class, function, or library name is load-bearing in the sentence.

## Step 5 — Scan for AI-authorship references

Check the fully composed subject + body for `Claude`, `Anthropic`, `Generated with`, any
`Co-Authored-By` naming an AI, `Claude-Session`, or any other harness-injected trailer. Strip it
immediately if present — this applies even when a tool/template tries to add it automatically,
every time, without being asked.

## Step 6 — Only now, show it or commit it

The message may only be shown to the user or passed to `git commit` once steps 1–5 have all been
walked through for *this* draft — not carried over from an earlier draft in the same conversation.
If the user pushes back on something you show them, that means the checklist was skipped or
rushed: go back to Step 1 on the corrected version rather than only patching the specific
complaint they happened to notice.

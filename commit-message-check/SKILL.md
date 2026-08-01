---
name: commit-message-check
description: Mandatory pre-commit gate for any git commit message drafted on this user's behalf, in any repo. Loads the user's own conventions from a per-user conventions file (bootstrapped on first use if it doesn't exist yet) and walks through a literal checklist — ticket-key prefix (if the user's conventions use one), subject mood/length, whether a body is even needed, a strip-test on every body bullet, and a scan for AI-authorship references — before the message is ever shown to the user or passed to `git commit`. Invoke this every time a commit message is about to be drafted, presented, or executed: before running `git commit` or `git commit --amend`, when asked to "give me a commit message" or "write the commit", or right before typing one out in a Bash/PowerShell call. Also invoke it if the user pushes back on a message you've shown them ("that's not right", "check this against conventions", "why did you skip x") — that pushback is a signal the checklist wasn't actually applied, not just a style nitpick. Do not skip this because the change "looks simple" or the draft "already looks like intent" — that exact self-assessment is what this skill exists to catch instead of relying on memory alone.
---

# Commit message check

This is a checklist skill, not an advisory one: the point is to make re-deriving and rechecking a
commit message mechanical, so it doesn't depend on remembering the rules correctly under time
pressure mid-task. The failure this skill exists to prevent isn't "not knowing the rules" — it's
drafting a message from whatever's fresh in context (the technical vocabulary of the change just
made) and presenting it without ever running the check. Actually walk through the steps below, in
order, every time.

The rules themselves are **not baked into this skill** — they're the user's own conventions,
kept in a conventions file this skill reads fresh every run and bootstraps on first use if it
doesn't exist yet. That split is deliberate: this skill is the mechanical checklist, portable
across users; the conventions file is one person's preferences, specific to them.

One companion file:

- `setup.md` — the one-time bootstrap interrogation. Read it when Step 0 finds no conventions
  file yet.

## Step 0 — Find or bootstrap the conventions file

Look for a conventions file at `~/.claude/commit-message-conventions.md` (the user's home
directory on whichever machine this is running on — never a path copied from a different
machine or account).

- **Exists** → read it fresh, in full, every run. Don't work from a paraphrased memory of it —
  the user can edit it any time, and a stale mental copy defeats the point of keeping it external.
- **Doesn't exist** → read `setup.md` and run the bootstrap interrogation before continuing.
  Don't improvise conventions from general commit-message knowledge or from this skill's own
  worked examples — those illustrate the mechanism, they aren't a default ruleset. Every "safe
  general default" referenced in Steps 2-5 below gets explicitly shown and confirmed during that
  interrogation, not silently assumed — see `setup.md`. A default a user never saw isn't really a
  default, it's undisclosed forced behavior.

## Step 1 — Ticket-key prefix (only if the conventions file defines one)

Not every user or repo uses a ticket-key prefix — treat this step as conditional on what the
conventions file actually says, not as a universal requirement.

If the conventions file defines a prefix convention, it should specify: which repos it applies
to (a detection rule, e.g. "repos with existing TICKET-#### style history"), the format, and what
to do when no ticket key is known (a placeholder value, and/or a threshold for when to stop and
ask instead of defaulting). Apply exactly that rule:

- Repo matches the convention's detection rule → prefix required, following its format/placeholder
  rules.
- Repo doesn't match → no prefix.
- **Genuinely can't tell** (too few commits to judge, mixed/inconclusive history) — this is a
  third state, not a coin flip. Don't silently default to "no prefix" just because nothing
  confirmed "yes" — say what you checked and ask the user directly which convention applies.

If the conventions file has no ticket-prefix section at all, skip this step — the user doesn't
use one.

## Step 2 — Subject line

Check the drafted subject against each rule the conventions file lists for subject lines,
individually — don't eyeball the whole line at once and call it good. If the conventions file is
silent on a point, these are safe general defaults:

- Imperative, present tense (`Add`, `Fix`, `Remove` — not `Added`, `Fixed`, `Adding`).
- No trailing period.
- One line, well under 72 characters.
- Names the object of the verb. A bare `Fix`, `Refactor`, or `WIP` fails this even on an
  iteration commit inside a bigger ticket — these get read individually later (bisect, blame,
  cherry-pick), not just squash-merged away.

If anything here fails, rewrite the subject before touching the body — a body can't rescue a bad
subject.

## Step 3 — Does this even need a body?

Default assumption: no. Only add one if the *why* genuinely isn't recoverable from the subject
alone. When in doubt, leave it out, unless the conventions file says otherwise for this user.

## Step 4 — If a body is written, strip-test every bullet

- Format is `-`-bulleted, never a prose paragraph, unless the conventions file specifies
  something different.
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
immediately unless the conventions file explicitly says to include one for this commit — this
applies even when a tool/template tries to add it automatically, every time, without being asked.

## Step 6 — Only now, show it or commit it

The message may only be shown to the user or passed to `git commit` once steps 1–5 have all been
walked through for *this* draft — not carried over from an earlier draft in the same conversation.
If the user pushes back on something you show them, that means the checklist was skipped or
rushed: go back to Step 1 on the corrected version rather than only patching the specific
complaint they happened to notice. If the pushback reveals the conventions file itself is wrong
or out of date, that's a separate, explicit edit to the conventions file — confirm the change with
the user before writing it, same as any other update to their stored preferences.

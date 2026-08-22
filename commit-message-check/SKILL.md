---
name: commit-message-check
description: Mandatory pre-commit gate for any git commit message drafted on this user's behalf, in any repo. Loads the user's own conventions from a per-user conventions file (bootstrapped on first use if it doesn't exist yet), organized by the structural parts of a commit message — prefix, subject, body, footer, whole-message, and miscellaneous — and checks the draft against every rule listed under each part before the message is ever shown to the user or passed to `git commit`. Invoke this every time a commit message is about to be drafted, presented, or executed: before running `git commit` or `git commit --amend`, when asked to "give me a commit message" or "write the commit", or right before typing one out in a Bash/PowerShell call. Also invoke it if the user pushes back on a message you've shown them ("that's not right", "check this against conventions", "why did you skip x") — that pushback is a signal the checklist wasn't actually applied, not just a style nitpick. Do not skip this because the change "looks simple" or the draft "already looks like intent" — that exact self-assessment is what this skill exists to catch instead of relying on memory alone.
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

**The checklist is organized around the structural parts of a commit message — Prefix, Subject,
Body, Footer, Whole-message, Miscellaneous — matching the conventions file's six headings, not
around a fixed list of named rules.** Every step below does exactly the same thing: *iterate every
rule the conventions file lists under that heading, check the draft against each one
individually.* Same mechanism, six times, not six bespoke ones — so a brand new rule always has a
home and always gets checked, without SKILL.md needing to change to accommodate it. This is stated
once, here; the steps below don't repeat it.

**If two rules genuinely conflict** — two rules under one heading, rules across two headings, or
a rule against a built-in default — that's the same third state Step 1 already handles for an
unclear prefix: not a coin flip. Don't silently pick whichever rule is more specific, more recent,
or easier to satisfy. Stop, show the user the specific conflict (both rules, quoted), and ask.
Whatever they say resolves it going forward is a conventions-file edit — write gate 2 below — not
a one-off judgment call repeated silently on every future commit that hits the same conflict.

This skill has more than one point where it writes something consequential; per this repo's
"propose, don't just do," each is gated on user confirmation and none skips it:

Scope: this table tracks **consequential writes** — anything that ends up in a file or in git
history — and nothing else. Steps 1-6's checks aren't in it because they aren't writes and aren't
gated: they run on every draft, unconditionally. Absence from this table never means optional.

| # | What gets written | Gated where |
|---|---|---|
| 1 | The conventions file itself, at bootstrap | `setup.md` steps 2-4 |
| 2 | A correction to an existing conventions file (conflict resolution, or a rule the user says is wrong/stale) | Step 7 |
| 3 | The commit message itself (shown or passed to `git commit`) | Step 7 |

Update this table in the same edit that adds or moves a write gate.

**Whenever two or more options are presented for the user to pick from** — the malformed-file
choice in Step 0, a conflict between two rules in Step 7, anything added later — **number them
`1.`, `2.`, `3.`… in a single sequential list**, whatever label each carries. A label explains an
option; a number is what the user can say back ("go with 2") to pick one unambiguously. A single
unambiguous recommendation with nothing else to choose between doesn't need one.

One companion file:

- `setup.md` — the one-time bootstrap interrogation. Read it when Step 0 finds no conventions
  file yet.

## Step 0 — Find or bootstrap the conventions file

Two possible locations, checked in this order:

1. **Repo-level**: `.claude/commit-message-conventions.md` at the current repo's root. This is a
   team's shared, committed convention — if it exists, it's not one person's file to silently
   defer to or override.
2. **Personal**: `~/.claude/commit-message-conventions.md` (the user's home directory on whichever
   machine this is running on — never a path copied from a different machine or account).

**Both paths are `.claude/`, deliberately, and that's also where a new one gets created.** This is
**config** — a file the skill reads on every run and a human opens rarely — as distinct from
working state or documentation a user reads and hand-edits, which belongs somewhere visible. So
don't look for a bare `commit-message-conventions.md` sitting directly at the repo root or inside a
docs folder, and never create one there.

**Repo root, not project root.** Deliberately different from where this repo's other skills put
their artifacts. Commit conventions are a team standard for a whole git repository; a repo holding
several projects still has one commit history and one set of conventions, so a per-project file
would fragment a rule that isn't per-project.

Read whichever exist, in full, fresh every run — don't work from a paraphrased memory of either,
they can be edited any time and a stale mental copy defeats the point of keeping them external.
**Precedence is per heading, not whole-file**: for each of the six headings, use the repo-level
file's version if it defines that heading, otherwise the personal file's version, otherwise the
built-in default (Steps 2 and 5 below). An empty or absent heading in either file just falls
through to the next source — it doesn't mean the matching step gets skipped without looking.

If neither file exists, read `setup.md` and run the bootstrap interrogation before continuing.
Don't improvise conventions from general commit-message knowledge or from this skill's own worked
examples — those illustrate the mechanism, they aren't a default ruleset. `setup.md` covers why
every built-in default below gets shown and confirmed there rather than assumed, and where the
bootstrapped file ends up (repo-level or personal).

**If a file exists but doesn't parse** — none of the six headings present, or content that doesn't
resemble this structure at all — don't silently reinterpret it, discard it, or fall back to
bootstrapping over it. Show the user what was found and ask them to pick, as a numbered choice:
1) fix it up into the expected format, 2) replace it via `setup.md`, or 3) leave it as-is with a
one-off manual read for this commit only.

## Step 1 — Prefix

Not every user or repo uses a ticket-key or other prefix — this step is conditional on whether
`## Prefix` has any rules, not a universal requirement.

If it does, it should specify: which repos it applies to (a detection rule, e.g. "repos with
existing TICKET-#### style history"), the format, and what to do when no ticket key is known (a
placeholder value, and/or a threshold for when to stop and ask instead of defaulting). Apply
exactly that rule, checking each listed condition individually:

- Repo matches the convention's detection rule → prefix required, following its format/placeholder
  rules.
- Repo doesn't match → no prefix.
- **Genuinely can't tell** (too few commits to judge, mixed/inconclusive history) — this is a
  third state, not a coin flip. Don't silently default to "no prefix" just because nothing
  confirmed "yes" — say what you checked and ask the user directly which convention applies.

If `## Prefix` is empty, skip straight to Step 2.

## Step 2 — Subject

Check the drafted subject against every rule listed under `## Subject`, individually — don't
eyeball the whole line at once and call it good. If that section is silent on a point, these are
the skill's built-in defaults (shown and confirmed at setup, not assumed here):

- Imperative, present tense (`Add`, `Fix`, `Remove` — not `Added`, `Fixed`, `Adding`).
- No trailing period.
- One line, well under 72 characters.
- Names the object of the verb. A bare `Fix`, `Refactor`, or `WIP` fails this even on an
  iteration commit inside a bigger ticket — these get read individually later (bisect, blame,
  cherry-pick), not just squash-merged away.

If anything here fails, rewrite the subject before touching the body — a body can't rescue a bad
subject.

## Step 3 — Body

First: does this commit even need a body? Check `## Body` for a stated policy; the built-in
default is *no, unless the why genuinely isn't recoverable from the subject alone*.

If a body is written, check it against every rule listed under `## Body`, individually. Built-in
default (deliberately light — no format imposed, applies only to whatever isn't overridden):

- Explain *why* the change happened, not what changed or how — the diff already shows the
  mechanism, so text that just narrates the diff isn't adding anything.
- No mandated structure (bulleted vs. prose vs. something else) — that's a formatting choice, not
  a universal git convention, so it's asked at setup rather than assumed here.

If `## Body` defines a specific technique for checking that (e.g. a strip-test — see `setup.md`
and `README.md`), apply exactly what's written there.

## Step 4 — Footer

Check for any rules under `## Footer` — trailers, required links, co-author lines, anything that
goes after the body. No built-in default content (most users have none): if `## Footer` lists
something (e.g. "append a link to the relevant ticket/PR"), apply it; if it's empty, there's no
footer to add.

## Step 5 — Whole-message

Check the fully composed message (prefix + subject + body + footer together) against every rule
listed under `## Whole-message` — rules that apply uniformly across the entire text rather than to
one part (e.g. a language/spelling convention, a tone rule). One built-in default always applies
here regardless of what the conventions file says, unless it explicitly opts out for a specific
commit:

- Scan for `Claude`, `Anthropic`, `Generated with`, any `Co-Authored-By` naming an AI,
  `Claude-Session`, or any other harness-injected AI-authorship trailer. Strip it immediately —
  this applies even when a tool/template tries to add it automatically, every time, without being
  asked, unless this specific commit was explicitly asked to include one.

## Step 6 — Miscellaneous

Check every rule listed under `## Miscellaneous` — rules that don't cleanly attach to one
structural part (e.g. how revert messages should read, how iteration commits within one piece of
work should relate to each other, a rule conditional on more than one part at once).

## Step 7 — Only now, show it or commit it

The message may only be shown to the user or passed to `git commit` once Steps 1-6 have all been
walked through for *this* draft — not carried over from an earlier draft in the same conversation.
If the user pushes back on something you show them, that means the checklist was skipped or
rushed: go back to Step 1 on the corrected version rather than only patching the specific
complaint they happened to notice. If the pushback reveals a conventions file rule itself is wrong
or out of date, that's a separate, explicit edit — write gate 2 in the table above — confirm the
change with the user before writing it. With two possible files, also confirm
*which one*: a wrong team standard belongs in the repo-level file, a wrong personal preference in
the personal one — don't assume based on which file happened to already define that heading.

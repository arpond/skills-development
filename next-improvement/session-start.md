# Session start: find/bootstrap the tracker, check staleness

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Steps 0
and 0.5 of the loop. Unlike the other companion files (`setup.md`, `strategies.md`,
`feedback.md`), this one isn't optional or one-time: every run starts here, since every run needs
a tracker to read and needs to know whether its Goals are still trustworthy before ranking
anything against them. It lives in its own file purely to keep `SKILL.md` focused on the
steady-state propose/build/record loop — the split is about what's loaded into the common-case
read, not about this content being rare.

Once this file's steps are done, continue to Step 1 in `SKILL.md`.

## Step 0: Find or bootstrap the tracker

Look for `IMPROVEMENT_TRACKER.md` at the root of whichever project the user is currently working
in (use judgement on project boundary: the nearest enclosing directory with its own README,
package manifest, or similar — not necessarily the git repo root, since one repo can contain
several projects with different concerns).

If it doesn't exist yet, read `setup.md` and follow it before doing anything else — that's a
one-time-per-project bootstrap, kept out of this file since most invocations don't need it.

If it does exist, read it as-is and continue — don't re-ask full setup questions on later runs.
Goals aren't fixed forever though: see Step 0.5 below.

**If it exists but is malformed** (no `## Goals` section, a tier line that doesn't parse as
priority order, an unrecognised `Selection strategy:`/`Feedback:` value) — this is a case of
"unreachable isn't resolved," not a normal empty/stale tracker: don't silently rewrite it back
into shape (that guesses at intent the user never confirmed) and don't refuse to proceed either.
Name the specific thing that doesn't parse and ask directly: fix it by hand, or walk through
re-doing just that broken piece (e.g. re-running the Goals portion of `setup.md` if only Goals is
broken, leaving categories/Done/Rejected untouched). Never fabricate a plausible-looking Goals
list to paper over a missing one — a wrong guess here silently misranks every candidate for as
long as the tracker lives, the exact failure mode Step 0.5 already exists to prevent for staleness.
This is one of the skill's hard rules (see the table in `SKILL.md`).

## Step 0.5: Check whether goals are stale

Goals can drift as the project evolves, even without a formal re-setup. Check the `Last
reviewed:` date under Goals:

- **Missing** (tracker predates this field): treat as stale, ask now.
- **Older than ~30 days, or the Done list has grown noticeably since the last review**: prompt
  the user with a short check-in — e.g. "Goals were last confirmed on <date> and N items have
  shipped since. Still the right order, or has anything changed?" Offer to keep as-is, reorder,
  add/remove a tier, or fold in a new priority entirely.
- **Recently reviewed and nothing suggests drift**: skip the prompt, proceed straight to Step 1.

**Don't update the Goals section until the user has responded to the check-in** — this is one of
the skill's hard rules (see the table in `SKILL.md`). If the user changes anything, update the
Goals section and bump `Last reviewed:` to today. If they confirm as-is, still bump the date so
the next run doesn't re-ask right away. This check is a single short question, not a repeat of the
full `setup.md` interrogation — don't re-litigate every tier from scratch unless the user wants
to.

If `Feedback:` is also due a check-in this same run (see `feedback.md`), fold both into a single
message rather than asking twice in a row — e.g. "Goals were last confirmed on <date> and N items
have shipped since, still the right order? Also, last shipped '<idea>' (<date>) — deliver as
expected, mixed, or miss?" Two unrelated confirmations stacked back-to-back at the start of a run
is exactly what "one check-in, not two" exists to avoid, even though they're about different
things (goals vs. outcomes) — the point is the user reads one message, not that the topics match.
If only one of the two is due, ask just that one; don't manufacture a second question to fill out
a combined message. Note that `feedback.md`'s own check-in only actually surfaces once per
session regardless — see its "Checking in" section — so on a later round in the same sitting there
may be nothing from Feedback to fold in at all.

The user can also trigger this at any time outside of a normal run — e.g. "reprioritise" or
"goals have changed" — by jumping straight to this step, editing Goals, and bumping the date.
This is also where an existing tie can be broken into a strict order, or a new tie formed between
previously-distinct tiers — same edit-and-bump mechanism as any other reprioritisation.

If `Selection strategy:` is present (or the user wants to add/change it), see `strategies.md` —
it's not fixed at setup either and is edited the same lightweight way. If `Feedback:` is present
(or the user wants to add/change it), see `feedback.md`, which also runs its own short check-in
from this step when relevant.

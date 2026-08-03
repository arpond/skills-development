# Session start: find/bootstrap the tracker, check staleness

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Steps 0
through 0.7 of the loop. Unlike the other companion files, this one has no gate at all: every run
starts here, since every run needs
a tracker to read and needs to know whether its Goals are still trustworthy before ranking
anything against them. It lives in its own file purely to keep `SKILL.md` focused on the
steady-state propose/build/record loop — the split is about what's loaded into the common-case
read, not about this content being rare.

Once this file's steps are done, continue to Step 1 in `SKILL.md`.

**Every check-in in this file folds into one message.** Steps 0.5, 0.6 and 0.7 can each turn up
something to raise, and they're all raised at the start of the same run — so whatever's due this
run gets asked in a single message, never stacked back-to-back. If Goals are stale, a reassess flag
is waiting, and a `revisit-after:` date has passed, that's one message with three questions in it,
not three prompts. If only one is due, ask just that one, and never manufacture a second question
to fill out a combined message. Each step below says what it contributes; none of them re-decides
this. They also share one throttle: each surfaces at most once per session, tracked in conversation
context only, never written to the tracker.

**Mechanical bookkeeping is a blocking gate, not optional prose to skim past.** Three items below
need no user response — backfilling missing `Created:`/`Feature check:` (Step 0), flagging a
closed-tracker-sections violation (Step 0), and re-deriving the Done archive sweep (Step 0.5) — and
because none of them wait on an answer, it's easy for a run to jump straight from "found the
tracker" to the check-in questions (0.5/0.6/0.7) and skip these silently, since skipping them
produces no visible error. That's not a shortened Step 0, it's an incomplete one: all three must
actually execute (files written, flag raised if applicable) before continuing to Step 1, every run,
regardless of whether anything below turns out to be due this run.

## Step 0: Find or bootstrap the tracker

First establish the project: the nearest enclosing directory with its own README, package manifest,
or similar — not necessarily the git repo root, since one repo can contain several projects with
different concerns.

**Then resolve `IMPROVEMENT_TRACKER.md` over these locations, in order, first hit wins:**

1. `<project>/IMPROVEMENT_TRACKER.md`
2. `<project>/<docs-dir>/IMPROVEMENT_TRACKER.md` — where `<docs-dir>` is `docs/`, `doc/`, or
   `documentation/`, whichever the project already has
3. `<project>/.claude/IMPROVEMENT_TRACKER.md`

Don't assume location 1 and stop. A tracker that exists somewhere else would be invisible, and the
next step would bootstrap a second one on top of real history — silently.

**Found in more than one location**: don't take the first and don't merge them. Say which files
were found where and ask which is authoritative; "first hit wins" orders the *lookup*, it isn't
permission to strand a second copy.

**Found nowhere**: read `setup.md` and follow it before doing anything else — a one-time-per-project
bootstrap, kept out of this file since most invocations don't need it. It creates the tracker in
`<docs-dir>/` if the project already has one, otherwise at `<project>/`. **Never create a docs
directory to hold it** — that imposes a layout the project didn't choose.

**Found somewhere other than location 1**: that's normal, not something to fix. Leave it there and
use it; existing files never get moved as a side effect of a run.

If it does exist, read it as-is and continue — don't re-ask full setup questions on later runs.
Goals aren't fixed forever though: see Step 0.5 below.

**If it exists but is malformed** (no `## Goals` section, a tier line that doesn't parse as
priority order, an unrecognised `Selection strategy:`/`Feedback:`/`Risk register:`/`Done archive:`
value, or a `Created:`/`Feature check:` that isn't a valid `X.Y.Z` version) — this is a case of
"unreachable isn't resolved," not a normal empty/stale tracker: don't silently rewrite it back
into shape (that guesses at intent the user never confirmed) and don't refuse to proceed either.
Name the specific thing that doesn't parse and ask directly: fix it by hand, or walk through
re-doing just that broken piece (e.g. re-running the Goals portion of `setup.md` if only Goals is
broken, leaving categories/Done/Rejected untouched). Never fabricate a plausible-looking Goals
list to paper over a missing one — a wrong guess here silently misranks every candidate for as
long as the tracker lives, the exact failure mode Step 0.5 already exists to prevent for staleness.
This is one of the skill's hard rules (see the table in `SKILL.md`).

**A `##` section that isn't Goals, a category, Done, or Rejected is a content-placement problem,
not a parsing problem** (see `SKILL.md`'s "closed sections" rule) — lighter-weight than the
malformed cases above, so it doesn't block the run. Flag it once per project (track in conversation
context whether it's already been raised this session, same throttle as the check-ins below —
don't re-raise every run once declined): name what's actually in the section and suggest where it
looks like it should live instead (`DEVELOPMENT.md`, a design doc, project docs). If the user wants
it moved, do that as its own small edit; if they want it left as a deliberate exception, don't
re-ask on future runs — note that call was made and move on.

**If `Created:` or `Feature check:` is missing** (tracker predates the version-stamp fields), don't
treat that as already caught up — a missing stamp is stronger evidence of being behind than a stale
one, never proof of being current. Backfill `Created:` to `SKILL.md`'s current skill version, same
mechanical no-confirmation bookkeeping as `Next id:`'s lazy-init (see `tracker-maintenance.md`) — it
only records when this tracker started being stamped, not real history, so it's fine to set
silently. `Feature check:` is different: treat it as if it had read version `0.0.0` and run Step
0.5's full behind-version disclosure walk (open `changelog.md`, walk every entry) before stamping it
to current — this tracker is owed disclosure for every feature that's ever shipped, not just future
ones, since a missing stamp confirms nothing about what it already knows. Fold that walk into the
same combined check-in as any other Step 0.5 trigger.

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

This step's contribution to the combined message is the goals question itself — e.g. "Goals were
last confirmed on <date> and N items have shipped since, still the right order? Also, last shipped
'<idea>' (<date>) — worked as intended, partial, ineffective, or reverted?" if `Feedback:` has something
due the same run. The topics don't need to match; the point is that the user reads one message.

The user can also trigger this at any time outside of a normal run — e.g. "reprioritise" or
"goals have changed" — by jumping straight to this step, editing Goals, and bumping the date.
This is also where an existing tie can be broken into a strict order, or a new tie formed between
previously-distinct tiers — same edit-and-bump mechanism as any other reprioritisation.

If `Selection strategy:` is present (or the user wants to add/change it), see `strategies.md` —
it's not fixed at setup either and is edited the same lightweight way. Same for `risk-register.md`
if `Risk register:` is present. **`Feedback:` gates on value, not presence** (`SKILL.md`'s
read-gate note): its default is `on`, so run `feedback.md`'s check-in unless the line explicitly
says `off`. That check-in contributes its own line to this run's combined message — including a
"backlog not shrinking" flag when its `growth-streak` hits 2.

**Also re-run Done's own archive sweep here, not only after Step 6 records a fresh ship.** The
sweep described in `SKILL.md` Step 6 ("After appending, check whether Done needs trimming") only
fires as a side effect of that one event — a tracker that predates the `Done archive:` field, was
hand-edited, or had a session end before that check completed can carry a Done section that's
overdue for archiving with nothing left to trigger it. Re-derive eligibility the same way Step 6
does (age vs. `floor`/`backstop`) every session start, and run the sweep if anything qualifies —
this is the same mechanical, no-confirmation bookkeeping as Step 6's own sweep, not a new
judgement call, so it doesn't wait for the combined check-in gate above. Update the same
`(last sweep: ..., streak: N)` counter Step 6 uses regardless of which step actually performed the
sweep — the counter tracks whether `age` is catching sweeps at all, not which step happened to run
one. Mention it in one clause if it actually moved anything ("archived 12 entries older than 60
days into `IMPROVEMENT_TRACKER_DONE.md`") — silent otherwise, same as any other automatic action
that didn't change what's visible this run.

**If `SKILL.md` Step 6's Done-archive `streak` has hit 3** (three backstop-triggered sweeps in a
row, `age` never once catching anything first), that's also due this step — fold it into the same
combined message per the rule above: `age` is calibrated for a slower project than this one, so
propose a concrete new number (e.g. halve it) or a higher `backstop`, wait for confirmation (hard
rule, see the table in `SKILL.md`), then reset the streak either way once asked.

**Check the tracker's `Feature check:` version against `SKILL.md`'s current skill version** (this is
also the walk Step 0 triggers for a missing stamp, treated as `0.0.0`). Compare
as standard semver — major first, then minor, then patch, numerically (`1.10.0` is newer than
`1.9.0`, not older) — never as plain string/lexicographic comparison. **Behind**: open `changelog.md`
(only now — this is exactly its trigger condition, see its own header) and walk every entry newer
than the stored version, folding them into the same combined check-in: "This tracker's on v1.0.0;
v1.1.0 added <one-line description> — want to turn it on, or leave as-is?" For each one the user
wants, hand off to that feature's *own* setup ask (`feedback.md`/`strategies.md`/`risk-register.md`'s
Setup sections, or the relevant inline instructions for a non-file feature) rather than writing the
tracker line directly here — reuse the existing confirm-gated flow per feature, don't invent a
second one. Whatever the user decides for each item, bump `Feature check:` to the skill's current
version once this has been asked — same "surfaced once, advance the marker" shape as `bulk-offer
last:`/dry-run counters, so a declined feature doesn't get re-offered every session. **Ahead** (the
tracker's `Feature check:` is newer than this skill install's current version — a downgraded skill
install, or a tracker copied over from a machine running a newer version) is a genuinely surprising
input, not a normal case to silently resolve either direction: say so once ("this tracker's stamped
v1.2.0 but this skill install is on v1.1.0 — that's unexpected, is the skill install stale?") and
don't attempt any disclosure walk, since nothing in this install's `changelog.md` is actually newer.
If only this check is due this run (Goals and Done-archive both fine), it still gets its own short
message — it doesn't need another trigger to piggyback on, just doesn't stack as a *second* message
if others are already due.

## Step 0.6: Surface standalone reassess flags (explicit `Feedback: off` only)

A `reassess: pending` flag (set by `SKILL.md` Step 6 when a later ship fixes/reworks an earlier
one) is standalone of `Feedback:` — it exists regardless of whether that subsystem is on. When
feedback is running, the flag is folded into `feedback.md`'s own check-in instead (see that file)
and this step does nothing. **This step fires only when `Feedback:` is spelled out as `off`** —
an *absent* line means the default `on`, so feedback is running and this step stays quiet.
Firing on an absent line would surface the flag twice, which is exactly what this gate prevents.

Scan Done for `reassess: pending` entries, per the combined-pool rule (`SKILL.md` Step 6's
"Reading the archive"). If any exist, surface the
oldest one as a single lightweight line — no persistent answer required, no wait/bulk timing, just
visibility: "'<origin idea>' needed a follow-up fix/rework (<the fixing idea's name>) — worth a
look at how it was scoped or actioned?" If the user engages, that's a normal conversation, not a
tracked field; if they don't, move on — don't block the rest of the run on it. Clear the flag
(remove `reassess: pending` from that entry) once it's been surfaced once, same "answered items
drop out" spirit as `feedback.md`'s eligible pool, so it doesn't repeat forever.

## Step 0.7: Surface due `revisit-after:` entries from Rejected

Scan Rejected for any `revisit-after:` date that's today or earlier. If any exist, surface the
oldest due one: "'<idea>' was declined on <date> for '<reason>', revisit was due <date> — still not
the right time, or reconsider it?" If reconsidered, hand it to `SKILL.md` Step 2 (confirm before
appending, reuse its existing id — see `SKILL.md`'s tracker-format id note). If still not the right
time, ask for a new `revisit-after:` date or drop the field so it stops resurfacing. If none are
due, say nothing.

# Session start: find/bootstrap the tracker, check staleness

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Steps 0
through 0.7 of the loop. This is a second core file, not a companion: every run starts here,
since every run needs
a tracker to read and needs to know whether its Goals are still trustworthy before ranking
anything against them. It lives in its own file purely to keep `SKILL.md` focused on the
steady-state propose loop — the split is about what's loaded into the common-case
read, not about this content being rare.

Once this file's steps are done, continue to Step 1 in `SKILL.md`.

**Every check-in in this file folds into one message.** Steps 0.5, 0.6 and 0.7 can each turn up
something to surface, and they're all surfaced at the start of the same run.
- Whatever is due this run gets asked in a single message, never stacked back-to-back. If Goals
  are stale, a reassess flag is waiting, and a `revisit-after:` date has passed, that's one
  message with three questions in it, not three prompts.
- **A backfilled tracker's baseline-subsystems catch-up (Step 0, below) is the same kind of
  contribution.** One more question folded into this run's combined message, not a separate
  prompt of its own.
- If only one item across all of these is due, ask just that one. Never manufacture a second
  question to fill out a combined message.
- Each item surfaces at most once per session, tracked in conversation context only, never
  written to the tracker.

Each step below says what it contributes; none of them re-decides this.

**The rules that need no answer still have to run.** Steps 0 and 0.5 carry four of them: the two
backfills, the closed-sections surfacing, and the Done archive sweep. `SKILL.md`'s hard-rules
table indexes each one, as a `mechanical` or a `surface` row — read them there rather than from a
second list here.

What the table can't say is the ordering. Because none of the four waits on an answer, a run can
jump from "found the tracker" straight to the check-in questions (0.5/0.6/0.7) and skip them
silently, since skipping them produces no visible error. That's not a shortened Step 0, it's an
incomplete one. All four execute — files written, violation surfaced if applicable — before Step
1, every run, whether or not anything else below turns out to be due.

## Step 0: Find or bootstrap the tracker

First establish the project: the nearest enclosing directory with its own README, package manifest,
or similar — not necessarily the git repo root, since one repo can contain several projects with
different concerns.

**Then resolve `IMPROVEMENT_TRACKER.md` over these locations, in order, first hit wins:**

1. `<project>/IMPROVEMENT_TRACKER.md`
2. `<project>/<docs-dir>/IMPROVEMENT_TRACKER.md` — where `<docs-dir>` is `docs/`, `doc/`, or
   `documentation/`, whichever the project already has. Where the project has more than one,
   check every one of them. A tracker in two of them is the ambiguity case below.
3. `<project>/.claude/IMPROVEMENT_TRACKER.md`

Don't assume location 1 and stop. A tracker that exists somewhere else would be invisible, and the
next step would bootstrap a second one on top of real history — silently.

**Found in more than one location**: don't take the first and don't merge them. Say which files
were found where and ask which is authoritative; "first hit wins" orders the *lookup*, it isn't
permission to strand a second copy.

**Found nowhere**: read `setup.md` and follow it before doing anything else — a one-time-per-project
bootstrap, kept out of this file since most invocations don't need it. It creates the tracker in
`<docs-dir>/` if the project already has one, otherwise at `<project>/`. **Never create a docs
directory to hold it.** That imposes a layout the project didn't choose.

**Found somewhere other than location 1**: that's normal, not something to fix. Leave it there and
use it; existing files never get moved as a side effect of a run.

If it does exist, read it as-is and continue — don't re-ask full setup questions on later runs.
Goals aren't fixed forever though: see Step 0.5 below.

**If it exists but is malformed, don't silently rewrite it back into shape, and don't refuse to
proceed either.** Malformed means: no `## Goals` section, a tier line that doesn't parse as
priority order, an unrecognised `Selection strategy:`/`Feedback:`/`Risk register:`/`Done archive:`
value, an `Entry word limit:` that is neither a positive whole number nor `off`, or a
`Created:`/`Feature check:` that isn't a valid `X.Y.Z` version. Two lines for one setting are
malformed too, because they can disagree. An `Entry limit:` line counts as an `Entry word limit:`
line for this. Unrecognised means the
setting itself can't be read: a mode or on/off value that names nothing. A parameter *inside* a
mode that reads fine is not this case. A degenerate count or a stale cursor is handled where that
mode is defined (`strategies.md`), announced rather than asked about. This is a case of
"unreachable isn't resolved," not a normal empty/stale tracker. Rewriting it guesses at intent the
user never confirmed.
Name the specific thing that doesn't parse and ask directly: fix it by hand, or walk through
re-doing just that broken piece (e.g. re-running the Goals portion of `setup.md` if only Goals is
broken, leaving categories/Done/Rejected untouched). Never fabricate a plausible-looking Goals
list to paper over a missing one — a wrong guess here silently misranks every candidate for as
long as the tracker lives, the exact failure mode Step 0.5 already exists to prevent for staleness.
This is one of the skill's hard rules (see the table in `SKILL.md`).

**Rename an `Entry limit:` line to `Entry word limit:` as soon as it is found.** It is the 2.4.0
spelling of the same setting. Do it before any check reads the setting, and at any stamp. Rename
that key in the header sentence in the same write. It is mechanical bookkeeping, with no gate.

**A `##` section that isn't Goals, a category, Done, or Rejected is a content-placement problem,
not a parsing problem** (see `SKILL.md`'s "closed sections" rule). It's lighter-weight than the
malformed cases above, so it doesn't block the run.
- Surface it once per session, tracked in conversation context, same throttle as the check-ins
  below. Don't re-surface every run once declined.
- Name what's actually in the section and suggest where it looks like it should live instead
  (`DEVELOPMENT.md`, a design doc, project docs).
- If the user wants it moved, do that as its own small edit. If they want it left as a deliberate
  exception, note that call was made and don't re-ask on future runs.

**If `Created:` or `Feature check:` is missing**, the tracker predates the version-stamp fields.
Read `tracker-maintenance.md`'s "Catching up a tracker that predates the version stamps" and
follow it before continuing. It covers the two backfills, the disclosure the tracker is owed, and
the baseline features it never got offered. Don't treat a missing stamp as already caught up, and
don't backfill and stamp in one move — both are failures that section exists to block.

## Step 0.5: Check whether goals are stale

Goals can drift as the project evolves, even without a formal re-setup. Check the `Last
reviewed:` date under Goals:

- **Missing** (tracker predates this field): treat as stale, ask now.
- **Older than ~30 days, or five or more items shipped since the last review**: prompt
  the user with a short check-in — e.g. "Goals were last confirmed on <date> and N items have
  shipped since. Still the right order, or has anything changed?" Offer to keep as-is, reorder,
  add/remove a tier, or fold in a new priority entirely.
- **Recently reviewed and nothing suggests drift**: skip the prompt, proceed straight to Step 1.

**Don't update the Goals section until the user has responded to the check-in.** This is one of
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
if `Risk register:` is present. **`Feedback:` is read by value, not presence** (`SKILL.md`'s
read-condition note): its default is `on`, so run `feedback.md`'s check-in unless the line explicitly
says `off`. That check-in contributes its own line to this run's combined message — including a
"backlog not shrinking" flag when its `growth-streak` hits 2.

**Run the Done archive sweep.** It checks at every session start, and again after each ship that
`build-and-record.md` Step 6 records. It archives only when an entry qualifies. A check that
archives nothing leaves the tracker, and the counter below, untouched. The run here catches what an append-time sweep missed: a
session that ended early, a hand-edited tracker, a tracker older than `Done archive:`. Primary
trigger is age, not count. How long ago something shipped decides whether it's still useful
working context, not how many entries sit next to it (a project shipping in bursts can produce 20
genuinely-recent entries in two weeks; a slow project can carry 10 stale ones for a year). The
sweep:
1. Archive any Done entry whose `shipped` date is older than `Done archive:`'s `age` (default 60
   days).
2. **Always keep the most recent `floor` entries live regardless of age** (default 5), so a
   dormant project that just resumed doesn't get its Done section swept to empty.
3. **Count stays as a backstop only.** If the live section still exceeds `backstop` entries
   (default 40) after the age sweep, archive the oldest down to `floor` by age regardless. One
   hyperactive stretch then can't leave the file unbounded between age-sweeps.
4. Move archived entries, unedited and in their existing order, to the end of
   `IMPROVEMENT_TRACKER_DONE.md`. Create it if it doesn't exist yet, in the same directory as
   `IMPROVEMENT_TRACKER.md`, with a one-line `# <Project> — archived Done history` header.
5. Update the archive-pointer note under the live `## Done` header to the cutoff date of the
   oldest entry now remaining live.
6. Mention it in one clause if it moved anything ("archived 12 entries older than 60 days into
   `IMPROVEMENT_TRACKER_DONE.md`"). Otherwise stay silent, same rule as the id backfill in Step 0.

This is mechanical bookkeeping, not a judgement call about ideas or priorities, so it doesn't wait
for the combined check-in. Only the knob *adjustment* below waits for confirmation.

**Trimming doesn't wait on `outcome`** (`Feedback: on` — see `feedback.md`). Archive eligible-by-age
entries regardless of whether their outcome is still `pending`. Otherwise a feedback loop that
can't keep pace with shipping would let the live Done section grow without bound. An entry crossing
into the archive while still `pending` stays askable from the other file, per `SKILL.md`'s
"Reading the archive".

`category-rotation` (`strategies.md`) counts live Done entries only, never the archive. A window
larger than the live section holds counts as insufficient history there, and never opens the
archive to fill the count.

**Track which trigger actually fired, to catch a miscalibrated `age`.** It is a self-correcting
counter, the same shape as `SKILL.md` Step 2's dry-run tracking. Note which kind of sweep just ran
inline on the `Done archive:` line: `(last sweep: backstop, streak: N)` or
`(last sweep: age, streak: 0)`.
Update it whichever run performed the sweep, and only when the sweep archived something. **If the
`Done archive:` line isn't present** (the
normal case, since it's absent whenever the defaults haven't changed), write it out with its
default values first and annotate that. There's no other line it belongs on. Trigger/increment: a
`backstop` sweep. Corrected signal/reset: an `age` sweep, back to 0. Threshold: `streak: 3` or
more (three backstop-triggered sweeps in a row with `age` never once catching anything first).
**Read the stored streak at session start, before this session's sweep can change it.** A
threshold reached by a sweep after a ship has no combined message to join, so it waits for the
next session start. At the threshold, fold it into this step's combined message:
1. Surface it: `age` is calibrated for a slower project than this one is actually shipping at.
2. Propose halving `age` (or raising `backstop`) with a concrete number.
3. Wait for confirmation before writing. This is a hard rule (see the table in `SKILL.md`).
4. Force-reset the streak once surfaced, regardless of the answer, same as the dry-run counter.

**Check entry sizes against `Entry word limit:`.** An absent line means 60 words, and `off` skips
this check.
1. Count the words in every entry of every idea category. An entry is its bullet line plus the
   indented lines under it, with its id and name.
2. Count with a tool, such as `wc -w` or a short script. An estimate is not a count.
3. Note any content in a category that is not an entry: a `###` heading, a table, a paragraph. The
   `(dry runs: …)` note is part of the format, not content.
4. If an entry is over the limit, or a category holds non-entry content, contribute one line to
   the combined message. Give the number of entries over the limit and the largest entry, by name
   and word count. Name any non-entry content by category. Ask whether to trim some now.
5. If neither is found, say nothing.

A yes goes to `tracker-maintenance.md`'s "Trimming an oversized entry". A no holds for the rest of
the session, and nothing about it is written to the tracker. Done and Rejected are not counted.
They are append-only history, and a trim edits the entry.

When the user asks to set `Entry word limit: off`, the header still tells writers to keep within a
limit. Offer to delete that sentence from the header in the same write.

**Check the tracker's `Feature check:` version against `SKILL.md`'s current skill version.** This
is also the walk Step 0 triggers for a missing stamp, treated as `0.0.0`. Compare as standard
semver: major first, then minor, then patch, numerically (`1.10.0` is newer than `1.9.0`, not
older), never as plain string/lexicographic comparison.

**Behind:**
1. Open `changelog.md` (only now; this is exactly its trigger condition, see its own header).
2. Walk every entry newer than the stored version in ascending version order (oldest first),
   applying each one's migration before moving to the next. `changelog.md` itself lists
   newest-first for a human skimming what's new, but that's a reading order, not an application
   order, and a later entry's migration can assume an earlier one already landed.
3. Fold them into the same combined check-in in that same order: "This tracker's on v1.0.0;
   v1.1.0 added <one-line description> — want to turn it on, or leave as-is?"
4. For each one the user wants, hand off to that feature's *own* setup ask
   (`feedback.md`/`strategies.md`/`risk-register.md`'s Setup sections, or the relevant inline
   instructions for a non-file feature) rather than writing the tracker line directly here. Reuse
   the existing confirm-gated flow per feature; don't invent a second one.
5. Whatever the user decides for each item, bump `Feature check:` to the skill's current version
   once this has been asked. Same "surfaced once, advance the marker" shape as `bulk-offer
   last:`/dry-run counters, so a declined feature doesn't get re-offered every session.

**Ahead** (the tracker's `Feature check:` is newer than this skill install's current version — a
downgraded skill install, or a tracker copied over from a machine running a newer version) is a
genuinely surprising input, not a normal case to silently resolve either direction:
1. Say so once ("this tracker's stamped v1.2.0 but this skill install is on v1.1.0 — that's
   unexpected, is the skill install stale?").
2. Don't attempt any disclosure walk, since nothing in this install's `changelog.md` is actually
   newer.
3. Leave the stamp alone. Don't move it forward to match the install, and don't wind it back.

If only this check is due this run (nothing else in this file has anything to surface), it still gets its own short
message. It doesn't need another trigger to piggyback on, just doesn't stack as a *second* message
if others are already due.

## Step 0.6: Surface standalone reassess flags (explicit `Feedback: off` only)

A `reassess: pending` flag (set by `build-and-record.md` Step 6 when a later ship fixes/reworks an earlier
one) is standalone of `Feedback:` — it exists regardless of whether that subsystem is on. When
feedback is running, the flag is folded into `feedback.md`'s own check-in instead (see that file)
and this step does nothing. **This step fires only when `Feedback:` is spelled out as `off`** —
an *absent* line means the default `on`, so feedback is running and this step stays quiet.
Firing on an absent line would surface the flag twice, which is exactly what this condition prevents.

Scan Done for `reassess: pending` entries, per the combined-pool rule (`SKILL.md`'s
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

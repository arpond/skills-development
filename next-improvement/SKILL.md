---
name: next-improvement
description: Runs a "what should we work on next" process for whatever project the user is currently in — maintains a per-project IMPROVEMENT_TRACKER.md (idea categories + a tiered priority list), tops up any category that's run low by brainstorming fresh ideas grounded in that project's actual current state, ranks candidates against the project's own configured tiers, and proposes the next thing to build for the user to confirm before any code changes happen. Bootstraps the tracker itself on first use if the project doesn't have one yet. Use this whenever the user asks "what should we do next" / wants to pick the next feature or refactor / asks to poll for more ideas / mentions an improvement tracker or backlog, or when a work session is starting on a project with no specific task queued up yet.
---

# Next improvement

**Skill version: 2.1.0.** `session-start.md`'s version check compares a tracker's `Feature check:`
stamp against this number. `changelog.md` holds both what shipped at each version and the
versioning policy itself — read it only when that check actually finds a gap, not on every run.

A repeatable "what next" loop: keep a running list of ideas per project, top the list up when
it runs thin, pick the next thing to build by weighing it against that project's own standing
priorities, confirm with the user, plan it in detail, build it, then record what shipped. This
skill is project-agnostic — all project-specific detail (what categories of idea to track, what
the priority tiers are, what's already been decided) lives in a file inside the project itself,
not in this skill. That file is what makes this skill reusable across every project rather than
rewritten per repo.

This file covers Steps 1-6, the steady-state propose/build/record loop. Seven companion files live
alongside it:

- `session-start.md` — Steps 0 through 0.7 (find/bootstrap the tracker, check whether Goals need a
  check-in, surface standalone reassess flags and due Rejected revisits). **Not optional** — read
  it every run, right after this intro, before Step 1. Split out purely to keep this file's
  common-case read focused on the propose/build/record loop.
- `setup.md` — the one-time-per-project bootstrap interrogation. Read it when `session-start.md`'s
  Step 0 finds no `IMPROVEMENT_TRACKER.md` yet.
- `strategies.md` — alternate ways of presenting candidates in Step 4, beyond the default
  single top pick. Read it when `Selection strategy:` is set to anything other than `top-tier`,
  or when setting/changing it.
- `feedback.md` — an optional loop that asks how past ships actually landed and feeds that back
  into future judgement. Read it whenever `Feedback:` isn't spelled out as `off`, or when
  setting/changing it. **This one defaults to `on`, so an absent line means read it** — see the
  read-gate note under the tracker format below.
- `risk-register.md` — an optional loop that traces which shipped ideas needed follow-up fixes or
  rework, persists that as a named risk area, and factors active risks into future proposals. Read
  it when `Risk register: on`, or when setting/changing it.
- `changelog.md` — what each skill version added, for telling an existing tracker what it's
  missing. Read it only when `session-start.md`'s version check finds a tracker's `Feature check:`
  behind the current skill version.
- `tracker-maintenance.md` — rare per-project edge cases (minting/migrating ids, retiring/merging/
  narrowing a category, one-time disclosures to an older tracker). Read it only when that specific
  trigger actually fires — each section names its own.

Of these, only `session-start.md` is unconditional. The other six are gated on their own trigger
condition, to keep the common-case read lean — note that `feedback.md`'s gate is satisfied by
default, so it's read on most runs too.

A project's tracker may also grow a sibling `IMPROVEMENT_TRACKER_DONE.md` — the overflow of old
**Done** history moved out of the live tracker (see Step 6). It's not a companion file of this
skill (no fixed content to read every run) and stays untouched unless something specifically
needs older shipped history.

A project with `Risk register: on` also has a sibling `RISK_REGISTER.md` — its own file, own id
space, own lifecycle, read/written per `risk-register.md`'s rules rather than this file's Step 0-6
loop.

## The tracker file

Each project that uses this skill has its own `IMPROVEMENT_TRACKER.md`, one per project — where
"project" means the directory containing its own code, not necessarily the overall repo root, since
a repo can hold several independent projects each with their own priorities. **`session-start.md`
Step 0 resolves where that file actually lives** (project root, the project's own docs directory,
or `.claude/`); don't assume a path here. This is the single source of truth: don't keep a separate
mental list of ideas or priorities, and don't split it across multiple files.

**This skill's other two files sit in whatever directory the tracker was found in** —
`IMPROVEMENT_TRACKER_DONE.md` (Step 6) and, with `Risk register: on`, `RISK_REGISTER.md`. They're
never resolved independently: they follow the tracker. One found somewhere else is worth surfacing
rather than quietly working around.

Format:

```markdown
# Improvement Tracker

## Goals (priority order, highest first)
Last reviewed: <YYYY-MM-DD>
Created: v<X.Y.Z>               <!-- skill version at setup time, stamped once, never changes -->
Feature check: v<X.Y.Z>         <!-- skill version last checked for new-feature disclosure -->
Next id: I<N>                  <!-- next unassigned idea id -->
Selection strategy: top-tier   <!-- optional, see strategies.md -->
Feedback: on                   <!-- optional, see feedback.md -->
Risk register: on              <!-- optional, see risk-register.md -->
Done archive: age=60, floor=5, backstop=40   <!-- optional, default shown, see Step 6 -->
1. <highest-priority tier>
2. <tier A> / <tier B> — tied; if a candidate must pick one, prefer: <tie-break rule>
3. <next tier>
...

## <Idea category A>
(dry runs: <N> — last: <YYYY-MM-DD>)  <!-- optional, only present after a dry top-up -->
- I7: **Idea name** — short rationale, referencing specific files/functions where useful.

## <Idea category B>
- ...

## Done
(archived before <YYYY-MM-DD>: see IMPROVEMENT_TRACKER_DONE.md)  <!-- optional, only present once an archive exists -->
- I7: **Idea name** (Category) — one-line note on what actually shipped (may differ from the
  original idea's exact wording if the implementation took a different shape).
- I12: **Idea name** (Category, fixes: I7, reassess: pending) — a later ship that fixes or
  reworks an earlier one carries the origin's id and flags the origin for reassessment.

## Rejected
- **Idea name** (Category, YYYY-MM-DD) — one-line reason it was declined.
- **Idea name** (Category, YYYY-MM-DD, revisit-after: YYYY-MM-DD) — a timing/priority reason
  carries an optional revisit date instead of relying on a coincidental re-proposal to catch it.
```

- **Goals** is an ordered list, highest priority first, with a `Last reviewed:` date. Earlier
  tiers dominate later ones when candidates trade off against each other; lower tiers only break
  ties among roughly-equal candidates. Edit this section directly to reprioritise, and bump
  `Last reviewed:` when you do — nothing else in this process needs to change when priorities
  shift. See Step 0.5 for how staleness gets surfaced automatically.
- **`Created:` and `Feature check:` are both skill-version stamps, distinct purposes.** `Created:`
  is set once at setup and never changes — a permanent record of what this tracker started life
  knowing about. `Feature check:` moves forward as new features get disclosed. Both are handled
  entirely by `session-start.md`'s Step 0/0.5 (including lazy-backfill of a tracker that predates
  them); nothing in Steps 1-6 reads or writes either.
- Two or more goals may share the same tier number when they're genuinely equal priority right
  now. A tied group must carry a short tie-break note on the same line: what to do when a real
  candidate serves one tied goal but not its sibling. If the user has no strong opinion, fall
  back to something concrete like "prefer whichever is cheaper/faster to build" or "ask me when
  it happens" — but prefer capturing their actual reasoning if they have one. Keep tie groups
  small (2, rarely 3); a tier that keeps growing tied entries is a smell that ranking has stopped
  meaning anything, and is worth flagging (see Step 0.5).
- `Selection strategy:`, `Feedback:`, `Risk register:`, and `Done archive:` are optional lines that
  may be absent. Their full format and behaviour live in `strategies.md`, `feedback.md`,
  `risk-register.md`, and Step 6 below respectively — don't inline their details here.
  **Gate reading each companion file on the setting's *value*, not on whether the line is
  present** — an absent line means that setting's documented default, and the defaults differ:
  `Selection strategy:` and `Risk register:` default to off (`top-tier` / `off`), so an absent line
  means don't read `strategies.md`/`risk-register.md`; `Feedback:` defaults to **on**, so an absent
  line means `feedback.md` *does* get read. Keying off presence instead would silently strand every
  tracker that simply never had reason to write the line, which defeats having a default at all.
- **Every idea gets an id** (`I<N>`) the moment it's added to a category (Step 2) — one counter
  for the whole tracker, tracked as `Next id:` under Goals, never reused. **Written as a leading
  `I<N>:` prefix on the line, not a trailing `(id: I<N>)`** — scanning a long category or Done list
  for a specific id is the common case, and a prefix reads left-to-right without having to parse
  into the parenthetical first. Rejected entries are the one exception: most have no id at all,
  so a leading `I<N>:` would misleadingly suggest every Rejected line has one — keep
  `id: I<N>` inside the parenthetical there, only when actually present. The id carries forward
  unchanged through Done (and into Rejected when it has one); it's what lets a later ship reference
  an earlier one reliably even after the earlier one's name gets reworded. An entry carrying no id
  at all is an expected steady state, not an error to flag — nothing mints one until something
  actually needs to reference it. **Minting and migration are all mechanical, and none of it is
  needed to run the normal loop** — an id-less entry that now needs referencing, a missing
  `Next id:`, an older tracker's trailing `(id: I<N>)` style, or a collision with a hand-typed id:
  see `tracker-maintenance.md`'s "Minting and migrating ids" at the point one of those actually
  comes up.
- **An id is for cross-referencing inside the files, never a substitute for the name in
  conversation.** Whenever an id gets said to the user — proposing a `fixes:`/`reworked:` origin,
  a reassess flag, a risk match or mitigation — say the idea's name or the risk's theme alongside
  it (`R3 — <theme>`, not bare `R3`); the id is what gets written into the tag, not what gets
  spoken. `session-start.md`'s reassess/revisit surfacing and `risk-register.md`'s
  cross-referencing wording already do this — the rule is to extend it everywhere else an id would
  otherwise stand alone, including this file's own Step 3 risk-mitigation wording below.
- **A ship that fixes or reworks an earlier Done item** tags itself with `fixes: I<N>` (bug fix) or
  `reworked: I<N>` (broader rework), referencing the origin's id — see Step 6. This also sets
  `reassess: pending` on the *origin* entry, standalone of whether `Feedback:` is on (see
  `feedback.md`'s and `session-start.md`'s handling of that flag). If `Risk register: on`, a
  `fixes:`/`reworked:` link is also one of the signals that can trigger a risk-area proposal — see
  `risk-register.md`.
- Idea category headers and names are entirely up to the project — there might be two, or
  five, and they might be called "Features"/"Refactors" or something far more specific to that
  project's domain. Discover them by reading the file; don't assume fixed category names.
- A category may carry an optional `(dry runs: N — last: DATE)` note right under its header —
  see Step 2 for when it's added, incremented, cleared, and surfaced to the user.
- **Retiring, merging, or narrowing a category** (offered at `dry runs: 2+`, see Step 2) and the
  Rejected-drop id-preservation rule that goes with it — rare per-project events, see
  `tracker-maintenance.md`.
- **Done** is append-only history, never deleted from. Prefix each entry with its origin
  category in parens — useful bookkeeping regardless of any optional subsystem; legacy entries
  without a tag just aren't counted by anything that relies on it, no migration needed.
- **Done grows unbounded over a project's life, so it's kept trimmed to a recent window in the
  live tracker, with the rest moved out to a sibling `IMPROVEMENT_TRACKER_DONE.md`** — same
  directory, same project, read only when Step 2's history-check or an explicit user question
  actually needs older history (see Step 6 for exactly when this move happens and what it must
  never move).
- **Rejected** is append-only, same as Done — an idea proposed in Step 2 and declined by the
  user goes here with the reason, not just dropped. See Step 2 for how this gets checked before
  re-proposing something similar; the reason is what matters, not the mere fact of rejection.
- **`revisit-after:` is optional, only for timing/priority reasons** ("not now, focused on X") —
  not for substance reasons ("doesn't fit," "already tried"), which don't go stale the same way and
  don't need a date. See Step 2 for when it's set and Step 1 for how it gets surfaced once due.
- **The file's top-level sections are closed: Goals, one `##` per idea category, Done, Rejected —
  nothing else.** Don't add a new `##` section for content that doesn't fit that shape (a
  design-discussion doc, a decision log, meeting notes, a roadmap), even when this file is already
  open and being edited and adding a section feels like the path of least resistance — that
  proximity is exactly why it happens and exactly why it's worth a hard no. Content like that
  dilutes the one thing this file is for and makes every future read slower (Step 2's history-check
  and every check-in scan the live sections). Point it at wherever the project already keeps that
  kind of content instead — `DEVELOPMENT.md`, a dedicated design doc, project docs — and only add a
  category if what's being recorded is genuinely idea-category shaped (a list of discrete,
  proposable, shippable ideas) — content that needs a different write target belongs in a
  different file, not squeezed into this one because it's already open. If a project's tracker
  already has a foreign section from before this rule existed, that's not
  silently fine either — see `session-start.md` Step 0's malformed-tracker handling, extended to
  this case.

**Hard rules by step, so a review can check none have gone missing.** Scope: rules that fail
*silently* if skipped — where nothing errors and no output looks wrong, so only this table would
ever reveal the omission. Two kinds qualify, marked in the **Kind** column: **gate** (show, then
wait for a go-ahead — skip it and the write just happens) and **surface** (tell the user something
unprompted — skip it and they simply never hear it). Rules that fail *visibly* are deliberately
absent: Step 2's "don't pad a thin category with filler" isn't here, because breaking it produces
visibly weak ideas the user can see for themselves. Absence from this table doesn't mean optional.

| Step | Kind | Hard rule |
|---|---|---|
| 0 (setup.md) | gate | Interrogate the proposed categories/tiers with the user before writing the initial tracker |
| 0 (setup.md) | surface | Disclose the behaviours that aren't opt-in (the fixes/reworks question, Done archiving) rather than letting them appear unannounced |
| 0 (session-start.md) | gate | If the tracker exists but is malformed, ask the user rather than silently rewriting or refusing |
| 0 (session-start.md) | surface | Flag a foreign `##` section once per project rather than leaving it unmentioned |
| 0 (risk-register.md) | gate | If `RISK_REGISTER.md` exists but is malformed, ask the user rather than silently rewriting or refusing |
| 0.5 (session-start.md) | gate | Confirm goal changes with the user before updating Goals / bumping `Last reviewed:` |
| 0.5 (session-start.md) | gate | Confirm before adjusting `Done archive:` knobs or `Feedback:`'s cadence knobs off the back of a detected drift signal |
| 0.5 (session-start.md) | surface | Raise a stale-Goals check-in when due, and a `Feature check:` version gap — including a missing stamp, walked as `0.0.0` — or an unexpectedly-ahead stamp |
| 0.6 (session-start.md) | surface | Surface standalone `reassess: pending` flags when `Feedback:` is explicitly `off` |
| 0.7 (session-start.md) | surface | Surface Rejected entries whose `revisit-after:` date has passed |
| 2 | gate | Show proposed new ideas, or a category retirement/merge/narrow, and wait for confirmation before writing anything |
| 2 | surface | Raise a category sitting at `dry runs: 2+` rather than silently polling it again |
| 2/4.5/6 (risk-register.md) | gate | Show a proposed risk-area creation or update (any trigger), and an archival/reactivation, and wait for confirmation before writing to `RISK_REGISTER.md` |
| 4 | gate | Do not start planning or implementing until the user confirms which one (if any) to build |
| 4 | surface | Flag a feature-type pick as such, and flag every candidate's risk-register signals (mitigates vs. merely exposed) |
| 4.5 | gate | Get the plan approved before writing any code |
| 6 | surface | Sweep Done into the archive whenever age/floor/backstop makes an entry eligible, not only when someone happens to notice |
| 0.5 (session-start.md) | surface | Re-run that same Done sweep independently of Step 6, so a missed append-time sweep gets caught at the next session start |
| Checking in (feedback.md) | surface | Always surface the pending-outcome count when it's nonzero, calling out the reassess subset separately |
| Checking on mitigations (risk-register.md) | surface | Say so the first time a `mitigated-by:` tag would be added while `Feedback:` is off, since nothing would ever ask about it |

*Update this table in the same edit whenever a hard rule is added, removed, or moved* — it's a
mirror of the steps, not independent prose, so it's the one place to check rather than several
scattered cross-references.

## Step 0 through Step 0.7: Find/bootstrap the tracker, check staleness, surface reassess flags and due revisits

Read `session-start.md` and follow it before continuing — it covers finding or bootstrapping the
tracker (including the malformed-tracker case), checking whether Goals are stale, (Step 0.6,
`Feedback: off` only) surfacing standalone reassess flags, and (Step 0.7) surfacing any Rejected
entries whose `revisit-after:` date has passed. This is the
one companion file that's read every run, not gated behind a trigger condition; see the intro
above for why it's split out. Once it says to, continue to Step 1 below.

## Step 1: Count what's outstanding

Count remaining (not-in-Done) items in each idea category.

**If `session-start.md`'s Step 0.7 flagged any due `revisit-after:` entries and the user chose to
reconsider one**, it goes back through Step 2 like any other candidate — confirm before appending,
reuse its existing id per the id-scheme note above.

## Step 2: Top up any category running low

If a category has fewer than ~3 items, or is empty, it needs fresh ideas before ranking makes
sense — there's nothing meaningful to weigh against the goals otherwise. The ~3 floor only
triggers a top-up; keep searching until the category reaches **~6-8 outstanding items**. This is a
target, not a quota — it raises how much ground to search, it never lowers the bar on any
individual idea (see "exhausted is a valid outcome" below), so a category with only 4 solid ideas
stays at 4. But stopping short of 6-8 needs a stated, concrete reason (e.g. "checked recent
commits, rough edges, and natural next-steps — only 4 solid candidates exist, the rest would be
filler") — a silent stop at 3-4 is exactly the undershoot this rule exists to prevent. Ground new
ideas in the project's actual current state rather than inventing from nowhere:

- What's been built or changed recently (recent commits, new modules, new files)?
- What's untested, fragile, or has a noted rough edge (TODO-style comments, test coverage gaps,
  anything flagged as a known issue in project docs or memory)?
- What's the natural next step after whatever just shipped?
- What did the user mention in passing that sounded like a want but wasn't captured yet?
- If `Feedback:` is on, factor recorded outcomes in too — see `feedback.md`.
- If `Risk register: on`, a rough edge that's actually a repeat/structural pattern (not just one
  isolated spot) is also a candidate risk-area proposal, not only a candidate idea — see
  `risk-register.md`'s Step 2 trigger.

**Assign an id when a proposed idea is actually appended.** Not at brainstorm time — only once the
user has confirmed it's going in (see the confirmation rule below), take the current `Next id:`
value, write it onto the new entry, and bump the counter. Declined ideas that go to Rejected don't
consume an id — **unless the idea already has one**, e.g. it was outstanding, dropped to Rejected
(a category retirement, or a plain decline of something already appended), and is now being
proposed again: reuse its existing id rather than minting a new one for what's the same idea
reappearing, so anything that referenced it by id (a `mitigated-by:` tag, a `fixes:` link) still
resolves correctly. Only mint fresh for an idea that's never been appended before.

**If `Risk register: on`, cross-reference each candidate against active risk areas** before
presenting it — read `RISK_REGISTER.md`'s active entries and check whether the candidate touches
the `areas:` of one **or more**, using `risk-register.md`'s "The area match" test (that's the one
definition of touching; don't improvise a second) and checking all active entries rather than
stopping at the first hit. If any
match, say so when presenting it (see `risk-register.md`) rather than leaving the match implicit,
and ask whether the candidate is merely exposed to the risk or specifically meant to fix it. Only
the "meant to fix it" answer writes anything — a `mitigated-by: ... (outcome: planned)` tag, made
in the same write as appending the idea itself. Mere exposure is recomputed from the areas every
time and is never recorded (see `risk-register.md`'s Cross-referencing new ideas section).

**Check Rejected before proposing.** If a candidate closely resembles something already in
Rejected, don't just skip it or blindly re-propose it — read the recorded reason and judge
whether it still applies. A timing/priority reason ("not now, focused on X") can go stale and
stop applying; a substance reason ("doesn't fit this project," "already tried, didn't work")
usually doesn't. When genuinely unsure, it's fine to re-propose with a note ("this was declined
before for X — has that changed?") rather than silently suppressing or silently repeating it.

**Same check, extended to "already shipped."** A candidate can also closely resemble something
already in **Done** — check the live tracker's Done section same as Rejected. If it's plausible
but not certain the same thing already shipped, and `IMPROVEMENT_TRACKER_DONE.md` exists (see
Step 6), it's fine to open it for this one lookup rather than guessing — that's exactly the kind
of "something actually needs older history" case Step 6 has in mind, not a normal-loop read.

**Show the proposed new ideas and wait for confirmation before appending anything.** This is one
of the skill's hard rules (see the table above): brainstorming is a recommendation, not a
decision — the user may accept all of it, drop some, tweak wording, or say none of it's worth
keeping. Don't write to
the tracker until they've had a chance to react. Whatever gets declined, add it to **Rejected**
with the reason given (or your best summary of it if the user was terse) — don't just drop it
silently, that's what lets the check above work next time. **If the reason is timing/priority-based
rather than substance**, ask for (or suggest) a rough `revisit-after:` date — "worth checking again
in a month or two, or should I just re-check whenever it comes up again?" — and store it if they
give one; a substance-based decline gets no such field, per the Rejected-format note above. Match
that file's existing format and voice for whatever does get appended. Don't pad a thin category
with filler just to hit a count:
if there are only one or two solid ideas, say so and move on rather than inventing weak ones. If
`Selection strategy:` includes `wildcard(tagged)`, see `strategies.md` for the idea-tagging
convention that mode depends on.

**Exhausted is a valid outcome, not a failure to fix.** If brainstorming (grounded in the checks
above) turns up nothing genuinely new or worth building, say so explicitly rather than quietly
lowering the bar until something fills the slot. When declaring a category exhausted, tell the
user *why*, concretely — e.g. "checked recent commits, open rough edges, and what shipped last —
everything that fits '<category>' either already shipped or the remaining candidates are
marginal/duplicate/out of scope." A vague "nothing comes to mind" isn't enough; the reasoning is
what lets the user judge whether the category's actually done or the search just wasn't broad
enough.

**Track dry top-ups so they don't repeat silently** — a self-correcting counter (increment on the
miscalibration signal, reset on the corrected one, force-reset once surfaced): note it inline under
that category's header, `(dry runs: N — last: YYYY-MM-DD)`. Trigger/increment: a top-up attempt ends up
adding nothing — brainstorming found nothing genuinely new, everything proposed was flagged weak,
or the user declined what was proposed. Corrected signal/reset: the next time a solid idea actually
gets added, remove the line entirely. Threshold: at `dry runs: 2+`, surface this to the user up
front the next time this category comes up — e.g. "Features has been topped up 2 times with
nothing solid since <date> — possible this category is genuinely done; want to retire/merge it,
narrow its scope, or keep polling?" (see `tracker-maintenance.md` for the mechanics of whichever
they pick) — and force-reset by removing the line once surfaced,
regardless of which answer they give, so "keep polling" doesn't re-nag on the very next dry
attempt; it takes two fresh dry runs to surface again.

## Step 3: Rank candidates against the tiers

Take the union of outstanding items across every idea category (freshly topped-up or not) and
weigh them against the Goals list **in order** — a candidate serving tier 1 beats one serving
only tier 3, even if the tier-3 one is cheaper or more appealing to build. Lower tiers only
break ties between candidates that are roughly equal on every tier above them. The last tier is
usually a filter rather than a tiebreaker: if nothing outstanding is genuinely compelling right
now, say that instead of picking something just to have an answer.

Think concretely about each candidate: what would actually happen if it were built, and which
tier does that outcome serve? Don't take a category label at face value — a "refactor" that
doesn't make anything more readable or any future feature easier doesn't serve the maintenance
tier just because it's filed under that category.

**Don't cite a factor in Step 4's reasoning that didn't actually decide anything.** It's tempting
to add color like "this one's been sitting in the backlog a while" when presenting a pick — but
unless that's an actual tie-break input in play (`wildcard(oldest)` explicitly uses idea age;
nothing else here does by default), saying it implies it mattered when it didn't. Only mention a
factor if it's tier fit, a genuine synergy (below), or an active strategy signal that actually
swung the pick.

**If `Risk register: on`, a candidate that mitigates an active risk is a distinct, stronger signal
than synergy** — it's not "these two ideas help each other," it's "this specific candidate is what
an already-persisted risk area names as its mitigation," which was itself already confirmed through
its own gate when the risk entry was created. This covers a candidate tagged `mitigated-by:
... (outcome: planned)` (proposed at Step 2 specifically as the fix, not yet built) the same as one
already shipped and proven `effective` — both are "this candidate is the named fix," just at
different lifecycle stages; word the reasoning accordingly ("this is the planned fix for
R3 — <theme>" vs. "this already proved effective against R3 — <theme>" if it's a repeat build).
Keep the reasoning text distinct: "mitigates R3 — <theme>" is a different claim than "also lays
groundwork for Y," and a candidate
that merely touches an active risk's areas (exposed to it, not building against it) is a caution
flag, not a tie-break in its favour — don't conflate the three in Step 4's presentation.

**Synergies are a soft signal, judged fresh each run, not tracked data.** While ranking, notice if
a candidate is a genuine stepping stone toward another outstanding candidate, would make one
noticeably easier, or shares real implementation with it — but only when it's concrete (name the
actual shared file/module/step), never a vague "these feel related." A tier-3 idea that happens to
set up a tier-1 idea is still tier-3 for ranking purposes; the synergy is worth mentioning in Step
4, not worth re-tiering it over. Nothing here gets written to the tracker — it's noticed and
reasoned about at ranking time from whatever's actually outstanding, so there's no annotation to
keep in sync as ideas get reworded, merged, or shipped.

It's scoped as narrowly as `category-rotation` (see `strategies.md`): it only breaks the base
pick's own close call, never a tie within one of `spread(N)`'s individual per-tier picks — a tie
that narrow is left as-is rather than resolved by either signal.

**Precedence when several of these signals bear on the same within-tier close call.** This is the
canonical ordering — everywhere else that mentions one of these defers here rather than restating
it:

1. **A tied tier's stored tie-break rule** always wins when it applies — it's the user's explicit,
   deliberate call, and everything below is a fallback that only kicks in when no such rule is in
   play.
2. **Risk-mitigation** beats the rest: it's a previously-confirmed judgement that this specific
   problem needs addressing, not a generic heuristic.
3. **Synergy** next — grounded in something concrete about the actual candidates (a named shared
   file/module/step).
4. **`category-rotation`**, if active (`strategies.md`) — last, since it's a content-blind
   diversity heuristic, and concrete beats generic.

None of these ever promotes a candidate across tiers; they only break ties *within* one.

**Tied tiers**: evaluate candidates against every goal in the tied group, not just one.
- If a candidate serves all goals in the tie equally (or none of them), there's no conflict —
  rank it normally against the other tiers.
- If candidates split — one serves goal A of the tie, another serves goal B — that's exactly
  the case the tie's stored tie-break rule exists for. If the rule is concrete (e.g. "cheaper
  wins"), apply it mechanically and rank the winner. If the rule says "ask me", or no rule was
  stored (a tracker predating this feature, or a same-number tier that was a typo), don't
  resolve it silently — carry both candidates forward as co-contenders into Step 4.

This ranking is what Step 4 presents from. If `Selection strategy:` is set to something other
than plain `top-tier`, `strategies.md` changes *how* the ranking gets presented, never how it's
computed — this step stays the same either way. If `Feedback:` is on, weigh recorded outcomes
qualitatively when judging candidates here too — see `feedback.md`.

## Step 4: Propose, then wait

**Whenever more than one option is presented, number them `1.`, `2.`, `3.`... in a single
sequential list, in the order listed below** — regardless of strategy (top-tier close
contenders, spread's tier picks, wildcard/quick-win additions, tied-goal co-contenders). This is
so the user can confirm by number ("go with 2") instead of by re-typing a name. Any descriptive
label a mode adds (`Tier 1 pick:`, `Wildcard:`, `Quick win:`) stays as text within that numbered
line — it's a label, not the list number. A single, unambiguous top pick with nothing else to
choose between doesn't need a number, since there's no distinct option to point at.

Default (no `Selection strategy:` set, or set to plain `top-tier`): present the top candidate,
or up to 4 total (winner + close contenders) if the ranking is genuinely close, with reasoning
tied to specific tiers — not "this seems good" but "this serves tier 1 because X" or "this is
tier-3 maintenance work but nothing above it is ready to build, since Y." The close-contender cap
is configurable (`max-options(N)`) — see `strategies.md`. If Step 3 noticed a genuine, concrete
synergy with another outstanding candidate, mention it here too ("this also lays the groundwork
for Y") — it's part of the reasoning, not a separate line item.

**Flag risk-register signals explicitly, and don't conflate them.** If `Risk register: on`, check
**every candidate being presented this round** — not just the top pick, every numbered option in a
multi-option list (close contenders, `spread(N)` tier picks, wildcard, quick-win alike) — against
active risk areas (same area match as Step 2). One that mitigates an active risk gets flagged
plainly ("this also mitigates R3 — <theme>"). One that merely touches an active entry's areas
without building against them gets flagged too, but as a caution, not a point in its favour ("this
touches R3's risk area — worth extra care on <what the risk actually is>"). A match that came out
borderline, or an area that no longer resolves, gets said as such rather than rounded to yes or no. Use the wording that
matches which one actually applies for each candidate, per Step 3's distinction.

If `Selection strategy:` is set to anything else, read `strategies.md` and build the
presentation as it describes instead.

**Flag feature-type picks explicitly.** If the top pick (or a close contender) comes from a
features/new-functionality category rather than maintenance/quality/refactor-style work, say so
plainly as part of its reasoning line (e.g. "this is a new feature, not a maintenance item — ...")
rather than leaving the category implicit. This doesn't change the presentation format above or
add a new confirmation gate — it's one clause within the existing line, same as any other
reasoning. The reason it's worth calling out: users tend to want more direct say over feature
scope/direction than over maintenance work, and Step 4.5's plan-approval step is where that
input actually happens — flagging it here just makes sure the user notices *before* reaching that
step, instead of registering it only once a plan is already drafted.

If Step 3 carried forward an unresolved tied-goal conflict, present that as its own distinct
case regardless of strategy — the user needs to know which situation they're looking at, and the
co-contenders still get numbered like any other multi-option list. E.g.: "X and Y are
tied-priority — which matters more for this one? 1. Candidate A (serves X) 2. Candidate B
(serves Y)." Close contenders are about candidates scoring similarly; a tied-goal conflict is
about the tier ranking itself being unable to pick a winner.

**Do not start planning or implementing until the user confirms which one (if any) to build.**
This is one of the skill's hard rules (see the table above): the ranking is a recommendation, not
a decision. The user may pick something other than the top candidate, ask for a different
combination, or say none of it is worth doing right now — all of those are fine outcomes.

## Step 4.5: Plan the confirmed pick

A confirmed idea is still just an idea — don't jump straight to code. Produce a detailed
implementation plan first: what files/functions get touched, the approach, and how it'll be
verified. **This is one of the skill's hard rules (see the table above): get the plan approved
before writing any code.**

If Claude Code's plan mode is available in this session, use it naturally for this (EnterPlanMode
/ ExitPlanMode) — write the plan to the plan file and call ExitPlanMode to request approval. If
plan mode isn't available or doesn't fit the context, present the plan inline instead and wait
for an explicit go-ahead before proceeding.

Keep the plan proportional to the work — a one-line fix doesn't need the same ceremony as a
multi-file feature. Use judgement on how much detail is actually useful rather than padding every
plan to a fixed template.

If the user asks for changes to the plan, revise and re-confirm before moving to Step 5 — that's
iterating on the same plan within the same session, not a persistence question.

If the user declines the plan outright rather than asking for changes ("actually, let's not do
this after all"), that's not a Step 6 outcome and not a Rejected outcome either — a plan getting
declined doesn't retroactively unpick or reject the idea itself, which is still perfectly valid,
just not being built right now. Leave it as-is in its category; it goes back through Step 3's
ranking next time like anything else outstanding.

**If planning surfaces a risk that wasn't already known** (e.g. scoping the work exposes fragile
coupling, an untested assumption, a structural weak point), and `Risk register: on`, propose a
risk-area entry right here rather than waiting for a future fix to retroactively prove the pattern
— same confirm gate as any other risk-register write, see `risk-register.md`.

**Always plan fresh; don't reuse an old plan for an idea that gets picked again later.** If a
candidate was proposed, planned, and then declined or shelved in an earlier session, and the same
idea comes up again now, write a new plan grounded in the project's current state rather than
resurrecting the old one — the codebase may have changed since (other ideas shipped, files
moved, dependencies shifted), and a stale plan silently reused is the same risk this skill
already guards against elsewhere (dry-run tracking, goal staleness, feedback outcomes: don't
trust a cached judgement, re-ground it). Plan-mode plan files aren't tracked by or referenced from
the tracker for this reason.

## Step 5: Build it

Once the plan is approved, implement it as planned — this skill only changes how the work item
was chosen and planned, not how you write code, run tests, or verify changes. Follow whatever
conventions the project's own docs/CLAUDE.md/memory already establish. If reality diverges from
the plan enough to matter, say so rather than silently deviating.

## Step 6: Record what shipped

Move the item from its origin category to **Done** in that project's tracker, with a one-line
note on what was actually built. If `Feedback: on`, see `feedback.md` for the extra tagging to
add at this step. Leave everything else in the file untouched. If the work surfaced new
follow-on ideas that weren't there before, add them to the relevant category now rather than
losing them — that's the loop closing, not scope creep.

**Ask whether this ship fixes or reworks an earlier one.** Every recording, ask directly — with an
auto-detect suggestion, not a blind open question: scan recent Done entries (and the branch/commit
context, if this session touched a specific bug or reopened specific files) for a plausible origin,
propose it, and let the user confirm, correct, or say no.

If `Next id:` was missing before this recording, this is the first time this project has ever been
asked — give the one-time heads-up in `tracker-maintenance.md` before asking.

If confirmed:
- Tag the new entry `fixes: I<N>` (bug fix) or `reworked: I<N>` (broader rework), referencing the
  origin's id (if the origin has no id, mint one for it now — see `tracker-maintenance.md`).
- Set `reassess: pending` on the **origin** entry — **in whichever file it actually lives in**, per
  the combined-pool rule below; Done-trimming can move an origin to the archive long before anyone
  fixes it. This is standalone of `Feedback:` — it
  applies whether or not the feedback subsystem is on. See `feedback.md` (Feedback on: folded into
  its check-in, prioritised over routine outcome asks) and `session-start.md` (Feedback off: a
  lightweight one-off surfacing, no persistent answer required).
- If `Risk register: on`, this link also feeds three of `risk-register.md`'s own Step-6-triggered
  checks, each with its full mechanics already documented there rather than repeated here: a
  creation/update trigger (its "Creating or updating an entry," trigger 1), whether the origin's id
  is itself a `mitigated-by:` entry (its "A mitigation needing its own fix"), and whether this
  ship's own id is a `mitigated-by: ... (outcome: planned)` entry on some risk (its "Recording a
  planned mitigation").

If the user says this ship is *not* a fix/rework of anything, or the auto-detect had nothing
plausible, record the ship normally with no `fixes:`/`reworked:` tag — don't force a link that
doesn't exist.

**A clean ship (no `fixes:`/`reworked:` tag) in an active risk entry's areas is counter-evidence
against that risk** — nothing to record for it, since exposure was never stored; it's read out of
Done whenever archival is next considered. See `risk-register.md`'s archival trigger.

**After appending, check whether Done needs trimming.** This isn't the only place this sweep runs —
`session-start.md` Step 0.5 re-derives the same eligibility independently at the start of every
session, so a sweep this step fails to complete (a session ending early, a hand-edited tracker, an
older tracker predating `Done archive:`) still gets caught rather than leaving Done to grow
unbounded with nothing left to trigger it. Primary trigger is age, not count — how
long ago something shipped is what determines whether it's still useful working context, not how
many entries happen to sit next to it (a project shipping in bursts can produce 20 genuinely-recent
entries in two weeks that are all still relevant; a slow project can carry 10 stale ones for a
year). Archive any Done entry whose `shipped` date is older than `Done archive:`'s `age` (default
60 days). **Always keep the most recent `floor` entries live regardless of age** (default 5), so a
dormant project that just resumed doesn't get its Done section swept to empty. **Count stays as a
backstop only**: if the live section still exceeds `backstop` entries (default 40) after the age
sweep — a burst of very recent ships — archive the oldest down to `floor` by age regardless, so one
hyperactive stretch can't leave the file unbounded between age-sweeps. Move archived entries,
unedited and in their existing order, to the end of `IMPROVEMENT_TRACKER_DONE.md` (create it, same
directory as `IMPROVEMENT_TRACKER.md`, with a one-line `# <Project> — archived Done history` header
if it doesn't exist yet). Update the archive-pointer note under the live `## Done` header to the
cutoff date of the oldest entry now remaining live. This is mechanical bookkeeping, not a judgement
call about ideas or priorities, so it doesn't need user confirmation the way Steps 2/4/4.5 do —
only the knob *adjustment* below is confirm-gated, not the routine sweep itself.

**Track which trigger actually fired, to catch a miscalibrated `age`** — a self-correcting counter,
same shape as Step 2's dry-run tracking: note inline on the `Done archive:` line which kind of
sweep just ran, `(last sweep: backstop, streak: N)` or `(last sweep: age, streak: 0)`. **If the
`Done archive:` line isn't present** (the normal case — it's absent whenever the defaults haven't
been changed), write it out with its default values first and annotate that, rather than dropping
the note somewhere else or silently skipping the tracking; there's no other line it belongs on. Trigger/increment: a `backstop` sweep. Corrected signal/reset: an
`age` sweep, back to 0. Threshold: at `streak: 3` (three backstop-triggered sweeps in a row with
`age` never once catching anything first), surface it at the next `session-start.md` Step 0.5
check-in — `age` is calibrated for a slower project than this one is actually shipping at, propose
halving it (or raising `backstop`) with a concrete number, wait for confirmation before writing
(this is a hard rule — see the table above) — and force-reset the streak once surfaced regardless
of the answer, same as Step 2's dry-run counter.

**Trimming doesn't wait on `outcome`** (`Feedback: on` — see `feedback.md`). Archive eligible-by-age
entries regardless of whether their outcome is still `pending` — otherwise a feedback loop that
can't keep pace with shipping would let the live Done section grow without bound. An entry crossing
into the archive while still `pending` doesn't drop out of consideration, per the combined-pool
rule below — it's still askable, just from the other file.

`category-rotation` (`strategies.md`) counts only the live tracker's Done entries, never the
archive — its default window (5) is well inside the default `floor`-`backstop` range kept live, so
this practically never runs short, but if a project sets a much larger window than the live Done
section holds, treat it the same as "fewer than N total" (insufficient history, skip the bias)
rather than reading the archive file to fill the count.

**Reading the archive.** Only open `IMPROVEMENT_TRACKER_DONE.md` when something actually needs
older history; otherwise don't read it as part of the normal Step 0-6 loop, since that's most of
the point of moving entries out of the live tracker. **When something does need it, the rule is
always the same one — treat the live tracker's Done section and the archive as one combined pool**,
never just the live file: the count is the sum, "oldest" is the oldest across both, and a write
lands in whichever of the two the entry actually sits in. Everywhere else that scans Done history
means this rule, and defers here rather than restating it — Step 2's "has something like this
already shipped" check, Step 6's `reassess:` write to an origin entry, the user asking about past
work, `feedback.md`'s eligible-entry scan, and `risk-register.md`'s evidence scan. Archiving is
purely about what gets loaded on a routine run; it never narrows what a deliberate history lookup
is allowed to see.

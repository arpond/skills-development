---
name: next-improvement
description: Runs a "what should we work on next" process for whatever project the user is currently in — maintains a per-project IMPROVEMENT_TRACKER.md (idea categories + a tiered priority list), tops up any category that's run low by brainstorming fresh ideas grounded in that project's actual current state, ranks candidates against the project's own configured tiers, and proposes the next thing to build for the user to confirm before any code changes happen. Bootstraps the tracker itself on first use if the project doesn't have one yet. Use this whenever the user asks "what should we do next" / wants to pick the next feature or refactor / asks to poll for more ideas / mentions an improvement tracker or backlog, or when a work session is starting on a project with no specific task queued up yet.
---

# Next improvement

A repeatable "what next" loop: keep a running list of ideas per project, top the list up when
it runs thin, pick the next thing to build by weighing it against that project's own standing
priorities, confirm with the user, plan it in detail, build it, then record what shipped. This
skill is project-agnostic — all project-specific detail (what categories of idea to track, what
the priority tiers are, what's already been decided) lives in a file inside the project itself,
not in this skill. That file is what makes this skill reusable across every project rather than
rewritten per repo.

This file covers Steps 1-6, the steady-state propose/build/record loop. Four companion files live
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
  into future judgement. Read it when `Feedback: on`, or when setting/changing it.
- `risk-register.md` — an optional loop that traces which shipped ideas needed follow-up fixes or
  rework, persists that as a named risk area, and factors active risks into future proposals. Read
  it when `Risk register: on`, or when setting/changing it.

Of these, only `session-start.md` is unconditional — the other four are read only when their
trigger condition says to, to keep the common-case read lean.

A project's tracker may also grow a sibling `IMPROVEMENT_TRACKER_DONE.md` — the overflow of old
**Done** history moved out of the live tracker (see Step 6). It's not a companion file of this
skill (no fixed content to read every run) and stays untouched unless something specifically
needs older shipped history.

A project with `Risk register: on` also has a sibling `RISK_REGISTER.md` — its own file, own id
space, own lifecycle, read/written per `risk-register.md`'s rules rather than this file's Step 0-6
loop.

## The tracker file

Each project that uses this skill has its own `IMPROVEMENT_TRACKER.md` at that project's root
(i.e. the directory containing its own code, not necessarily the overall repo root — if you're
working in `some-repo/some-project/`, the tracker lives at `some-repo/some-project/IMPROVEMENT_TRACKER.md`,
not at the top of the whole repo, since a repo can hold several independent projects each with
their own priorities). This is the single source of truth: don't keep a separate mental list of
ideas or priorities, and don't split this across multiple files — one tracker per project.

Format:

```markdown
# Improvement Tracker

## Goals (priority order, highest first)
Last reviewed: <YYYY-MM-DD>
Next id: I<N>                  <!-- next unassigned idea id -->
Selection strategy: top-tier   <!-- optional, see strategies.md -->
Feedback: on                   <!-- optional, see feedback.md -->
Risk register: on              <!-- optional, see risk-register.md -->
1. <highest-priority tier>
2. <tier A> / <tier B> — tied; if a candidate must pick one, prefer: <tie-break rule>
3. <next tier>
...

## <Idea category A>
(dry runs: <N> — last: <YYYY-MM-DD>)  <!-- optional, only present after a dry top-up -->
- **Idea name** (id: I7) — short rationale, referencing specific files/functions where useful.

## <Idea category B>
- ...

## Done
(archived before <YYYY-MM-DD>: see IMPROVEMENT_TRACKER_DONE.md)  <!-- optional, only present once an archive exists -->
- **Idea name** (Category, id: I7) — one-line note on what actually shipped (may differ from the
  original idea's exact wording if the implementation took a different shape).
- **Idea name** (Category, id: I12, fixes: I7, reassess: pending) — a later ship that fixes or
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
- Two or more goals may share the same tier number when they're genuinely equal priority right
  now. A tied group must carry a short tie-break note on the same line: what to do when a real
  candidate serves one tied goal but not its sibling. If the user has no strong opinion, fall
  back to something concrete like "prefer whichever is cheaper/faster to build" or "ask me when
  it happens" — but prefer capturing their actual reasoning if they have one. Keep tie groups
  small (2, rarely 3); a tier that keeps growing tied entries is a smell that ranking has stopped
  meaning anything, and is worth flagging (see Step 0.5).
- `Selection strategy:`, `Feedback:`, and `Risk register:` are optional lines, absent by default.
  Their full format and behaviour live in `strategies.md`, `feedback.md`, and `risk-register.md`
  respectively — don't inline their details here, and don't read those files unless one of them
  is actually present/being set up.
- **Every idea gets an `id:`** (`I<N>`) the moment it's added to a category (Step 2) — one counter
  for the whole tracker, tracked as `Next id:` under Goals, never reused. The id carries forward
  unchanged through Done and Rejected; it's what lets a later ship reference an earlier one
  reliably even after the earlier one's name gets reworded. **Migrating an older tracker that
  predates this field is lazy, not a bulk pass**: if `Next id:` is missing, initialize it (from 1,
  or from the highest existing id + 1 if some entries already have one) the first time anything
  actually needs it — same non-judgement mechanical bookkeeping as Step 6's Done-trimming, no
  confirmation needed. **This same rule covers any id-less entry, not just ones from before this
  feature existed** — including one someone added or edited by hand without following the format.
  Such entries stay id-less until something specifically needs to reference them (a `fixes:` link,
  an `at-risk:` list, a reassess flag) — at that point mint the next counter value for that one
  entry in place, same precedent as Done's legacy-tag handling below; don't rewrite every existing
  entry just because the field now exists, and don't treat a missing id as a malformed-tracker case
  either (contrast `session-start.md`'s Step 0 malformed-tracker handling) — it's the expected
  steady state for anything that hasn't needed a reference yet, not an error to flag.
  **Before minting any id** (lazy-backfill or a fresh Step 2 append), check it isn't already in use
  anywhere in the tracker — a hand-typed `id: I5` can exist on some entry while `Next id:` is still
  sitting at `I5` or lower, e.g. from manual editing. If the value about to be minted collides,
  skip forward past every id already in use (checking the live tracker, and
  `IMPROVEMENT_TRACKER_DONE.md`/`RISK_REGISTER.md` if either exists) and mint the first free one
  instead, then set `Next id:` to one past whatever got minted — this is the same mechanical,
  no-confirmation bookkeeping as the rest of id assignment, not a new judgement call.
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
- **Retiring or merging a category** (offered at `dry runs: 2+`, see Step 2): if the user
  confirms retirement, delete that category's `##` header and its (by then empty, or otherwise
  moved) item list from the active section — but never touch **Done**/**Rejected** entries
  already tagged with that category name; they're history, not live state, and stay exactly as
  written. If the user confirms a merge into an existing category instead, move any remaining
  outstanding items under the surviving category's header (dropping the retired one), and don't
  rewrite old Done/Rejected tags to the new name — a mismatched historical tag is expected and
  fine, not a bug to fix. **Narrowing scope instead** means renaming the category's `##` header to
  a more specific name (the tracker format has no separate scope/description field — the name
  *is* the scope) and treating that narrower name as the brief for future brainstorming in Step 2;
  existing outstanding items stay under it unless they no longer fit, in which case handle them
  like any other Step 2 judgement call (re-propose to a different category, or drop with a
  Rejected note) rather than silently discarding them. All three (retire, merge, narrow) are still
  a write to the tracker and need confirmation first, same as any other Step 2 change (see the
  hard-rules table). **Preserve the id on a dropped item's Rejected note** (`(Category, YYYY-MM-DD,
  id: I<N>)`) if it already had one — an outstanding idea can be referenced from elsewhere (a risk
  entry's `at-risk:` list) purely by id, and dropping it to Rejected doesn't retract that reference;
  if `Risk register: on`, also remove the id from any `at-risk:` list it appears on, same as any
  other idea leaving the outstanding pool (see Step 6's clean-ship handling for the parallel case).
  **This applies to any outstanding idea dropped to Rejected, not just a category-retirement drop**
  — including one tagged `mitigated-by: ... (outcome: planned)` on a risk entry (`risk-register.md`):
  if the idea it names is dropped instead of shipped, remove that `mitigated-by:` tag too rather
  than leaving a dangling reference to a fix that will never ship.
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

**Hard rules by step, so a review can check none have gone missing:**

| Step | Hard rule |
|---|---|
| 0 (setup.md) | Interrogate the proposed categories/tiers with the user before writing the initial tracker |
| 0 (session-start.md) | If the tracker exists but is malformed, ask the user rather than silently rewriting or refusing |
| 0 (risk-register.md) | If `RISK_REGISTER.md` exists but is malformed, ask the user rather than silently rewriting or refusing |
| 0.5 (session-start.md) | Confirm goal changes with the user before updating Goals / bumping `Last reviewed:` |
| 2 | Show proposed new ideas, or a category retirement/merge/narrow, and wait for confirmation before writing anything |
| 2/4.5/6 (risk-register.md) | Show a proposed risk-area creation or update (any trigger), and an archival/reactivation, and wait for confirmation before writing to `RISK_REGISTER.md` |
| 4 | Do not start planning or implementing until the user confirms which one (if any) to build |
| 4.5 | Get the plan approved before writing any code |

*Update this table in the same edit whenever a hard rule is added, removed, or moved* — it's a
mirror of the steps, not independent prose, so it's the one place to check rather than three
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
sense — there's nothing meaningful to weigh against the goals otherwise. The ~3 floor is only the
*trigger* for starting a top-up, not the stopping point — don't stop searching once the count
clears 3. Keep searching until the category reaches **~6-8 outstanding items**, and don't stop
short of that range without a concrete reason. If you stop before reaching 6-8, say explicitly
why (e.g. "checked recent commits, rough edges, and natural next-steps — only 4 solid candidates
exist, the rest would be filler") — a silent stop at 3-4 is exactly the undershoot this rule
exists to prevent. This is a target, not a quota: it raises how much ground to search before
stopping, it never lowers the bar on any individual idea (see "exhausted is a valid outcome"
below) — a category that only has 4 solid ideas stays at 4, but that must be a stated, evidenced
conclusion, not a default stopping point. Ground new ideas in the project's actual current state
rather than inventing from nowhere:

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
reappearing, so anything that referenced it by id (an `at-risk:` list, a `fixes:` link) still
resolves correctly. Only mint fresh for an idea that's never been appended before.

**If `Risk register: on`, cross-reference each candidate against active risk areas** before
presenting it — read `RISK_REGISTER.md`'s active entries and check whether the candidate's
category/theme matches one **or more** (check all active entries, not just until the first hit).
If any match, say so when presenting it (see `risk-register.md`) rather than leaving the match
implicit, and ask whether the candidate is merely exposed to the risk or specifically meant to fix
it — the answer decides whether it lands on that risk area's `at-risk:` list or its `mitigated-by:`
list as a `planned` mitigation, not both (see `risk-register.md`'s Cross-referencing new ideas
section). Either way, the write happens in the same write as appending the idea itself.

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

**Track dry top-ups so they don't repeat silently.** When a top-up attempt ends up adding
nothing — brainstorming found nothing genuinely new, everything proposed was flagged weak, or
the user declined what was proposed — note it inline under that category's header:
`(dry runs: N — last: YYYY-MM-DD)`. Increment on each dry attempt; reset to nothing (remove the
line) the next time a solid idea actually gets added. At `dry runs: 2+`, surface this to the user
up front the next time this category comes up — e.g. "Features has been topped up 2 times with
nothing solid since <date> — possible this category is genuinely done; want to retire/merge it,
narrow its scope, or keep polling?" — rather than letting the same empty search repeat forever
unnoticed.

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
different lifecycle stages; word the reasoning accordingly ("this is the planned fix for R3" vs.
"this already proved effective against R3" if it's a repeat build). It still only breaks ties within
a tier, never
promotes across tiers, same as synergy — but when a risk-mitigation signal and a synergy signal
disagree on the same close call, risk-mitigation wins (see `strategies.md`'s `category-rotation`
precedence note, which covers all of tie-break rule / synergy / risk-mitigation / category-rotation
together). Keep the reasoning text distinct regardless: "mitigates R3" is a different claim than
"also lays groundwork for Y," and a candidate that's merely `at-risk:`-tagged (exposed to a risk,
not building against it) is a caution flag, not a tie-break in its favour — don't conflate the
three in Step 4's presentation.

**Synergies are a soft signal, judged fresh each run, not tracked data.** While ranking, notice if
a candidate is a genuine stepping stone toward another outstanding candidate, would make one
noticeably easier, or shares real implementation with it — but only when it's concrete (name the
actual shared file/module/step), never a vague "these feel related." Where it's genuinely true,
use it the same way a tied-goal's tie-break rule is used: to break a tie between candidates that
are already close within a tier, never to promote a candidate across tiers — a tier-3 idea that
happens to set up a tier-1 idea is still tier-3 for ranking purposes; the synergy is worth
mentioning in Step 4, not worth re-tiering it over. Nothing here gets written to the tracker —
it's noticed and reasoned about at ranking time from whatever's actually outstanding, so there's
no annotation to keep in sync as ideas get reworded, merged, or shipped. If `category-rotation` is
also active and points at a different candidate for the same close call, see its precedence rule
in `strategies.md` — a stored tie-break rule beats both, and synergy beats category-rotation when
the two disagree. Scoped the same way `category-rotation` is: it breaks the base pick's own close
call, not a tie within one of `spread(N)`'s individual per-tier picks — a tie that narrow is left
as-is rather than resolved by either signal.

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
active risk areas. One that mitigates an active risk gets flagged plainly ("this also mitigates
R3 — <theme>"). One that's merely `at-risk:`-tagged (touches a category with an active risk but
isn't building against it) gets flagged too, but as a caution, not a point in its favour ("this
touches R3's risk area — worth extra care on <what the risk actually is>"). These are two
different claims; use the wording that matches which one actually applies for each candidate — see
`risk-register.md`.

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

**One-time heads-up on a tracker that predates this feature.** If `Next id:` was missing before
this recording (the lazy-init case, tracker-format section above) — meaning this is the first time
this project has ever seen this question — say so in one clause before asking it, e.g. "(this
tracker's picking up a new feature: every ship now gets asked if it fixes/reworks an earlier one,
used to flag the origin for a second look)" — same disclosure `setup.md` gives a brand-new
tracker at bootstrap, given once here since an existing tracker never goes through `setup.md`
again. Don't repeat it on later ships once `Next id:` exists.

If confirmed:
- Tag the new entry `fixes: I<N>` (bug fix) or `reworked: I<N>` (broader rework), referencing the
  origin's id (mint one for the origin now if it predates the id field — see the tracker-format
  section above).
- Set `reassess: pending` on the **origin** entry — **in whichever file it actually lives in.** The
  origin may already have been archived to `IMPROVEMENT_TRACKER_DONE.md` by the time a fix ships
  (Step 6's own Done-trimming can move it there long before anyone fixes it); check there if it's
  not still in the live tracker's Done section, same "one combined pool, not just the live file"
  treatment `feedback.md`'s outcome-writes already use. This is standalone of `Feedback:` — it
  applies whether or not the feedback subsystem is on. See `feedback.md` (Feedback on: folded into
  its check-in, prioritised over routine outcome asks) and `session-start.md` (Feedback off: a
  lightweight one-off surfacing, no persistent answer required).
- If `Risk register: on`, this link is also one of `risk-register.md`'s creation/update triggers —
  follow it there (propose creating or extending a risk area, confirm before writing).
- **If `Risk register: on`, also check whether the origin's id is itself a `mitigated-by:` entry
  on any risk area** — i.e., the thing that was supposed to *fix* a risk just needed fixing itself.
  This is stronger, more specific evidence than an ordinary same-category `fixes:` link (trigger 1)
  — see `risk-register.md`'s "A mitigation needing its own fix" note for how it's surfaced and
  what it does to that mitigation's `outcome:`.

If the user says this ship is *not* a fix/rework of anything, or the auto-detect had nothing
plausible, record the ship normally with no `fixes:`/`reworked:` tag — don't force a link that
doesn't exist.

**Recording any ship, first drop its id from every active risk entry's `at-risk:` list** — that
field is specifically *outstanding* ideas (see `risk-register.md`), and this one just stopped being
outstanding regardless of how it shipped. Then, separately: if this ship needed no `fixes:`/
`reworked:` tag of its own, that clean ship is itself counter-evidence against the risk (see
`risk-register.md`'s archival trigger) — note it there rather than just silently removing the id
and moving on.

**Also check whether this ship's id is tagged `mitigated-by: ... (outcome: planned)` on any active
risk entry** — a candidate proposed at Step 2 specifically as a risk's planned fix. If so, flip
`planned → pending` there (see `risk-register.md`'s Recording a planned mitigation) — this is what
starts the real outcome-check timing, distinct from the routine `fixes:`/`reworked:` handling above,
which is about *unplanned* fixes discovered after the fact.

**After appending, check whether Done needs trimming.** If the live tracker's Done section now
holds more than ~20 entries, archive the oldest down to a working set of ~15 (a target, same
spirit as Step 2's buffer — trim generously so this doesn't refire every single run): move them,
unedited and in their existing order, to the end of `IMPROVEMENT_TRACKER_DONE.md` (create it,
same directory as `IMPROVEMENT_TRACKER.md`, with a one-line `# <Project> — archived Done history`
header if it doesn't exist yet). Update the archive-pointer note under the live `## Done` header
to the cutoff date of the oldest entry now remaining live. This is mechanical bookkeeping, not a
judgement call about ideas or priorities, so it doesn't need user confirmation the way Steps 2/4/
4.5 do.

**Trimming doesn't wait on `outcome`** (`Feedback: on` — see `feedback.md`). Archive the oldest
entries on the normal ~20→~15 schedule regardless of whether their outcome is still `pending` —
otherwise a feedback loop that can't keep pace with shipping would let the live Done section grow
without bound. `feedback.md`'s eligible-count and drip/bulk logic treat the live tracker and
`IMPROVEMENT_TRACKER_DONE.md` as one combined pool of pending entries, oldest-first, so an entry
crossing into the archive while still `pending` doesn't drop it from consideration — it's still
askable, just from the other file.

`category-rotation` (`strategies.md`) counts only the live tracker's Done entries, never the
archive — its default window (5) is well inside the ~15-20 kept live, so this practically never
runs short, but if a project sets a much larger window than the live Done section holds, treat it
the same as "fewer than N total" (insufficient history, skip the bias) rather than reading the
archive file to fill the count.

**Reading the archive.** Only open `IMPROVEMENT_TRACKER_DONE.md` when something actually needs
older history — Step 2's Rejected-style history check extended to "has something like this
already shipped," the user explicitly asking about past work, or (`Feedback: on`) `feedback.md`'s
Step 0.5 check-in scanning for `pending` entries that got archived before being answered. Otherwise
don't read it as part of the normal Step 0-6 loop; that's most of the point of moving entries out
of the live tracker.

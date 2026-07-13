---
name: next-improvement
description: Runs a "what should we work on next" process for whatever project the user is currently in -- maintains a per-project IMPROVEMENT_TRACKER.md (idea categories + a tiered priority list), tops up any category that's run low by brainstorming fresh ideas grounded in that project's actual current state, ranks candidates against the project's own configured tiers, and proposes the next thing to build for the user to confirm before any code changes happen. Bootstraps the tracker itself on first use if the project doesn't have one yet. Use this whenever the user asks "what should we do next" / wants to pick the next feature or refactor / asks to poll for more ideas / mentions an improvement tracker or backlog, or when a work session is starting on a project with no specific task queued up yet.
---

# Next improvement

A repeatable "what next" loop: keep a running list of ideas per project, top the list up when
it runs thin, pick the next thing to build by weighing it against that project's own standing
priorities, confirm with the user, plan it in detail, build it, then record what shipped. This
skill is project-
agnostic -- all project-specific detail (what categories of idea to track, what the priority
tiers are, what's already been decided) lives in a file inside the project itself, not in this
skill. That file is what makes this skill reusable across every project rather than rewritten
per repo.

This file covers the steady-state loop only. Three companion files live alongside it and are
only worth reading when actually in play -- **don't read them unless the trigger condition
below says to**, they exist to keep this file lean for the common case:

- `setup.md` -- the one-time-per-project bootstrap interrogation. Read it when Step 0 finds no
  `IMPROVEMENT_TRACKER.md` yet.
- `strategies.md` -- alternate ways of presenting candidates in Step 4, beyond the default
  single top pick. Read it when `Selection strategy:` is set to anything other than `top-tier`,
  or when setting/changing it.
- `feedback.md` -- an optional loop that asks how past ships actually landed and feeds that back
  into future judgment. Read it when `Feedback: on`, or when setting/changing it.

## The tracker file

Each project that uses this skill has its own `IMPROVEMENT_TRACKER.md` at that project's root
(i.e. the directory containing its own code, not necessarily the overall repo root -- if you're
working in `some-repo/some-project/`, the tracker lives at `some-repo/some-project/IMPROVEMENT_TRACKER.md`,
not at the top of the whole repo, since a repo can hold several independent projects each with
their own priorities). This is the single source of truth: don't keep a separate mental list of
ideas or priorities, and don't split this across multiple files -- one tracker per project.

Format:

```markdown
# Improvement Tracker

## Goals (priority order, highest first)
Last reviewed: <YYYY-MM-DD>
Selection strategy: top-tier   <!-- optional, see strategies.md -->
Feedback: on                   <!-- optional, see feedback.md -->
1. <highest-priority tier>
2. <tier A> / <tier B> -- tied; if a candidate must pick one, prefer: <tie-break rule>
3. <next tier>
...

## <Idea category A>
(dry runs: <N> -- last: <YYYY-MM-DD>)  <!-- optional, only present after a dry top-up -->
- **Idea name** -- short rationale, referencing specific files/functions where useful.

## <Idea category B>
- ...

## Done
- **Idea name** (Category) -- one-line note on what actually shipped (may differ from the
  original idea's exact wording if the implementation took a different shape).

## Rejected
- **Idea name** (Category, YYYY-MM-DD) -- one-line reason it was declined.
```

- **Goals** is an ordered list, highest priority first, with a `Last reviewed:` date. Earlier
  tiers dominate later ones when candidates trade off against each other; lower tiers only break
  ties among roughly-equal candidates. Edit this section directly to reprioritize, and bump
  `Last reviewed:` when you do -- nothing else in this process needs to change when priorities
  shift. See Step 0.5 for how staleness gets surfaced automatically.
- Two or more goals may share the same tier number when they're genuinely equal priority right
  now. A tied group must carry a short tie-break note on the same line: what to do when a real
  candidate serves one tied goal but not its sibling. If the user has no strong opinion, fall
  back to something concrete like "prefer whichever is cheaper/faster to build" or "ask me when
  it happens" -- but prefer capturing their actual reasoning if they have one. Keep tie groups
  small (2, rarely 3); a tier that keeps growing tied entries is a smell that ranking has stopped
  meaning anything, and is worth flagging (see Step 0.5).
- `Selection strategy:` and `Feedback:` are optional lines, absent by default. Their full format
  and behavior live in `strategies.md` and `feedback.md` respectively -- don't inline their
  details here, and don't read those files unless one of them is actually present/being set up.
- Idea category headers and names are entirely up to the project -- there might be two, or
  five, and they might be called "Features"/"Refactors" or something far more specific to that
  project's domain. Discover them by reading the file; don't assume fixed category names.
- A category may carry an optional `(dry runs: N -- last: DATE)` note right under its header --
  see Step 2 for when it's added, incremented, cleared, and surfaced to the user.
- **Done** is append-only history, never deleted from. Prefix each entry with its origin
  category in parens -- useful bookkeeping regardless of any optional subsystem; legacy entries
  without a tag just aren't counted by anything that relies on it, no migration needed.
- **Rejected** is append-only, same as Done -- an idea proposed in Step 2 and declined by the
  user goes here with the reason, not just dropped. See Step 2 for how this gets checked before
  re-proposing something similar; the reason is what matters, not the mere fact of rejection.

## Step 0: Find or bootstrap the tracker

Look for `IMPROVEMENT_TRACKER.md` at the root of whichever project the user is currently working
in (use judgment on project boundary: the nearest enclosing directory with its own README,
package manifest, or similar -- not necessarily the git repo root, since one repo can contain
several projects with different concerns).

If it doesn't exist yet, read `setup.md` and follow it before doing anything else -- that's a
one-time-per-project bootstrap, kept out of this file since most invocations don't need it.

If it does exist, read it as-is and continue -- don't re-ask full setup questions on later runs.
Goals aren't fixed forever though: see Step 0.5.

## Step 0.5: Check whether goals are stale

Goals can drift as the project evolves, even without a formal re-setup. Check the `Last
reviewed:` date under Goals:

- **Missing** (tracker predates this field): treat as stale, ask now.
- **Older than ~30 days, or the Done list has grown noticeably since the last review**: prompt
  the user with a short check-in -- e.g. "Goals were last confirmed on <date> and N items have
  shipped since. Still the right order, or has anything changed?" Offer to keep as-is, reorder,
  add/remove a tier, or fold in a new priority entirely.
- **Recently reviewed and nothing suggests drift**: skip the prompt, proceed straight to Step 1.

If the user changes anything, update the Goals section and bump `Last reviewed:` to today. If
they confirm as-is, still bump the date so the next run doesn't re-ask right away. This check is
a single short question, not a repeat of the full `setup.md` interrogation -- don't re-litigate
every tier from scratch unless the user wants to.

The user can also trigger this at any time outside of a normal run -- e.g. "reprioritize" or
"goals have changed" -- by jumping straight to this step, editing Goals, and bumping the date.
This is also where an existing tie can be broken into a strict order, or a new tie formed between
previously-distinct tiers -- same edit-and-bump mechanism as any other reprioritization.

If `Selection strategy:` is present (or the user wants to add/change it), see `strategies.md` --
it's not fixed at setup either and is edited the same lightweight way. If `Feedback:` is present
(or the user wants to add/change it), see `feedback.md`, which also runs its own short check-in
from this step when relevant.

## Step 1: Count what's outstanding

Count remaining (not-in-Done) items in each idea category.

## Step 2: Top up any category running low

If a category has fewer than ~3 items, or is empty, it needs fresh ideas before ranking makes
sense -- there's nothing meaningful to weigh against the goals otherwise. Ground new ideas in
the project's actual current state rather than inventing from nowhere:

- What's been built or changed recently (recent commits, new modules, new files)?
- What's untested, fragile, or has a noted rough edge (TODO-style comments, test coverage gaps,
  anything flagged as a known issue in project docs or memory)?
- What's the natural next step after whatever just shipped?
- What did the user mention in passing that sounded like a want but wasn't captured yet?
- If `Feedback:` is on, factor recorded outcomes in too -- see `feedback.md`.

**Check Rejected before proposing.** If a candidate closely resembles something already in
Rejected, don't just skip it or blindly re-propose it -- read the recorded reason and judge
whether it still applies. A timing/priority reason ("not now, focused on X") can go stale and
stop applying; a substance reason ("doesn't fit this project," "already tried, didn't work")
usually doesn't. When genuinely unsure, it's fine to re-propose with a note ("this was declined
before for X -- has that changed?") rather than silently suppressing or silently repeating it.

**Show the proposed new ideas and wait for confirmation before appending anything.** This is the
first of the skill's three hard rules (the others being Step 4's pick-confirmation gate and
Step 4.5's plan-approval gate): brainstorming is a recommendation, not a decision -- the user
may accept all of it, drop some, tweak wording, or say none of it's worth keeping. Don't write to
the tracker until they've had a chance to react. Whatever gets declined, add it to **Rejected**
with the reason given (or your best summary of it if the user was terse) -- don't just drop it
silently, that's what lets the check above work next time. Match that file's existing format and
voice for whatever does get appended. Don't pad a thin category with filler just to hit a count --
if there are only one or two solid ideas, say so and move on rather than inventing weak ones. If
`Selection strategy:` includes `wildcard(tagged)`, see `strategies.md` for the idea-tagging
convention that mode depends on.

**Exhausted is a valid outcome, not a failure to fix.** If brainstorming (grounded in the checks
above) turns up nothing genuinely new or worth building, say so explicitly rather than quietly
lowering the bar until something fills the slot. When declaring a category exhausted, tell the
user *why*, concretely -- e.g. "checked recent commits, open rough edges, and what shipped last
-- everything that fits '<category>' either already shipped or the remaining candidates are
marginal/duplicate/out of scope." A vague "nothing comes to mind" isn't enough; the reasoning is
what lets the user judge whether the category's actually done or the search just wasn't broad
enough.

**Track dry top-ups so they don't repeat silently.** When a top-up attempt ends up adding nothing
-- brainstorming found nothing genuinely new, everything proposed was flagged weak, or the user
declined what was proposed -- note it inline under that category's header:
`(dry runs: N -- last: YYYY-MM-DD)`. Increment on each dry attempt; reset to nothing (remove the
line) the next time a solid idea actually gets added. At `dry runs: 2+`, surface this to the user
up front the next time this category comes up -- e.g. "Features has been topped up 2 times with
nothing solid since <date> -- possible this category is genuinely done; want to retire/merge it,
narrow its scope, or keep polling?" -- rather than letting the same empty search repeat forever
unnoticed.

## Step 3: Rank candidates against the tiers

Take the union of outstanding items across every idea category (freshly topped-up or not) and
weigh them against the Goals list **in order** -- a candidate serving tier 1 beats one serving
only tier 3, even if the tier-3 one is cheaper or more appealing to build. Lower tiers only
break ties between candidates that are roughly equal on every tier above them. The last tier is
usually a filter rather than a tiebreaker: if nothing outstanding is genuinely compelling right
now, say that instead of picking something just to have an answer.

Think concretely about each candidate: what would actually happen if it were built, and which
tier does that outcome serve? Don't take a category label at face value -- a "refactor" that
doesn't make anything more readable or any future feature easier doesn't serve the maintenance
tier just because it's filed under that category.

**Tied tiers**: evaluate candidates against every goal in the tied group, not just one.
- If a candidate serves all goals in the tie equally (or none of them), there's no conflict --
  rank it normally against the other tiers.
- If candidates split -- one serves goal A of the tie, another serves goal B -- that's exactly
  the case the tie's stored tie-break rule exists for. If the rule is concrete (e.g. "cheaper
  wins"), apply it mechanically and rank the winner. If the rule says "ask me", or no rule was
  stored (a tracker predating this feature, or a same-number tier that was a typo), don't
  resolve it silently -- carry both candidates forward as co-contenders into Step 4.

This ranking is what Step 4 presents from. If `Selection strategy:` is set to something other
than plain `top-tier`, `strategies.md` changes *how* the ranking gets presented, never how it's
computed -- this step stays the same either way. If `Feedback:` is on, weigh recorded outcomes
qualitatively when judging candidates here too -- see `feedback.md`.

## Step 4: Propose, then wait

Default (no `Selection strategy:` set, or set to plain `top-tier`): present the top candidate,
or 2-3 close contenders if the ranking is genuinely close, with reasoning tied to specific tiers
-- not "this seems good" but "this serves tier 1 because X" or "this is tier-3 maintenance work
but nothing above it is ready to build, since Y."

If `Selection strategy:` is set to anything else, read `strategies.md` and build the
presentation as it describes instead.

If Step 3 carried forward an unresolved tied-goal conflict, present that as its own distinct
case regardless of strategy -- the user needs to know which situation they're looking at. E.g.:
"X and Y are tied-priority; candidate A serves X, candidate B serves Y, and no stored rule
resolves it automatically -- which matters more for this one?" Close contenders are about
candidates scoring similarly; a tied-goal conflict is about the tier ranking itself being unable
to pick a winner.

**Do not start planning or implementing until the user confirms which one (if any) to build.**
This is the second of this skill's three hard rules (the others being Step 2's append gate and
Step 4.5's plan-approval gate): the ranking is a recommendation, not a decision. The user may
pick something other than the top candidate, ask for a different combination, or say none of it
is worth doing right now -- all of those are fine outcomes.

## Step 4.5: Plan the confirmed pick

A confirmed idea is still just an idea -- don't jump straight to code. Produce a detailed
implementation plan first: what files/functions get touched, the approach, and how it'll be
verified. **This is the third hard rule: get the plan approved before writing any code.**

If Claude Code's plan mode is available in this session, use it naturally for this (EnterPlanMode
/ ExitPlanMode) -- write the plan to the plan file and call ExitPlanMode to request approval. If
plan mode isn't available or doesn't fit the context, present the plan inline instead and wait
for an explicit go-ahead before proceeding.

Keep the plan proportional to the work -- a one-line fix doesn't need the same ceremony as a
multi-file feature. Use judgment on how much detail is actually useful rather than padding every
plan to a fixed template.

If the user asks for changes to the plan, revise and re-confirm before moving to Step 5 -- that's
iterating on the same plan within the same session, not a persistence question.

If the user declines the plan outright rather than asking for changes ("actually, let's not do
this after all"), that's not a Step 6 outcome and not a Rejected outcome either -- a plan getting
declined doesn't retroactively unpick or reject the idea itself, which is still perfectly valid,
just not being built right now. Leave it as-is in its category; it goes back through Step 3's
ranking next time like anything else outstanding.

**Always plan fresh; don't reuse an old plan for an idea that gets picked again later.** If a
candidate was proposed, planned, and then declined or shelved in an earlier session, and the same
idea comes up again now, write a new plan grounded in the project's current state rather than
resurrecting the old one -- the codebase may have changed since (other ideas shipped, files
moved, dependencies shifted), and a stale plan silently reused is the same risk this skill
already guards against elsewhere (dry-run tracking, goal staleness, feedback outcomes: don't
trust a cached judgment, re-ground it). Plan-mode plan files aren't tracked by or referenced from
the tracker for this reason.

## Step 5: Build it

Once the plan is approved, implement it as planned -- this skill only changes how the work item
was chosen and planned, not how you write code, run tests, or verify changes. Follow whatever
conventions the project's own docs/CLAUDE.md/memory already establish. If reality diverges from
the plan enough to matter, say so rather than silently deviating.

## Step 6: Record what shipped

Move the item from its origin category to **Done** in that project's tracker, with a one-line
note on what was actually built. If `Feedback: on`, see `feedback.md` for the extra tagging to
add at this step. Leave everything else in the file untouched. If the work surfaced new
follow-on ideas that weren't there before, add them to the relevant category now rather than
losing them -- that's the loop closing, not scope creep.

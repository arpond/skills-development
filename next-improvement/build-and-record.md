# Build and record: Steps 4.5 through 6

Read this file once the user confirms a pick in `SKILL.md` Step 4, or when finished work needs
recording without one. Many runs end at Step 4 with nothing confirmed, so these steps stay out
of the core read.

## Step 4.5: Plan the confirmed pick

A confirmed idea is still just an idea — don't jump straight to code. Produce a detailed
implementation plan first: what files/functions get touched, the approach, and how it'll be
verified. **This is one of the skill's hard rules (see the table in `SKILL.md`): get the plan approved
before writing any code.**

**Two handoff points, one test.** Other skills in the session can help here, and what a skill
does with the plan decides where it fits. One that questions the user until the open decisions
are settled belongs *before* the draft — `grill-me` is the reference case. One that examines a
drafted plan and argues against it belongs *after* — `plan-red-team` is the reference case. A
skill that does neither is not offered at this step at all. Both offers work the same way:

- Each is one line, folded into a message already being sent: the acknowledgement of the
  confirmed pick before the draft, the plan itself after it. Neither is a stop of its own.
- Each is asked per pick. Nothing is configured, and no answer is remembered.
- More than one qualifying skill is a numbered choice, per `SKILL.md` Step 4's rule, each named with the one
  thing it does differently. Being the reference case doesn't make a skill the winner.
- Declining stays available beside the numbered skills, and only one runs per handoff point.
- An offer says what a skill costs, where the skill states a cost of its own. A panel of
  subagents isn't a free yes, and the offer is where that gets decided.
- No qualifying skill means silence. An absent skill isn't a finding to report.

**Before the draft**, hand off to the chosen skill's own flow, then plan from what the interview
settled. Don't re-ask in the plan what the interview already answered. The interview goes before
the draft for a reason: a plan drafted first anchors it to Claude's guesses about scope. The
user's answers then arrive as corrections to those guesses, rather than as the input the plan was
built from. This is most worth taking up on a feature-type pick, for the reason `SKILL.md` Step 4
already gives for surfacing one.

**After the draft**, the offer rides with the plan itself, ahead of the approval gate rather than
after it. A review comes back with findings, not with a verdict:

- judge each finding rather than applying it
- revise the plan where one lands
- say which ones you disagreed with, and why

Then the plan goes to the same approval gate as any other. A review is never approval, however
clean it comes back.

If Claude Code's plan mode is available in this session, use it naturally for this (EnterPlanMode
/ ExitPlanMode) — write the plan to the plan file and call ExitPlanMode to request approval. The
after-draft offer goes in that same message. If
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
just not being built right now. Leave it as-is in its category; it goes back through `SKILL.md`
Step 3's ranking next time like anything else outstanding.

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
losing them — that's the loop closing, not scope creep. Each one stays within `Entry word limit:`.
Evidence from the build goes in the commit message or the ticket, not in any entry.

**Ask whether this ship fixes or reworks an earlier one.** Every recording, ask directly, with an
auto-detect suggestion rather than a blind open question:
1. Scan recent Done entries (and the branch/commit context, if this session touched a specific
   bug or reopened specific files) for a plausible origin.
2. Propose it.
3. Let the user confirm, correct, or say no.

If `Next id:` was missing before this recording, this is the first time this project has ever been
asked — give the one-time heads-up in `tracker-maintenance.md` before asking.

If confirmed:
- Tag the new entry `fixes: I<N>` (bug fix) or `reworked: I<N>` (broader rework), referencing the
  origin's id (if the origin has no id, mint one for it now — see `tracker-maintenance.md`).
- Set `reassess: pending` on the **origin** entry — **in whichever file it actually lives in**, per
  `SKILL.md`'s "Reading the archive". The Done archive sweep can move an origin to the archive long
  before anyone fixes it. This is standalone of `Feedback:` — it
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
against that risk.** Nothing to record for it, since exposure was never stored; it's read out of
Done whenever archival is next considered. See `risk-register.md`'s archival trigger.

**After appending, run the Done archive sweep.** `session-start.md` Step 0.5 holds its rules,
and that file is already loaded. A sweep after a ship catches entries that crossed the age line
since the session began.

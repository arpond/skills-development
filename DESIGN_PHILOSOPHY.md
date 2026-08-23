# Design philosophy

Principles applied consistently across the skills in this repo, grouped by the concern they
address rather than a flat unstructured list.

**These govern this file and `CONVENTIONS.md` too, not only the skills.** The bullets read as
advice about skills because that's what they were written from, but nothing in them is
skill-specific: both shared files are text that gets read and acted on, so they're subject to the
same rules. The failure is asymmetric and worth naming, because it has happened repeatedly — the
principles get applied to a skill reflexively and to these two files hardly at all, since a
document about rules doesn't feel like a thing the rules apply to. Worked instances, all real:

- `CONVENTIONS.md` grew per-skill conformance tables — a stored verdict recomputable by a grep, and
  one that misleads the moment it goes stale. Both
  [Don't persist a signal just because it's useful once](#dont-persist-a-signal-just-because-its-useful-once)
  and [Re-ground, don't cache](#re-ground-dont-cache) already forbade it.
- `CLAUDE.md`'s review loop carried a trailing line restating its own opening, which promptly went
  stale when the opening changed — the repetition it warns about, in the file doing the warning.
- A spec here was once widened to match what its implementations happened to do, rather than the
  implementations being brought up to it.

When editing either shared file, run the same passes over it that a skill change would get. A
principle that only ever gets applied outward isn't being applied.

## Contents

- [Write gates & confirmation](#write-gates--confirmation)
  - [Propose, don't just do](#propose-dont-just-do)
  - [A default the user never saw isn't a default](#a-default-the-user-never-saw-isnt-a-default)
  - [One gate, not two](#one-gate-not-two)
  - [Numbered choices, not just labels](#numbered-choices-not-just-labels)
- [Trust & staleness](#trust--staleness)
  - [Re-ground, don't cache](#re-ground-dont-cache)
  - [Reasons over blacklists](#reasons-over-blacklists)
  - [Inputs are claims, not truth](#inputs-are-claims-not-truth)
  - [A claimed property that isn't self-verifying](#a-claimed-property-that-isnt-self-verifying)
  - [Unreachable isn't resolved, in either direction](#unreachable-isnt-resolved-in-either-direction)
  - [Malformed stored state gets its own check](#malformed-stored-state-gets-its-own-check)
  - [Don't persist a signal just because it's useful once](#dont-persist-a-signal-just-because-its-useful-once)
- [Principles vs. specs](#principles-vs-specs)
- [Structure & reuse](#structure--reuse)
  - [Index what fails silently](#index-what-fails-silently)
  - [A rule is a sentence, an instruction block is a list](#a-rule-is-a-sentence-an-instruction-block-is-a-list)
  - [A review criterion needs a floor](#a-review-criterion-needs-a-floor)
  - [Reuse a judgment test, don't invent a parallel one](#reuse-a-judgment-test-dont-invent-a-parallel-one)
  - [A computed join needs its matching test written down once](#a-computed-join-needs-its-matching-test-written-down-once)
  - [Self-correcting knobs share one shape — reuse it](#self-correcting-knobs-share-one-shape--reuse-it)
  - [Structure around the domain's natural shape](#structure-around-the-domains-natural-shape)
  - [Split along orthogonal triggers, not around size](#split-along-orthogonal-triggers-not-around-size)
  - [Concrete over vague](#concrete-over-vague)
  - [Ask when genuinely ambiguous, don't silently resolve](#ask-when-genuinely-ambiguous-dont-silently-resolve)
- [Docs, portability & configuration](#docs-portability--configuration)
  - [Progressive disclosure](#progressive-disclosure)
  - [Moving content means re-pointing every reference to it](#moving-content-means-re-pointing-every-reference-to-it)
  - [Documentation travels with the skill](#documentation-travels-with-the-skill)
  - [A skill's own instructions can't depend on the dev repo around it](#a-skills-own-instructions-cant-depend-on-the-dev-repo-around-it)
  - [No machine-specific paths in a tracked skill file](#no-machine-specific-paths-in-a-tracked-skill-file)
  - [Mechanism and personal preference belong in different files](#mechanism-and-personal-preference-belong-in-different-files)
  - [Independent knobs, not piggybacked defaults](#independent-knobs-not-piggybacked-defaults)
  - [Every write path needs an explicit target](#every-write-path-needs-an-explicit-target)
  - [An artifact's location is resolved, not assumed](#an-artifacts-location-is-resolved-not-assumed)
  - [State hard dependencies explicitly](#state-hard-dependencies-explicitly)

## Write gates & confirmation

When a skill acts on the user's behalf, showing the action before it happens is the safeguard —
these bullets cover when/how that gate fires.

### Propose, don't just do

Every consequential write — a new idea added to a tracker, a choice of what to build, an
implementation plan — gets shown to the user and confirmed before it happens. A recommendation is
not a decision. A gate that quietly stopped being enforced is invisible — nothing fails, the write
just happens — so where a skill has more than one, they get indexed rather than left implicit. Gates
are the clearest member of a wider class that needs indexing for that same reason; see
[Index what fails silently](#index-what-fails-silently) for the class and the test.

### A default the user never saw isn't a default

It's undisclosed forced behavior. Any skill with a built-in fallback (a threshold, a selection
strategy, a term list) must surface that fallback's concrete effect during setup/bootstrap and get
it confirmed, not just ask "want the defaults?" and move on — a special case of
[Propose, don't just do](#propose-dont-just-do), applied to defaults specifically.

### One gate, not two

When a skill needs several related confirmations before proceeding (e.g. scope and understanding),
fold them into a single gate rather than gating twice in a row. Back-to-back stops for adjacent
information don't add safety — they train the user to skim past confirmations instead of actually
reading them, which undermines [Propose, don't just do](#propose-dont-just-do) more than it
reinforces it.

### Numbered choices, not just labels

A user confirming a choice should be able to say the shortest possible thing back ("go with 2")
without re-typing a name or guessing which label you meant. Descriptive labels explain options;
they don't identify them. The exact format is a spec — see `CONVENTIONS.md`, "Numbered choices."

## Trust & staleness

Nothing a skill holds — a past judgement, an external input, a stored file, an unverified claim
— is trustworthy by default. Each of these fails differently, so each gets its own check:

### Re-ground, don't cache

Judgements (priorities, rejected ideas, plans) can go stale as a project changes. Rather than
trusting a cached decision indefinitely, skills re-check it against current state — but the check
itself should be cheap and only interrupt the user when there's real reason to think something's
drifted, not on every run.

### Reasons over blacklists

When something gets declined, record _why_, not just _that_ it was declined. A flat suppression
list risks permanently hiding something that was only rejected for timing, not substance — the
reason is what lets a future judgement call be made correctly.

### Inputs are claims, not truth

Applies the same discipline as [Re-ground, don't cache](#re-ground-dont-cache) to what comes in
from outside the skill on a single pass — a ticket description, a config file, a local checkout.
None of these are guaranteed accurate just because they were provided: verify them against a more
authoritative source (the actual code, the actual remote, the actual current state) before
building on them, and treat a mismatch as something to surface, not quietly reconcile.

### A claimed property that isn't self-verifying

Deserves a one-time check at the point it's created. "This should be committed for sharing to
actually work" is a sentence, not a guarantee. Where a skill's behavior depends on an external fact
holding (a file actually tracked, a dependency actually installed), check it once at the moment
that matters most — creation — rather than asserting it in prose and trusting it got acted on.

### Unreachable isn't resolved, in either direction

Sometimes a check can't be run at all — a linked ticket without read access, an unfetchable remote
link, a search with zero results, a missing git remote. That's a third state, distinct from
"confirmed true" and "confirmed false," and collapsing it into either — treating it as absent, or
treating it as an automatic blocker — is the mistake. Surface the specific thing that couldn't be
checked and let the user decide, rather than guessing which direction is safer.

### Malformed stored state gets its own check

Distinct from "can't reach it." A stored file that *can* be read but doesn't parse into the shape
a skill expects is a different failure mode from
[unreachable](#unreachable-isnt-resolved-in-either-direction): don't silently reinterpret it,
discard it, or bootstrap over it. Stop and ask.

### Don't persist a signal just because it's useful once

If a piece of information can be computed fresh, cheaply, at the moment it's needed, that beats
writing it down and now having to keep it in sync. Stored state (a tracker annotation, a cached
judgement) needs its own staleness-handling the moment it's written — an idea gets reworded,
merged, or shipped, and whatever referenced it by name is now wrong. This is about _not storing_
the judgement in the first place when recomputing it costs little, as distinct from re-checking a
judgement already stored (see [Re-ground, don't cache](#re-ground-dont-cache)).

## Principles vs. specs

Which of this repo's two shared files a rule belongs in — and the test for deciding, since the
answer isn't obvious and getting it wrong is why specs end up buried inside principles.

**Ask what failure the rule prevents.** If the failure is *two implementations doing it
differently* — drift between skills, where each one alone looks fine and only the disagreement is
wrong — it's a spec, and belongs in `CONVENTIONS.md`. If the failure is *one judgment made badly*
— this skill, this decision, no second implementation involved — it's a principle, and belongs
here.

A rule can be both, and usually the embedded spec is the part that got written down first because
it's easier to state. Split it rather than filing the whole thing under one: the principle keeps
the *why* and ends with a pointer, the spec takes the exact shape. "Self-correcting knobs share one
shape" was a principle ("don't write a bespoke counter per knob") wrapped around a spec (increment
here, reset there, force-reset once surfaced) — the spec had already drifted across three instances
while the principle read as perfectly sound.

Two things that look like specs and aren't. A **prohibition** ("no machine-specific paths in a
tracked file") has no shared implementation for anyone to drift from — it's a constraint, not a
shape to match. And a rule with only one implementation isn't a spec *yet*; it becomes one when a
second skill needs it, which is the point to move it rather than copy it.

## Structure & reuse

How a skill's checks and prompts get built — coverage should come from the shape of the problem
and from reusing what already exists, not from listing cases as they're remembered.

### Index what fails silently

A skill accumulates rules that must never be skipped, and a review can only check the ones it can
find. So collect them in one index — but the inclusion test is not "is this important," which
everything passes. **It's whether skipping the rule produces a visible failure.** If it does, the
output already reports it and an index adds nothing. If it doesn't, nothing anywhere will ever say
so, and the index is the only thing standing between a quietly-dropped rule and never finding out.

The clearest case is a confirm-before-write gate ([Propose, don't just do](#propose-dont-just-do)):
skip it and nothing errors, the write just happens. But that's the clearest case, not the only one
— a "never write secrets into this file" prohibition fails the same way and more expensively, and
so does anything that makes an absence look like a legitimate answer ("a dimension with nothing
wrong says so explicitly, rather than going quiet"). Conversely a rule like "every finding cites
its evidence" is *out*: drop it and the very next report is visibly full of uncited findings.

Keeping the test sharp is what keeps the index useful. An index that grows to cover every rule in
the skill is no longer checkable at a glance, which was the entire point — so a rule that doesn't
pass the test stays where it's stated and simply isn't indexed. The index's exact shape is a spec —
see `CONVENTIONS.md`, "The hard-rules table."

### A rule is a sentence, an instruction block is a list

A rule in the fourth clause of a sixty-word sentence reads as part of the explanation around it,
not as a rule. The reader here is a model scanning for what to do. A constraint it has to extract
from a subordinate clause is one it will sometimes not extract, and nothing flags when that
happens — the same silent failure [Index what fails silently](#index-what-fails-silently) exists
for, one level down. A rule that isn't its own sentence also can't be indexed, grepped, or quoted
in a review without trimming it, so the two go together: the table can only hold what the prose
already separates.

So: state each rule as its own sentence, of at most twenty-five words. The explanation around
it — the why, the worked failure, the contrast with what it isn't — stays as long as it needs to
be. Where a sentence or paragraph is several instructions rather than one rule with its
reasoning, make it a list, one instruction per item. A chain of imperatives joined by dashes is
the usual disguise. Six instructions in one paragraph is six chances to stop reading before the
last one; `CLAUDE.md`'s review-loop check 1 was the worked instance.

**The cap applies to the sentence a reader would copy into a hard-rules table, and that is the
test, not an illustration.** A sentence is rule-bearing if it belongs in such a table (it fails
silently when skipped), or if it is an imperative the reader executes as a step. Everything else
is explanation and has no cap. Within a rule-bearing sentence:
- Count to the full stop. "Rule — reason" and "rule; reason" are one sentence; if the rule clause
  alone fits the cap, a full stop at the dash is the whole fix.
- Parenthetical examples, `e.g.` lists, a dash-enclosed example run, and a bold label
  (`**Found nowhere**:`) don't count. Inline `code` spans do count; they're words the reader reads.
- An imperative inside a parenthetical is still an instruction. Move it out; the exemption is for
  examples, not for rules hidden in them.
- A list item that is one instruction plus its reasoning is fine at any length. Split an item only
  when it carries three or more instructions; two, each its own short sentence, are fine.

**Which sentence is the rule: the one a reader needs in order to act.** A short bold lead
followed by a sixty-word sentence carrying the actual mechanics has its rule in the long one, and
that is the sentence to split. The usual end-loaded shape is "If ‹forty-word condition›, ‹rule›
rather than ‹contrast›": condition as its own sentence, then the rule, then the contrast.

Out of scope: a skill's frontmatter `description` (trigger text, one sentence by construction),
README prose and example dialogue (a human reads the prose, and dialogue quotes how Claude
speaks), and a vendored skill's upstream text. README procedures — install steps, a refresh
command — are in scope.

The twenty-five-word cap and the one-instruction-per-item shape are borrowed from ASD-STE100
(rules 6.3 and 5.2). The rest of that standard deliberately isn't: it strips voice, and the
reasoning in this file is the voice. `python ste-writing/scripts/ste-lint.py --cap 25 --show
<file>` lists each sentence over the cap and each paragraph over six sentences, with the line its
paragraph starts on; `--show` skips parentheticals and bold labels when counting, matching the
rule above. It can't tell a rule from its explanation, so its hits are where to look, not a
verdict. There is no sentence-count cap on a paragraph; `long_paragraph` is a locator only.

### A review criterion needs a floor

An unbounded rule ("every X must be Y") yields findings in proportion to corpus size, not
defects, so fixing one round exposes the next. "A rule is a sentence" shipped without its
scope paragraph: two blind rounds found 119 then ~160 sites, every reviewer raised the same
four ambiguities, and the findings that mattered were about thirty, all from round one.
Writing the scope down dropped round three to 74.

So: a new rule ships with its scope — what it covers, what's exempt, what counts. Read a
round's ambiguities before its findings; anything two reviewers raised independently is a
defect in the rule, fixed there first. A round that finds as much as the last is measuring
the corpus, not the work: stop and bound the rule.

### Reuse a judgment test, don't invent a parallel one

When a skill needs to classify or filter something in a new context — deciding whether existing
documentation belongs somewhere else, say, rather than a fresh capture candidate — check first
whether an existing test elsewhere in the skill already answers the same underlying question, just
pointed at different input, before drafting a new one. A second, slightly-different test for what
is structurally the same judgment call is harder to keep consistent than one test applied twice,
and the two versions will eventually drift from each other as one gets refined and the other
doesn't.

### A computed join needs its matching test written down once

Replacing a stored link (an id on a list) with a computed match ("does this candidate touch this
risk's areas?") is usually the right trade — it deletes the add/remove/repopulate paths and with
them every way the list could go stale, per
[Don't persist a signal just because it's useful once](#dont-persist-a-signal-just-because-its-useful-once).
But it doesn't delete the work, it relocates it into a judgement that now runs at every call site.
State that judgement once, name it, and have each site refer to it — otherwise the design has
swapped a visible failure (one stale list) for an invisible one (nine sites quietly disagreeing
about what "touches" means), which is
[reuse a judgment test](#reuse-a-judgment-test-dont-invent-a-parallel-one) failing in a new guise.
The test has to say what gets compared when the two sides aren't alike — an idea that hasn't been
built has no files yet, so it matches on what its rationale names, not on a diff.

Two non-answers belong in the test, not rounded away: *too vague to place*, and *the key no longer
resolves*. That second one is the sharp edge — when a join key names something external (a path, a
module, a ticket), it needs the same treatment any other external claim gets under
[A claimed property that isn't self-verifying](#a-claimed-property-that-isnt-self-verifying), and
for a worse reason than usual: a stored id that dangles breaks loudly, while a stored path that
stopped existing just silently matches nothing forever, leaving the entry looking healthy while it
protects nothing. Check it resolves at the point the entry is already in hand — not as a sweep.

### Self-correcting knobs share one shape — reuse it

When a skill stores a numeric default and can also detect that the default is miscalibrated (a
counter that keeps hitting the same fallback path instead of the intended one), don't write a
bespoke streak/counter per knob — that's the same "second, slightly-different test" mistake
[above](#reuse-a-judgment-test-dont-invent-a-parallel-one), applied to a mechanism instead of a
judgment call, and just as prone to drifting: each bespoke copy tends to answer small design
questions ("does surfacing it reset the counter, or only a genuine correction?") slightly
differently, with no single place that's actually right. State the shape once; each instance then
declares only its own trigger, corrected signal, and threshold. That shape is a spec — see
`CONVENTIONS.md`, "Self-correcting counters."

### Structure around the domain's natural shape

Not around whatever named rules got thought of first. A checklist keyed to a fixed list of named
items (rule A, rule B, rule C) always has a gap for whatever wasn't named yet — a new rule either
doesn't fit any of them or gets stuffed into one that's a poor match. Structure the check around
the domain's actual shape instead (the parts a thing is made of, the stages a process goes
through), with one genuinely-enforced miscellaneous bucket for whatever still doesn't fit. A
miscellaneous bucket only satisfies this if it gets the same enforced check as every other part;
otherwise it's just where rules go to be silently skipped.

### Split along orthogonal triggers, not around size

Before building a new skill, check whether it's actually one capability or several — different
trigger conditions, different audiences, different write targets are the signal, not word count.
If orthogonal, build separate skills and cross-reference each explicitly in its own description
(which one handles what, where the handoff is) — as `jira-ticket-audit`/`plan-technical-jira-ticket`
already do — rather than one skill with internal branching for unrelated use cases. The same
question applies retrospectively, not just at birth: a skill that grew one feature at a time can
drift into covering 2+ orthogonal triggers without anyone deciding that on purpose — the repo's
review loop (see `CLAUDE.md`, check 3) treats "does this skill now cover more than one orthogonal
capability" as one of the things a Gaps pass looks for, not something judged once and forgotten.
The reverse mistake is splitting prematurely: steps that always fire together and share all state
aren't separate capabilities, they're one skill's internal structure — that's what
[progressive disclosure](#progressive-disclosure) (a companion file) is for, not a second skill.

### Concrete over vague

Prompts push for specific, defensible reasoning ("checked X, Y, Z, here's why") rather than
accepting a shrug as an answer — both from the model's own outputs and in what it asks the user to
confirm.

### Ask when genuinely ambiguous, don't silently resolve

Ties, close calls, and conflicting signals get surfaced explicitly rather than picked arbitrarily
and presented as if there was only ever one obvious answer.

## Docs, portability & configuration

Where things live and how they're written: what belongs in-context vs. one-time, what travels with
the skill folder vs. stays machine-specific, and who owns which layer of a config write.

### Progressive disclosure

The always-loaded core file stays lean; anything one-time (a bootstrap/setup step) or opt-in (a
feature most projects won't touch) lives in a companion file read only when its trigger condition
is actually met. A file's size is a signal — if a section only matters rarely, it usually belongs
somewhere that's only read rarely too. The diagnostic here is temporal (does this run every time,
or only once/rarely), not proportional to how much configuration or setup logic a skill happens to
have — a skill with nothing to negotiate at bootstrap can still accumulate real one-time content
over time, and each addition needs the every-run-vs-once question re-asked on its own merits.

### Moving content means re-pointing every reference to it

Not just the file it moved from/to. [Progressive disclosure](#progressive-disclosure) says _where_
something should live; it doesn't guarantee every other file gets updated when it moves. A
companion file can cross-reference another step/section by name without either file being touched
in the edit that relocates it — that reference goes stale silently. Grep the whole skill for the
old location whenever content is split out or merged, and treat the move as incomplete until every
cross-reference repo-wide points at the new home.

### Documentation travels with the skill

Installing a skill means copying its folder, so anything a person needs to evaluate or use it
belongs inside that folder as its own `README.md`, not in a repo-level file that doesn't get copied
along. Different concern from [Progressive disclosure](#progressive-disclosure) (which is about
what Claude loads into context) — this is about what a human still has once the skill is installed
elsewhere. The top-level README stays a thin index pointing into each skill's own docs, rather than
duplicating them.

The bar is a person deciding whether to install this, who can't see the code and won't read
`SKILL.md`. That includes the question skills most often leave unanswered: **what will this write
into my project, and where?** Someone is entitled to know that before a skill edits their repo,
not after. Which sections a README must carry to clear that bar is a spec — see `CONVENTIONS.md`,
"Skill README contents."

### A skill's own instructions can't depend on the dev repo around it

A third case, distinct from both neighbours here: not what a human needs
([Documentation travels with the skill](#documentation-travels-with-the-skill)) and not what Claude
loads into context ([Progressive disclosure](#progressive-disclosure)) — this is about a skill's
own *operative* content (text Claude actually reads and acts on) citing something that only
happens to exist in this dev repo. Pointing `SKILL.md` or a companion file at this
`DESIGN_PHILOSOPHY.md`, or any other repo-root file, for justification reads fine here, where the
file sits alongside the skill, but breaks the moment the skill deploys standalone, since only its
own folder gets copied. State the underlying reasoning inline instead of citing shared context
that may not travel with it.

### No machine-specific paths in a tracked skill file

An absolute path to a specific user account or machine (`C:\Users\someone\...`) breaks the moment
the skill is installed anywhere else, and often fails silently — the skill just can't find its
dependency and either stalls or improvises. Any path a skill depends on should be expressed
relative to a portable anchor (the current user's home directory, a location the skill bootstraps
itself) rather than copied from wherever it was first written.

### Mechanism and personal preference belong in different files

A skill's own logic (the checklist, the loop, the ranking method) should be portable across users;
whatever encodes one person's actual rules, priorities, or ruleset belongs in a separate file the
skill reads, not hardcoded into the skill itself. This is the same split `IMPROVEMENT_TRACKER.md`
already makes per-project — apply it per-user too whenever a skill's judgment calls are really one
person's preferences rather than something universal.

### Independent knobs, not piggybacked defaults

When a skill has multiple configurable quantities that interact — how many items a sub-mode
generates vs. an overall cap on the total, say — keep each one separately named and settable
rather than hardcoding one to silently ride on another's number or on an unstated constant. A user
changing one shouldn't have to reason about which other knobs secretly moved with it.

### Every write path needs an explicit target

Not just every read path a precedence order. Layered config (project-level over personal over
built-in default) is easy to get right on the read side and easy to forget on the write side: when
a correction needs writing back, which layer does it belong to? Solve both directions, not just
the one that's exercised on every run.

### An artifact's location is resolved, not assumed

A skill that maintains a file inside the user's project shouldn't hardcode one path for it. A file
sitting somewhere else is then invisible, and the skill bootstraps a second copy on top of work
that already existed — the worst outcome available, and a silent one. Resolve over a short ordered
list of candidate locations instead, and treat the two awkward results as first-class: finding it
in *two* places is ambiguity to surface, not a race the first hit wins
([Ask when genuinely ambiguous](#ask-when-genuinely-ambiguous-dont-silently-resolve)), and finding
it nowhere means bootstrapping — which should follow the layout the project already has rather than
imposing one. Creating a directory structure to hold your own artifact is a layout decision that
isn't yours to make.

Related but distinct from [Every write path needs an explicit target](#every-write-path-needs-an-explicit-target):
that one is about *which layer* a write belongs to once you know the file; this is about finding
the file at all. Both fail the same way — quietly, on the write side, long after the read side
looked fine.

Where more than one skill writes into the same project, the resolution order has to be identical
across them, or the same project ends up with artifacts scattered by whichever skill created each
one. That shared order is a **concrete spec, not a principle** — it belongs in this repo's
`CONVENTIONS.md`, with each skill restating it inline, since
[a skill can't cite a repo-root file](#a-skills-own-instructions-cant-depend-on-the-dev-repo-around-it)
and only its own folder travels.

### State hard dependencies explicitly

Distinguish them from what degrades gracefully. If a skill can't function at all without something
external (an MCP server, a specific tool), that belongs up front in its own docs — not just
handled gracefully at runtime once someone's already hit it. Dependencies the skill already works
around on its own (per
[Unreachable isn't resolved](#unreachable-isnt-resolved-in-either-direction)) don't need the same
billing; conflating the two either buries a real blocker behind a wall of caveats or overstates
how fragile the skill actually is.

Applies between a skill's own optional subsystems too, not just external tools — if optional
feature B reuses optional feature A's periodic mechanism (a check-in loop, a scheduled surfacing),
turning B on without A doesn't just degrade gracefully, it can leave B permanently inert with no
visible sign. State that dependency explicitly and surface it at the point B would first activate,
the same as an external dependency would be stated up front.

# Design philosophy

Principles applied consistently across the skills in this repo, grouped by the concern they
address rather than a flat unstructured list.

## Contents

- [Write gates & confirmation](#write-gates--confirmation)
  - [Propose, don't just do](#propose-dont-just-do)
  - [A default the user never saw isn't a default](#a-default-the-user-never-saw-isnt-a-default)
  - [One check-in, not two](#one-check-in-not-two)
  - [Numbered choices, not just labels](#numbered-choices-not-just-labels)
- [Trust & staleness](#trust--staleness)
  - [Re-ground, don't cache](#re-ground-dont-cache)
  - [Reasons over blacklists](#reasons-over-blacklists)
  - [Inputs are claims, not truth](#inputs-are-claims-not-truth)
  - [A claimed property that isn't self-verifying](#a-claimed-property-that-isnt-self-verifying)
  - [Unreachable isn't resolved, in either direction](#unreachable-isnt-resolved-in-either-direction)
  - [Malformed stored state gets its own check](#malformed-stored-state-gets-its-own-check)
  - [Don't persist a signal just because it's useful once](#dont-persist-a-signal-just-because-its-useful-once)
- [Structure & reuse](#structure--reuse)
  - [Reuse a judgment test, don't invent a parallel one](#reuse-a-judgment-test-dont-invent-a-parallel-one)
  - [Structure around the domain's natural shape](#structure-around-the-domains-natural-shape)
  - [Split along orthogonal triggers, not around size](#split-along-orthogonal-triggers-not-around-size)
  - [Concrete over vague](#concrete-over-vague)
  - [Ask when genuinely ambiguous, don't silently resolve](#ask-when-genuinely-ambiguous-dont-silently-resolve)
- [Docs, portability & configuration](#docs-portability--configuration)
  - [Progressive disclosure](#progressive-disclosure)
  - [Moving content means re-pointing every reference to it](#moving-content-means-re-pointing-every-reference-to-it)
  - [Documentation travels with the skill](#documentation-travels-with-the-skill)
  - [No machine-specific paths in a tracked skill file](#no-machine-specific-paths-in-a-tracked-skill-file)
  - [Mechanism and personal preference belong in different files](#mechanism-and-personal-preference-belong-in-different-files)
  - [Independent knobs, not piggybacked defaults](#independent-knobs-not-piggybacked-defaults)
  - [Every write path needs an explicit target](#every-write-path-needs-an-explicit-target)
  - [State hard dependencies explicitly](#state-hard-dependencies-explicitly)

## Write gates & confirmation

When a skill acts on the user's behalf, showing the action before it happens is the safeguard —
these bullets cover when/how that gate fires.

### Propose, don't just do

Every consequential write — a new idea added to a tracker, a choice of what to build, an
implementation plan — gets shown to the user and confirmed before it happens. A recommendation is
not a decision. Where a skill has more than one such gate, they should be explicitly
numbered/cross-referenced so drift is easy to catch on review, not left implicit — and that
cross-reference needs to mirror the skill's actual structure (one entry per step/section, e.g. a
table keyed to step number) rather than free prose that bundles items under a loose phrase, and
should carry an explicit note to update it in the same edit that changes what it's summarizing.

### A default the user never saw isn't a default

It's undisclosed forced behavior. Any skill with a built-in fallback (a threshold, a selection
strategy, a term list) must surface that fallback's concrete effect during setup/bootstrap and get
it confirmed, not just ask "want the defaults?" and move on — a special case of
[Propose, don't just do](#propose-dont-just-do), applied to defaults specifically.

### One check-in, not two

When a skill needs several related confirmations before proceeding (e.g. scope and understanding),
fold them into a single message rather than gating twice in a row. Back-to-back stops for adjacent
information don't add safety — they train the user to skim past confirmations instead of actually
reading them, which undermines [Propose, don't just do](#propose-dont-just-do) more than it
reinforces it.

### Numbered choices, not just labels

When presenting two or more options for the user to pick from, number them `1.`, `2.`, `3.`... in
a single sequential list, regardless of what other labels each option carries (a tier name,
"wildcard", a category). A descriptive label explains an option; it isn't a substitute for a
number the user can just say back ("go with 2") to confirm unambiguously.

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

## Structure & reuse

How a skill's checks and prompts get built — coverage should come from the shape of the problem
and from reusing what already exists, not from listing cases as they're remembered.

### Reuse a judgment test, don't invent a parallel one

When a skill needs to classify or filter something in a new context — deciding whether existing
documentation belongs somewhere else, say, rather than a fresh capture candidate — check first
whether an existing test elsewhere in the skill already answers the same underlying question, just
pointed at different input, before drafting a new one. A second, slightly-different test for what
is structurally the same judgment call is harder to keep consistent than one test applied twice,
and the two versions will eventually drift from each other as one gets refined and the other
doesn't.

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

Installing a skill means copying its folder, so anything a person needs to evaluate or use it —
what it does, when it triggers, example runs, prerequisites — belongs inside that folder as its
own `README.md`, not in a repo-level file that doesn't get copied along. Different concern from
[Progressive disclosure](#progressive-disclosure) (which is about what Claude loads into context)
— this is about what a human still has once the skill is installed elsewhere. The top-level README
stays a thin index pointing into each skill's own docs, rather than duplicating them.

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

### State hard dependencies explicitly

Distinguish them from what degrades gracefully. If a skill can't function at all without something
external (an MCP server, a specific tool), that belongs up front in its own docs — not just
handled gracefully at runtime once someone's already hit it. Dependencies the skill already works
around on its own (per
[Unreachable isn't resolved](#unreachable-isnt-resolved-in-either-direction)) don't need the same
billing; conflating the two either buries a real blocker behind a wall of caveats or overstates
how fragile the skill actually is.

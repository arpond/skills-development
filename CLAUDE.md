# skills-development

Instructions for working in this specific repo, on top of global preferences.

## Review loop

After a non-trivial change to a skill in this repo (a new feature, a fix, a rework — not a single
typo fix), **or to either shared file — `DESIGN_PHILOSOPHY.md` or `CONVENTIONS.md`** — offer a
review pass rather than running it unasked or waiting to be asked every time. One short offer, e.g.
"Want a review pass?" — not four separate offers for the four checks below.

If the user says yes, run these four checks in order, on whatever was just changed:

1. **Design philosophy.** Check the changed files against every bullet in `DESIGN_PHILOSOPHY.md` —
   **including when the changed file is `CONVENTIONS.md` or `CLAUDE.md` itself**, which are text
   that gets read and acted on like any skill and are subject to the same bullets (see that file's
   opening note). Report violations found; fix what's confirmed. **Also check `CONVENTIONS.md`** — if the change
   touched anything a spec covers, verify the skill's inline copy still matches it, since the
   copies are what actually run (a skill can't cite a repo-root file) and drift between them stays
   invisible until two skills disagree inside the same project. **For a brand-new skill, check it
   against every spec there**, not just ones the diff touched: a new skill has no prior
   implementation for a drift check to catch, so nothing else would ever flag a spec it simply
   never implemented. **N/A when the change is to
   `DESIGN_PHILOSOPHY.md` itself** — checking a file against itself is circular, not a real check;
   skip straight to pass 2. **Also check size, not just the diff**: if the skill's always-loaded
   core file (the one read on every invocation, not read on a trigger condition) is at or
   above ~500 lines, do a quick whole-file skim — not just the changed lines — specifically for
   Progressive disclosure violations: content that only matters rarely/once but lives in the core
   read anyway. A diff-scoped pass can't catch drift sitting in untouched sections, which is exactly
   how this kind of bloat accumulates unnoticed across many small, individually-reasonable changes;
   size crossing the threshold is the trigger to zoom out. Skip this check when the file's under the
   threshold — most reviews stay diff-scoped and cheap, this is only for the file that's grown
   enough to warrant a fresh look.
2. **Repetition, complexity, verbosity.** Reread the changed files fresh — same statement made
   more than once across files or sections, mechanisms that could reuse an existing pattern
   instead of inventing a parallel one, prose that's denser or longer than the content requires.
   On `DESIGN_PHILOSOPHY.md` this means checking bullets against each other, not just against a
   skill; on `CONVENTIONS.md`, checking specs against each other, and each spec against its own
   inline copies — a spec restated in three skills is three chances for the same sentence to say
   three slightly different things.

   Three concrete tests, from `DESIGN_PHILOSOPHY.md`'s "A rule is a sentence" and
   `CONVENTIONS.md`'s "Vocabulary":
   - a rule not in its own sentence, or in one over twenty-five words — split it (exactly
     twenty-five passes)
   - several instructions in one sentence or paragraph — make it a list, one per item
   - a concept named by a word in the Vocabulary table's right-hand column — use the left-hand one

   `python ste-writing/scripts/ste-lint.py --cap 25 --show <file>` lists the first two with line
   numbers. It can't tell a rule from its explanation, so read the hits, don't count them.
   `python check-hard-rules.py` does the rule-bearing half mechanically: for every hard-rules
   table row in every skill, it finds the closest prose sentence and reports whether that sentence
   fits the cap. A row with no close sentence is a rule that lives only in the index.

   Not findings, for any of the three tests: the principle's out-of-scope list (frontmatter,
   README prose and dialogue, vendored text) and `CONVENTIONS.md`'s open-gap sites. Not
   repetition: a hard-rules table row restating its step (the table is an index by spec), a
   mandated inline copy of a `CONVENTIONS.md` spec, a core file's pointer to a companion, a file's
   own intro previewing the steps below it, and a README summarising `SKILL.md` (documentation
   travels with the skill). Repetition is the same rule stated twice in operative prose, or a
   README procedure and its `SKILL.md` twin drifting apart.
3. **Gaps.** Functional/logical holes, not wording — contradictory inputs, malformed stored state,
   ambiguous write targets when more than one file/location can hold state, claims about external
   facts (committed, installed, reachable) that are asserted but never checked, third states
   collapsed into a binary, and whether the skill now covers more than one orthogonal capability
   (different trigger, audience, or write target) that grew in gradually and was never deliberately
   split (see `DESIGN_PHILOSOPHY.md`'s "Split along orthogonal triggers, not around size"). Distinct
   from pass 1: philosophy violations are "breaks a stated rule," gaps are "no rule covers this
   yet." On `DESIGN_PHILOSOPHY.md` itself, a gap looks like a principle with no worked example, an
   ambiguous cross-reference, or two bullets that quietly contradict each other. On
   `CONVENTIONS.md`, it looks like a spec with no implemented-by table, a table asserting something
   that isn't actually true of the skill named, a spec stating a rule with no test for applying it,
   or a requirement no skill has ever met — which is a spec nobody wrote from, not a standard.
4. **Shared-file additions.** Given what passes 1-3 turned up, is there a new pattern here that
   would generalize to other skills in this repo, not just this one? If yes, **decide which shared
   file it belongs in before drafting it**, using the test in `DESIGN_PHILOSOPHY.md`'s "Principles
   vs. specs": ask what failure the rule prevents. *Two implementations doing it differently*, where
   each looks fine alone and only the disagreement is wrong → a `CONVENTIONS.md` spec, which also
   needs its implemented-by table and an inline copy in each skill that implements it, since a skill
   can't cite a repo-root file. *One judgement made badly*, no second implementation involved → a
   `DESIGN_PHILOSOPHY.md` bullet. A rule can be both, and the embedded spec is usually the half
   that got written first because it's easier to state — split it rather than filing the whole
   thing under one, with the principle keeping the why and pointing at the spec.

   Either way, propose before writing — same "propose, don't just do" gate as any other change to a
   shared file. Two things that look like specs and aren't: a prohibition has no shared
   implementation to drift from, and a rule with only one implementation isn't a spec yet.

   **A pattern found here is not licence to restate an existing rule.** If a spec already covers it
   and some skills don't match, that's a conformance finding for pass 1, not an addition — and the
   fix is bringing the skills up to the spec or recording an explicit `✗`, never widening the spec
   to describe what the implementations happen to do. Widening is sometimes right, but it's a
   deliberate change to the rule with its own proposal, not a by-product of noticing drift.

   When the change under review *is* `DESIGN_PHILOSOPHY.md` or `CONVENTIONS.md`, this pass instead
   asks whether passes 2-3 surfaced a wording/structure fix worth applying now, same propose-first
   gate.

Timing: offer once, after the change is otherwise done and deployed — not mid-edit, and not
stacked as a second ask right after some other confirmation (see "One gate, not two"). If
declined, don't re-offer for that same change; the user can ask for any individual pass (or the
whole loop) at any time without waiting for the offer.

## Deploying a skill locally

After editing a skill's files in this repo, redeploy to make the change live for this session's
own use: overwrite the matching folder under the user's local `~/.claude/skills/<name>/` with the
repo's version, then commit the repo change. Both steps belong to finishing an edit, not just the
edit itself.

## Changelog

`CHANGELOG.md` gets an entry when a change alters what a skill does for its user, what an author
here has to follow, or how the repo is organised. Not every commit. Write it in the same edit as
the change.

The format keeps the file scannable; match it:
- One heading per period, as `## <theme> · <start date>`. Start a new period when the theme
  changes, not the date; name it by what changed, not when.
- Three fixed sections in order, omitted when empty: **Skills**, **Standards**, **Tooling**.
- One line per item, skill or file name first, at most 25 words. Reasoning stays in the linked
  file or the commit.
- Prose in `ste-writing`'s flavored mode: short sentences, active voice, simple tenses, no
  semicolons. British spelling, per this repo. Lint with
  `python ste-writing/scripts/ste-lint.py CHANGELOG.md`; target under 2.5 per 100 words, and
  treat list-as-paragraph and possessive-`'s` hits as noise.

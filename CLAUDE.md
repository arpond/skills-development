# skills-development

Instructions for work in this specific repo, on top of global preferences.

## Review loop

Offer a review pass after a non-trivial change to a skill in this repo (a new feature, a fix, a
rework, not a single typo fix), **or to either shared file, `DESIGN_PHILOSOPHY.md` or
`CONVENTIONS.md`**. Do not run it unasked, and do not wait to be asked every time. One short
offer, e.g. "Want a review pass?", not four separate offers for the four checks below.

If the user says yes, run these four checks in order, on whatever was just changed:

1. **Design philosophy.** Check the changed files against every principle in
   `DESIGN_PHILOSOPHY.md`. **This includes a change to `CONVENTIONS.md` or `CLAUDE.md` itself.**
   Both are text that is read and acted on like any skill, and both are subject to the same
   principles (see that file's opening note). Report violations found. Fix what is confirmed.
   - **Also check `CONVENTIONS.md`.** If the change touched anything a spec covers, make sure the
     skill's inline copy still matches it. The copies are what runs, because a skill cannot cite a
     repo-root file. Drift between them stays invisible until two skills disagree inside the same
     project.
   - **For a brand-new skill, check it against every spec there**, not only the ones the diff
     touched. A new skill has no prior implementation for a drift check to catch, so nothing else
     would ever report a spec it never implemented.
   - **N/A when the change is to `DESIGN_PHILOSOPHY.md` itself.** A check of a file against itself
     is circular, not a real check. Skip straight to pass 2.
   - **Also check size, not only the diff.** If the skill's core file (the one read on every
     invocation, not on a trigger condition) is at or above ~500 lines, skim the whole file, not
     only the changed lines, for Progressive disclosure violations: content that matters rarely or
     once but lives in the core read anyway. A diff-scoped pass cannot catch drift in untouched
     sections. That is exactly how this kind of bloat accumulates unnoticed across many small,
     individually reasonable changes. Size across the threshold is the trigger to look at the whole
     file. Skip this check when the file is under the threshold. Most reviews stay diff-scoped and
     cheap. This is only for the file that grew enough to warrant a fresh look.
2. **Repetition, complexity, verbosity.** Reread the changed files fresh. Look for the same
   statement made more than once across files or sections, a mechanism that could reuse an existing
   pattern instead of a parallel one, and prose that is denser or longer than the content requires.
   On `DESIGN_PHILOSOPHY.md` this means a check of principles against each other, not only against
   a skill. On `CONVENTIONS.md`, a check of specs against each other, and of each spec against its
   own inline copies. A spec restated in three skills is three chances for the same sentence to say
   three slightly different things.

   Three concrete tests, from `DESIGN_PHILOSOPHY.md`'s "A rule is a sentence" and
   `CONVENTIONS.md`'s "Vocabulary":
   - a rule not in its own sentence, or in one over twenty-five words: split it (exactly
     twenty-five passes)
   - several instructions in one sentence or paragraph: make it a list, one per item
   - a concept named by a word in the Vocabulary table's right-hand column: use the left-hand one

   `python ste-writing/scripts/ste-lint.py --cap 25 --show <file>` lists the first two with line
   numbers. It cannot tell a rule from its explanation, so read the hits, do not count them.
   `python check-hard-rules.py` does the rule-bearing half mechanically. For every hard-rules table
   row in every skill, it finds the closest prose sentence and reports whether that sentence fits
   the cap. A row with no close sentence is a rule that lives only in the index.

   Not findings, for any of the three tests: the principle's out-of-scope list (frontmatter, README
   prose and dialogue, vendored text) and `CONVENTIONS.md`'s open-gap sites. Not repetition: a
   hard-rules table row that restates its step (the table is an index by spec), a mandated inline
   copy of a `CONVENTIONS.md` spec, a core file's pointer to a companion, a file's own intro that
   previews the steps below it, and a README that summarises `SKILL.md` (documentation travels with
   the skill). Repetition is the same rule stated twice in operative prose, or a README procedure
   and its `SKILL.md` twin that drift apart.
3. **Gaps.** Functional or logical holes, not wording: contradictory inputs, malformed stored
   state, ambiguous write targets when more than one file or location can hold state, claims about
   external facts (committed, installed, reachable) asserted but never checked, third states
   collapsed into a binary, and a skill that now covers more than one orthogonal capability
   (different trigger, audience, or write target) that grew gradually and was never deliberately
   split (see `DESIGN_PHILOSOPHY.md`'s "Split along orthogonal triggers, not around size").
   Distinct from pass 1. A philosophy violation "breaks a stated rule". A gap is "no rule covers
   this yet". On `DESIGN_PHILOSOPHY.md` itself, a gap looks like a principle with no worked
   example, an ambiguous cross-reference, or two principles that quietly contradict each other. On
   `CONVENTIONS.md`, it looks like a spec with no implemented-by table, a table that asserts
   something untrue of the skill named, a spec that states a rule with no test to apply it, or a
   requirement no skill has ever met, which is a spec nobody wrote from, not a standard.
4. **Shared-file additions.** Given what passes 1-3 found, is there a new pattern here that would
   generalise to other skills in this repo, not only this one? If yes, **decide which shared file
   it belongs in before you draft it**, with the test in `DESIGN_PHILOSOPHY.md`'s "Principles vs.
   specs": ask what failure the rule prevents. *Two implementations that do it differently*, where
   each looks fine alone and only the disagreement is wrong → a `CONVENTIONS.md` spec. That also
   needs its implemented-by table and an inline copy in each skill that implements it, because a
   skill cannot cite a repo-root file. *One judgement made badly*, no second implementation
   involved → a `DESIGN_PHILOSOPHY.md` principle. A rule can be both. The embedded spec is usually
   the half written first, because it is easier to state. Split it rather than file the whole thing
   under one. The principle keeps the why and points at the spec.

   Either way, propose before you write. This is the same "propose, don't just do" gate as any
   other change to a shared file. Two things that look like specs and are not: a prohibition has no
   shared implementation to drift from, and a rule with only one implementation is not a spec yet.

   **A pattern found here is not licence to restate an existing rule.** If a spec already covers it
   and some skills do not match, that is a conformance finding for pass 1, not an addition. The fix
   is to bring the skills up to the spec or record an explicit `✗`, never to widen the spec to
   describe what the implementations happen to do. A wider spec is sometimes right, but it is a
   deliberate change to the rule with its own proposal, not a by-product of noticed drift.

   When the change under review *is* `DESIGN_PHILOSOPHY.md` or `CONVENTIONS.md`, this pass instead
   asks whether passes 2-3 surfaced a wording or structure fix worth an edit now, under the same
   propose-first gate.

Timing: offer once, after the change is otherwise done and deployed. Not mid-edit, and not stacked
as a second ask right after some other confirmation (see "One gate, not two"). If declined, do not
re-offer for that same change. The user can ask for any individual pass (or the whole loop) at any
time without the offer.

## Deploying a skill locally

After an edit to a skill's files in this repo, redeploy to make the change live for this session's
own use. Overwrite the matching folder under the user's local `~/.claude/skills/<name>/` with the
repo's version, then commit the repo change. Both steps belong to the edit, not only the edit
itself.

## Prose standards

Human-facing prose in this repo is in `ste-writing`'s flavored mode: short sentences, active
voice, simple tenses, no semicolons, no contractions. British spelling, per this repo. Lint with
`python ste-writing/scripts/ste-lint.py --cap 25 <file>`, the descriptive-prose cap. Target under
2.5 per 100 words, and treat list-as-paragraph hits as noise.

It applies to:
- `CHANGELOG.md`
- every `README.md`, repo root and per skill. The prose only, not the fenced example dialogue,
  which quotes how Claude speaks.
- every per-skill `changelog.md`. Its entries reach the user nearly verbatim on a version gap.
- `CONVENTIONS.md` and this file. Both are facts and procedures, not reasoning.

It does not apply to `SKILL.md` and its companions, `DESIGN_PHILOSOPHY.md`, vendored text, or a
skill's `references/`. Those keep only the 25-word cap and the list-per-instruction rule from
`DESIGN_PHILOSOPHY.md`.

## Changelog

`CHANGELOG.md` gets an entry when a change alters what a skill does for its user, what an author
here has to follow, or how the repo is organised. Not every commit. Write it in the same edit as
the change.

The format keeps the file scannable. Match it:
- One heading per period, as `## <theme> · <start date>`. Start a new period when the theme
  changes, not the date. Name it by what changed, not when.
- Three fixed sections in order, omitted when empty: **Skills**, **Standards**, **Tooling**.
- One line per item, skill or file name first, at most 25 words. Reasoning stays in the linked
  file or the commit.

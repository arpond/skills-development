# skills-development

Instructions for working in this specific repo, on top of global preferences.

## Review loop

After a non-trivial change to a skill in this repo (a new feature, a fix, a rework — not a single
typo fix), **or to `DESIGN_PHILOSOPHY.md` itself**, offer a review pass rather than running it
unasked or waiting to be asked every time. One short offer, e.g. "Want a review pass?" — not four
separate offers for the four checks below.

If the user says yes, run these four checks in order, on whatever was just changed:

1. **Design philosophy.** Check the changed files against every bullet in `DESIGN_PHILOSOPHY.md`.
   Report violations found; fix what's confirmed. **N/A when the change is to
   `DESIGN_PHILOSOPHY.md` itself** — checking a file against itself is circular, not a real check;
   skip straight to pass 2.
2. **Repetition, complexity, verbosity.** Reread the changed files fresh — same statement made
   more than once across files or sections, mechanisms that could reuse an existing pattern
   instead of inventing a parallel one, prose that's denser or longer than the content requires.
   On `DESIGN_PHILOSOPHY.md` this means checking bullets against each other, not just against a
   skill.
3. **Gaps.** Functional/logical holes, not wording — contradictory inputs, malformed stored state,
   ambiguous write targets when more than one file/location can hold state, claims about external
   facts (committed, installed, reachable) that are asserted but never checked, third states
   collapsed into a binary. Distinct from pass 1: philosophy violations are "breaks a stated rule,"
   gaps are "no rule covers this yet." On `DESIGN_PHILOSOPHY.md` itself, a gap looks like a
   principle with no worked example, an ambiguous cross-reference, or two bullets that quietly
   contradict each other.
4. **Philosophy additions.** Given what passes 1-3 turned up, is there a new pattern here that
   would generalize to other skills in this repo, not just this one? If yes, propose it as a new
   `DESIGN_PHILOSOPHY.md` bullet before writing it — same "propose, don't just do" gate as any
   other change to a shared file. When the change under review *is* `DESIGN_PHILOSOPHY.md`, this
   pass instead asks whether passes 2-3 surfaced a wording/structure fix worth applying now, same
   propose-first gate.

Timing: offer once, after the change is otherwise done and deployed — not mid-edit, and not
stacked as a second ask right after some other confirmation (see "one check-in, not two"). If
declined, don't re-offer for that same change; the user can ask for any individual pass (or the
whole loop) at any time without waiting for the offer.

This loop isn't exclusive to `commit-message-check` — apply it to whichever skill (or
`DESIGN_PHILOSOPHY.md`) just changed.

## Deploying a skill locally

After editing a skill's files in this repo, redeploy to make the change live for this session's
own use: overwrite the matching folder under the user's local `~/.claude/skills/<name>/` with the
repo's version, then commit the repo change. Both steps belong to finishing an edit, not just the
edit itself.

# ste-writing

Rewrites prose — docs, READMEs, PR descriptions, error messages, release notes, comments, tool
descriptions, system prompts — into ASD-STE100 Simplified Technical English, and reviews existing
text for STE violations. The point is removing "AI slop": the controlled-language rules (short
simple sentences, active voice, simple tenses, one word per meaning, no marketing adjectives, no
phrasal verbs, no nominalisations) happen to target exactly the tics that make text read as
machine-generated. A bundled lint script scores a draft so "clean" is measured, not asserted.

Two modes: **strict** (procedures, runbooks, safety text, error messages — every rule, both
length caps, the strict word set) and **STE-flavored** (general prose — the sentence, tense,
voice, and noun-cluster discipline, with the 875-word dictionary lockdown relaxed so text still
reads naturally). Never applied to code, identifiers, or command syntax.

**Origin.** Vendored from
[woosal1337/blog — ep01 "The cure for AI slop"](https://github.com/woosal1337/blog/tree/e77daea86f8ef76241647f750b784468e3267946/videos/ep01-the-cure-for-ai-slop)
at upstream commit `e77daea` (2026-08-08), not authored in this repo. Diff against that commit, not
`main`, to see what changed upstream since then. Local changes: the lint script moved to `scripts/`, `python3` became
`python` in the lint instructions, a hard-rules table was added to `SKILL.md` to match this
repo's conventions, and the lint script diverges from upstream in four ways: it unwraps
hard-wrapped paragraphs before splitting sentences (upstream counts each wrapped line as a
sentence, so long sentences in wrapped markdown never registered); it splits sentences that open
or close with markdown emphasis; it keeps a code fence's newlines so line numbers stay true; and it
gains `--cap N` and `--show`, where `--show` lists long sentences with line numbers and counts
them the way this repo's "A rule is a sentence" principle does (parentheticals and bold labels
excluded, inline code included). The STE score itself is computed as upstream does. Rule content
is unchanged. The skill is unofficial and not affiliated with
ASD; the full standard is free at https://asd-ste100.org.

Files:
- `SKILL.md` — the rule set (keyed to Issue 9 rule numbers), guards, the two modes, and the
  verify step. Read on every invocation.
- `ste-recurring-errors.md` — the standard's own list of the 39 most frequent writer errors with
  approved replacements, plus the ten that matter for software docs. Read only in strict mode.
- `scripts/ste-lint.py` — regex-based scorer: counts passive voice, complex tenses, long
  sentences, semicolons, contractions, banned and marketing words, phrasal verbs, nominalisations,
  and reports violations per 100 words. Run on a draft during the verify step; `--strict` adds the
  strict word set, `--json` gives the full breakdown, `--fail-over N` exits 1 above a threshold.

## What it writes

**Nothing into your project by default.** Rewritten or reviewed text is returned in the
conversation. The verify step lints a draft, which means writing the draft to a temporary file
first — that goes in a scratch location, not your repo. If you ask for the rewrite to be applied
to a file, that is an ordinary edit you requested, not something the skill does on its own.

The lint script only reads the files it is given and prints a score. It never writes.

## Requires

Nothing for write, rewrite, and review — they are pure prose work. The verify step needs Python 3
(standard library only) to run `scripts/ste-lint.py`; without it, `SKILL.md` falls back to a
ten-item manual checklist, so the skill degrades rather than blocks.

## When it triggers

- "Make this README not sound like AI."
- "Rewrite this PR description in plain English."
- "Review these release notes for STE violations." (review mode — a violation table, no rewrite)
- "Write the runbook for this in Simplified Technical English." (strict mode)
- "Enforce a controlled writing style on these docs."

## Example: rewrite

```
You: Rewrite this so it doesn't sound like AI:

     "Leveraging our robust caching layer, requests are seamlessly served from
     memory, ensuring that latency has been dramatically reduced whilst
     additionally providing a cutting-edge experience for users."

Claude: [invokes ste-writing — flavored mode, descriptive prose]

        The caching layer serves requests from memory. This reduces latency.

        [writes both versions to a scratch file, runs
         python <skill-dir>/scripts/ste-lint.py on each]

        Lint: original 27.3 per 100 words (marketing ×3, banned ×4, passive,
        complex tense, phrasal). Rewrite 0.0 per 100 words.

        Dropped: "cutting-edge experience for users" — no fact behind it, so
        nothing to keep. Kept every other claim.
```

## Example: review

```
You: Review this paragraph for STE violations, don't rewrite it.

Claude: [invokes ste-writing — review mode]

        | Rule | Original | Simplified |
        |---|---|---|
        | 3.2 simple tenses | we have received the report | we received the report |
        | 3.7 verb for action | perform an analysis of the log | analyze the log |
        | 8.1 no semicolons | ...fails; the log shows... | ...fails. The log shows... |
        | 9.3 no phrasal verbs | spin up a worker | start a worker |

        Left alone: "the field is required" — past participle as adjective
        (3.3), not passive.
```

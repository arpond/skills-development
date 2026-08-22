# Selection strategies (optional)

Read this file only when the tracker's `Selection strategy:` line is anything other than plain
`top-tier`, or when the user is setting one up or asking to change it. If a project never touches
this setting, none of this applies and you never need to read it.

Selection strategy controls how Step 4 of `SKILL.md` **presents** candidates from the ranking
Step 3 already computed — it never changes how ranking itself works.

**Quick reference** — full detail for each is under Modes/Capping below:

| Syntax | Kind | Default | What it does |
|---|---|---|---|
| `top-tier` | base mode (pick one) | — | Top pick, plus close contenders if genuinely close |
| `spread(N)` | base mode (pick one) | N=3 | Top pick from each of the top N tiers |
| `wildcard(mode)` | additive | `mode`=`rotate` | Extra pick outside ranking; exempt from `max-options(N)` |
| `quick-win` | additive | — | Appends the cheapest candidate; same exemption as `wildcard` |
| `category-rotation(window=N)` | additive | N=5 | Tie-break bias toward categories that haven't shipped recently |
| `max-options(N)` | additive | N=4 | Cap on the base mode's own picks (close contenders / tier picks) — not a total cap, see Capping |

Numbering the final list is `SKILL.md` Step 4's rule, not this file's — it applies regardless of
strategy. What this file adds: display order within that numbered list is base-mode pick(s) first
(tier order for `spread(N)`), then `wildcard`, then `quick-win` — and each mode's gate checks
against every pick placed earlier in that order, not just the base pick, so the same candidate
never occupies two numbered lines under two different labels.

## Tracker format

In the Goals block:

```markdown
Selection strategy: top-tier
```

Values, combinable space- or `+`-separated, e.g. `spread(3) + wildcard(rotate) + quick-win`.
`top-tier` and `spread(N)` are the two base modes and mutually exclusive; `wildcard`,
`quick-win`, `category-rotation`, and `max-options(N)` are additive on top of either base mode.

Two separate counts exist — `spread(N)` (how many tiers to generate from) and `max-options(N)`
(how many of the base mode's picks to display) — set independently, neither piggybacking on the
other's number. See their own entries under Modes, and Capping for how they interact.

## Modes

Each entry below covers what the mode means *and* what Step 4 does with it — one place per mode.

- **`top-tier`** (default) — the skill's original, always-available behaviour. Step 4 presents the
  top tier's winner alone, or up to `max-options(N)` total (winner + close contenders, default 4)
  if the ranking is genuinely close — never more than that even if more candidates are arguably
  close, and never padded up to it if only the winner is actually clear. The close-contender count
  is `max-options(N)`'s job, not a separate `top-tier`-only setting — see Capping. Reasoning stays
  tied to specific tiers either way — not "this seems good" but "this serves tier 1 because X" or
  "this is tier-3 maintenance work but nothing above it is ready to build, since Y."
- **`spread(N)`** — Step 4 presents the top candidate from each of the top N tiers (default
  N=3, capped at however many tiers exist), one numbered line per tier — "1. Tier 1 pick: X,
  because...", "2. Tier 2 pick: Y, because..." — for real cross-tier choice instead of one narrow
  answer. Tier 1's pick is still the top recommendation unless a tied-goal conflict (`SKILL.md`
  Step 3/4) overrides that. If one of the top N tiers has no outstanding candidate at all, skip
  its line rather than fabricating a weak pick or silently pulling one from a lower tier to
  backfill the count — say so in one clause ("Tier 2 has nothing outstanding right now") so the
  gap is visible, and let the numbered list simply be shorter than N that run. If one of the top
  N tiers *is itself* an unresolved tied-goal conflict (`SKILL.md` Step 3), that tier contributes
  both co-contenders as their own numbered lines instead of one pick — same as any other
  tied-goal conflict, they're never dropped to fit a count (see Capping), so this can legitimately
  make the list longer than N or push past `max-options(N)` by exactly the size of that one tie.
- **`wildcard(mode)`** — Step 4 appends one extra, clearly-labelled candidate chosen *outside*
  normal ranking, alongside the base proposal, as the next number in the list: "3. Wildcard: Z
  (picked via <source>, because <reason>)". `mode` is:
  - `rotate` (default) — cycles oldest -> random -> low-tier -> repeat across runs, tracked via
    `wildcard(rotate: last=oldest)` inline in the Selection strategy line, updated after each
    presentation. An unrecognised or missing `last=` value just restarts the cycle from the top
    — never treat it as an error.
  - `oldest` — the outstanding idea that's sat longest without being picked.
  - `random` — a random draw from all outstanding candidates.
  - `low-tier` — the candidate from the single lowest tier that still has an outstanding item;
    if more than one, apply the cheapest-first judgement described under `quick-win` below.
  - `tagged` — only pulls ideas the user explicitly marked `(wildcard)` when adding them, e.g.
    `- I7: **Idea name** (wildcard) — rationale...`. None tagged -> no wildcard to offer this run.

  Read condition: only add a wildcard if there's a candidate left over that isn't already one of
  the base picks. If the pool's too small for a distinct pick, skip the wildcard silently rather
  than re-listing the same item under a different label — that's padding, not variety. When the condition
  passes, the wildcard always shows — it's not counted by or trimmed for `max-options(N)` (see
  Capping); it's a fixed, self-limiting +1, not part of the base-mode count.
- **`quick-win`** — Step 4 appends the cheapest/fastest outstanding candidate with clear value,
  regardless of tier, as the next number in the list: "4. Quick win: W (cheap, tier-N, could
  slot in alongside or instead of the above)". "Cheapest" isn't a stored metric — judge it the
  same way you'd judge tier fit in Step 3: think concretely about what building each candidate
  would actually involve (scope described in its rationale, files/functions it touches if named)
  and pick whichever reads as smallest, with a defensible one-line reason ("touches one function,
  no new UI"). Same read condition as
  wildcard, extended to cover wildcard's own pick too: skip it if the cheapest candidate is
  already one of the base picks *or* already the wildcard pick (checked in that order, since
  wildcard is placed earlier in display order — see Modes intro) — a candidate never occupies two
  numbered lines under two different labels. Same exemption as `wildcard`: when the read condition passes,
  quick-win always shows, uncounted by `max-options(N)`.
- **`category-rotation`** or **`category-rotation(window=N)`** (default N=5) — when the base
  pick's ranking has a genuine close call, Step 4 prefers whichever candidate's category hasn't
  appeared in the last N Done entries (across all categories combined, oldest-first count, live
  tracker only — the one deliberate exception to the combined-pool rule, since this is a "what
  shipped lately" window rather than a history lookup; fewer than N total live Done entries ->
  insufficient history, skip the bias), and says so ("Y also serves
  tier 1 equally well and its category hasn't shipped recently"). Only affects the base
  `top-tier`/`spread(N)` pick's own close-call, not each `spread(N)` tier independently; never
  overrides a clear tier-1-vs-lower-tier win, only breaks ties. **This mode sits last of the four
  signals that can bear on the same close call.** See `SKILL.md` Step 3's precedence ladder for
  the full ordering; it loses to a stored tie-break rule, to risk-mitigation, and to synergy, since
  it's a content-blind diversity heuristic and those are all grounded in something specific.

## Setup (from `setup.md`)

Present the full option set explicitly, not just an open "any preference?" — the user can't pick
combinations they were never shown. Two separate choices, since they compose differently:

1. **Base mode (pick exactly one)**: `top-tier` (single best pick, default) or `spread(N)` (one
   candidate per top tier). One sentence each is enough.
2. **Additive modifiers (pick any number, or none)**: `wildcard`, `quick-win`,
   `category-rotation`, `max-options(N)` — each stacks on top of whichever base mode was picked.
   One sentence each; mention `max-options(N)` defaults to 4 and controls how many of the base
   mode's own picks show (close contenders / tier picks) — `wildcard` and `quick-win` are separate
   fixed extras it doesn't count, so it's not a literal cap on everything shown.

Then show at least one worked example of combining a base mode with modifiers, so the free-text
combination syntax itself is demonstrated rather than left implicit — e.g. "so if you wanted the
top pick from each of the top 3 tiers, plus a rotating wildcard, plus the cheapest outstanding
option, that'd be written `spread(3) + wildcard(rotate) + quick-win`." This is opt-in enrichment,
not a mandatory extra setup burden — don't turn it into another long interrogation; a plain
`top-tier` with no modifiers is a completely fine answer if the user doesn't care. Write their
choice as the `Selection strategy:` line, using the combinable space- or `+`-separated syntax
described above.

**This is a single message, not a negotiation.** Show the menu below (or an equivalent one
covering the same ground) once, then wait for their pick; don't ask a bare "want a selection
strategy?" first and only reveal the options if they say yes. Something along these lines
satisfies it:

> By default I'll always present the single top-ranked idea (`top-tier`). A few optional ways to
> change that:
> - `spread(N)` — show the top pick from each of the top N tiers instead of just one (default 3)
> - `wildcard` — add one extra pick outside the ranking (rotates through oldest / random / low-tier)
> - `quick-win` — add the cheapest outstanding candidate regardless of tier
> - `category-rotation` — break close ties in favour of a category that hasn't shipped in the last
>   5 Done entries (`category-rotation(window=N)` to change that number)
> - `max-options(N)` — cap how many of the base mode's own picks are shown (default 4)
>
> These combine, e.g. `spread(3) + wildcard(rotate) + quick-win`. Happy with the default
> (`top-tier`), or want to combine some of these?

Reusing this wording verbatim is fine — the point is that every option is named and described
before the user answers, not that the phrasing is original each time.

## Changing it later (from `session-start.md` Step 0.5)

Not fixed at setup. The user can change it any time by just saying so (e.g. "show me more
options next time", "add a wildcard", "drop category-rotation") — edit the line in place, no
need to re-run the full `setup.md` interrogation. If they name a concrete mode/modifier, just
apply it. If instead they ask to change it but aren't specific about what's available (e.g. "what
else can I do here?", "show me the options"), show the same menu from the Setup section above
rather than guessing at what they mean — don't make them already know the syntax to ask about it.

## Capping combined output

`max-options(N)` (default 4) caps the **base mode's own picks** — `top-tier`'s close contenders,
or `spread(N)`'s tier picks — not the total shown. `wildcard` and `quick-win` are separate, fixed
extras: each shows at most once, whenever its own read condition passes, and neither is trimmed for or
counted by `max-options(N)`. So the actual total on screen can be `max-options(N)` +1 (wildcard)
+1 (quick-win) at most — a small, bounded, predictable overshoot, not the unranked pile this skill
exists to avoid; always mark exactly one pick as *the* top recommendation regardless of how many
supplementary lines accompany it.

When the base mode alone would produce more than `max-options(N)`, trim it down: for `spread(N)`,
drop tier picks lowest-tier-first; for `top-tier`, drop close contenders weakest-first. An
unresolved tied-goal conflict's co-contenders are never dropped — they're a real ranking
ambiguity, handled in `SKILL.md` Step 3/Step 4, and take priority over `max-options(N)` even if
honouring it means exceeding the cap (by one per unresolved tie in play — two co-contenders
replacing what would otherwise be a single slot; more than one simultaneous tie is rare but
follows the same rule).

**Degenerate values.** Every `N` here (`spread(N)`, `max-options(N)`,
`category-rotation(window=N)`) means what it says only for N ≥ 1; treat 0, negative, or
non-numeric input as a typo, not a valid "show nothing" instruction — clamp to 1 and mention the
correction rather than silently presenting an empty list or erroring. There's always at least one
slot: the single top recommendation is never trimmed away by any cap, so `max-options(N)` below
what's needed to hold it still shows that one pick, even if that means showing fewer than N when
N was set to something like 1 — `max-options(N)` never zeroes out the base recommendation itself.
`wildcard` and `quick-win` are unaffected by any of this since `max-options(N)` doesn't govern
them at all (see above).

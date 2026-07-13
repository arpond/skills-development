# Selection strategies (optional)

Read this file only when the tracker's `Selection strategy:` line is anything other than plain
`top-tier`, or when the user is setting one up or asking to change it. If a project never touches
this setting, none of this applies and you never need to read it.

Selection strategy controls how Step 4 of `SKILL.md` **presents** candidates from the ranking
Step 3 already computed -- it never changes how ranking itself works.

## Tracker format

In the Goals block:

```markdown
Selection strategy: top-tier
```

Values, combinable space- or `+`-separated, e.g. `spread(3) + wildcard(rotate) + quick-win`.
`top-tier` and `spread(N)` are the two base modes and mutually exclusive; `wildcard`,
`quick-win`, and `category-rotation` are additive on top of either base mode.

## Modes

Each entry below covers what the mode means *and* what Step 4 does with it -- one place per mode.

- **`top-tier`** (default) -- the skill's original, always-available behavior. Step 4 presents
  the top tier's winner, or 2-3 close contenders if the ranking is genuinely close, with
  reasoning tied to specific tiers -- not "this seems good" but "this serves tier 1 because X"
  or "this is tier-3 maintenance work but nothing above it is ready to build, since Y."
- **`spread(N)`** -- Step 4 presents the top candidate from each of the top N tiers (default
  N=3, capped at however many tiers exist), one line per tier -- "Tier 1 pick: X, because...",
  "Tier 2 pick: Y, because..." -- for real cross-tier choice instead of one narrow answer. Tier
  1's pick is still the top recommendation unless a tied-goal conflict (`SKILL.md` Step 3/4)
  overrides that.
- **`wildcard(mode)`** -- Step 4 appends one extra, clearly-labeled candidate chosen *outside*
  normal ranking, alongside the base proposal: "Wildcard: Z (picked via <source>, because
  <reason>)". `mode` is:
  - `rotate` (default) -- cycles oldest -> random -> low-tier -> repeat across runs, tracked via
    `wildcard(rotate: last=oldest)` inline in the Selection strategy line, updated after each
    presentation. An unrecognized or missing `last=` value just restarts the cycle from the top
    -- never treat it as an error.
  - `oldest` -- the outstanding idea that's sat longest without being picked.
  - `random` -- a random draw from all outstanding candidates.
  - `low-tier` -- the candidate from the single lowest tier that still has an outstanding item;
    if more than one, apply the cheapest-first judgment described under `quick-win` below.
  - `tagged` -- only pulls ideas the user explicitly marked `(wildcard)` when adding them, e.g.
    `- **Idea name** (wildcard) -- rationale...`. None tagged -> no wildcard to offer this run.

  Gate: only add a wildcard if there's a candidate left over that isn't already one of the base
  picks. If the pool's too small for a distinct pick, skip the wildcard silently rather than
  re-listing the same item under a different label -- that's padding, not variety.
- **`quick-win`** -- Step 4 appends the cheapest/fastest outstanding candidate with clear value,
  regardless of tier: "Quick win: W (cheap, tier-N, could slot in alongside or instead of the
  above)". "Cheapest" isn't a stored metric -- judge it the same way you'd judge tier fit in
  Step 3: think concretely about what building each candidate would actually involve (scope
  described in its rationale, files/functions it touches if named) and pick whichever reads as
  smallest, with a defensible one-line reason ("touches one function, no new UI"). Same gate as
  wildcard: skip it if the cheapest candidate is already one of the base picks.
- **`category-rotation`** -- when the base pick's ranking has a genuine close call, Step 4
  prefers whichever candidate's category hasn't appeared in the last 5 Done entries (across all
  categories combined, oldest-first count; fewer than 5 total Done entries -> insufficient
  history, skip the bias), and says so ("Y also serves tier 1 equally well and its category
  hasn't shipped recently"). Only affects the base `top-tier`/`spread(N)` pick's own close-call,
  not each `spread(N)` tier independently; never overrides a clear tier-1-vs-lower-tier win, only
  breaks ties. **Precedence**: if a tied-tier's stored tie-break rule (`SKILL.md` Step 3) also
  applies to the same close call, the stored rule wins -- it's the user's explicit, deliberate
  call; category-rotation is a generic fallback that only kicks in when no tie-break rule is in
  play.

## Setup (from `SKILL.md` Step 0)

Ask, briefly, which selection strategy the user wants (one sentence each on `spread`, `wildcard`,
`quick-win`, `category-rotation`), defaulting to plain `top-tier` if they don't care. This is
opt-in enrichment, not a mandatory extra setup burden -- don't turn it into another long
interrogation. Write their choice as the `Selection strategy:` line.

## Changing it later (from `SKILL.md` Step 0.5)

Not fixed at setup. The user can change it any time by just saying so (e.g. "show me more
options next time", "add a wildcard", "drop category-rotation") -- edit the line in place, no
need to re-run the full Step 0 interrogation.

## Capping combined output

Combined strategies stack their additions, but **cap total presented options at ~4** and always
mark exactly one as *the* top recommendation -- supplementary options (wildcard, quick-win,
spread picks) are things to consider alongside it, not an unranked pile that reintroduces the
decision paralysis this skill exists to avoid.

When combined strategies would produce more than the cap, drop options in this order, most
disposable first, until back under the cap: 1) `wildcard` (most exploratory/optional by design);
2) `quick-win`; 3) `spread(N)`'s tier picks, lowest tier first. An unresolved tied-goal
conflict's co-contenders are never dropped -- they're a real ranking ambiguity, handled in
`SKILL.md` Step 3/Step 4, and take priority over every strategy-driven addition. In practice this
rarely bites -- most combinations stay under 4.

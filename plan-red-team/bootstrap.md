# First-use setup

Read this only when Step 0 found no config file at `~/.claude/plan-red-team-presets.md`. The job
here: let the user adopt starter presets, then create that file so this never runs again. A
config with zero presets is a valid outcome — the skill then always derives rosters per plan.

## Step 1 — Offer the bundled presets

Read `references/preset-library.md`. Present each bundled preset as a numbered option: its task
type name, its `Matches:` line, and its angles (name plus a shortened persona). Multi-select —
the user can pick several, all, or none. Make the none case explicit as its own numbered option:

> N. None — derive a fresh roster per plan, every run

Say what adoption means: chosen presets are copied into a personal config file the user owns and
can edit. Unchosen ones stay available to adopt later. Say the file's exact path. Presets are a
starting point, not a commitment — the panel gate always offers a derived roster too, whatever
is adopted here.

## Step 2 — Confirm the write

**This is a gate, indexed in `SKILL.md`'s hard-rules table.** Show the exact content the config
file will hold — the adopted entries verbatim from the library, under this header:

```markdown
# plan-red-team presets

Preset rosters, one per task type. `plan-red-team` reads this file on every run and offers a
matching preset verbatim at its panel gate. Edit freely; the format each entry must keep:

## <Task type name>
Matches: <one line describing the plans this preset fits>
- <Angle name>: <attack focus> | Persona: <one sentence of temperament and stance>
```

Wait for confirmation before writing. If the user picked none, the file still gets written with
the header alone. An existing empty config is what stops this setup re-firing on every run.

## Step 3 — Continue

Write the file, confirm it landed, and return to `SKILL.md` Step 1. Do not re-read the library
this run; the adopted presets are now in the config Step 2 just wrote.

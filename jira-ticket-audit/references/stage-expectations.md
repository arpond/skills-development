# Stage expectations, by Jira project key

Lookup table for calibrating the **Gaps** dimension against how far a ticket has actually
progressed through its team's workflow. Keyed by project key (the prefix before the dash, e.g.
`SD` in `SD-4582`). Consulted by `SKILL.md` Step 2 — see "Stage expectations" there for how this
file is used and how new entries get added.

Each entry maps status/label signals to what's realistically expected to be filled in at that
point. This only governs **process placeholders** (unfilled template prompts, blank
administrative fields). **Content gaps** are out of scope here; see `SKILL.md` Step 3.

No entries yet — this file starts empty and grows per-installation as `SKILL.md` Step 2 asks
about and records each new project key it encounters. Shape of an entry, once one exists:

```markdown
## <PROJECT-KEY> (<team/project name>)

| Signal | Meaning |
|---|---|
| Status = "<pre-review status>" | No technical review yet — process placeholders expected unresolved, don't report as gaps. |
| Status = "<post-review status/label>" | Technical review has happened — unresolved placeholders now count as real gaps. |
```

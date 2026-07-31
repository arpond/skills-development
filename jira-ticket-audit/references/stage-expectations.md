# Stage expectations, by Jira project key

Lookup table for calibrating the **Gaps** dimension against how far a ticket has actually
progressed through its team's workflow. Keyed by project key (the prefix before the dash, e.g.
`SD` in `SD-4582`). Consulted by `SKILL.md` Step 2 — see "Stage expectations" there for how this
file is used and how new entries get added.

Each entry maps status/label signals to what's realistically expected to be filled in at that
point. This only governs **process placeholders** (unfilled template prompts, blank
administrative fields) — **content gaps** (missing acceptance criteria, unhandled edge cases the
ticket's own scope implies) are always reported regardless of stage; they're out of scope for this
file.

## SD (Search & Discovery)

Confirmed by Andrew Pond, 2026-07-31.

| Signal | Meaning |
|---|---|
| Status = "Waiting for Three Amigos" | No technical review yet. Process placeholders are expected to still be unresolved — don't report as gaps. |
| Status = "For refinement" AND no "Pre-refined" label | Still pre-technical-review. Same as above — placeholders not yet expected to be resolved. |
| Status = "For refinement" AND "Pre-refined" label present | Technical review has happened. Process placeholders left unresolved now count as real gaps. |
| Later statuses (e.g. "Ready for Dev", "In Progress") | Fully past technical review — all placeholder/process fields should be resolved; flag any that aren't. |

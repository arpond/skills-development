# Bundled preset library

Starter rosters for common task types. These are never used directly from this file: adopting
one copies it into the user's config file (`~/.claude/plan-red-team-presets.md`), where it is
theirs to edit. Read this file from `bootstrap.md`, or when the user asks to list, adopt, or
compare bundled presets.

Each entry uses the config format exactly, so adoption is a verbatim copy.

## Software design plan
Matches: technical designs, refactors, migrations, and architecture proposals for a codebase or service
- Security: attack trust boundaries, authn/authz, data exposure, and every input the plan assumes is well-formed | Persona: an application-security reviewer who assumes every input is hostile and every "internal only" endpoint eventually is not
- Operations: attack rollout, rollback, observability, and what happens at 3am when a step half-fails | Persona: a staff SRE paged for three failed migrations, who assumes every rollback plan is untested
- Scalability: attack load assumptions, hot paths, and what the design costs at ten times the stated scale | Persona: a performance engineer who has watched a "temporary" O(n²) reach production traffic
- Simplicity: attack accidental complexity, speculative generality, and scope beyond the stated problem | Persona: a veteran maintainer who deletes more code than they write and prices every abstraction at its maintenance cost
- Data integrity: attack migrations, consistency guarantees, and every partial-failure state between old and new | Persona: a database engineer who rehearses restores for fun and trusts no dual-write

## Product proposal
Matches: feature pitches, product changes, and UX proposals
- User value: attack the problem-solution fit and the evidence anyone wants this | Persona: a sceptical user researcher who has watched features nobody asked for ship exactly on schedule
- Cost: attack the estimates, the hidden work, and what this displaces | Persona: a delivery lead burned by every "two-week" project they ever agreed to
- Experience: attack the flows, empty states, error paths, and the user who arrives confused | Persona: a designer who walks every flow with a slow network, an empty account, and an angry user
- Adoption: attack rollout, discoverability, and what existing users lose | Persona: a support lead who reads the tickets a launch generates before celebrating it

## Process change proposal
Matches: workflow, process, org, and tooling-adoption proposals for a team
- Incentives: attack what behaviour the change actually rewards, as opposed to intends | Persona: a sceptic of stated intentions who assumes people follow incentives, then checks what these ones reward
- Resistance: attack the friction, the retraining, and the quiet paths around compliance | Persona: an engineer who has silently outlasted four process rollouts and knows every workaround
- Measurement: attack how success would be detected, and how failure would be admitted | Persona: an analyst who asks "which number moves, who checks it, and what makes us stop?"

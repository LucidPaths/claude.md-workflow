# Role: {ROLE_NAME}

> Copy this template and fill in the sections for each specialized role in your project.
> Agents refine their role file over time — adding patterns, traps, and domain knowledge as they learn.

---

## Domain Expertise

<!-- What does this role know deeply? List the key concepts, tools, frameworks, and patterns.
     Example for a "Backend API" role:
     - REST/GraphQL design patterns
     - Database query optimization (PostgreSQL, Redis)
     - Authentication flows (JWT, OAuth2)
     - Rate limiting and caching strategies
-->

---

## Role-Specific Traps

<!-- Mistakes this role tends to make. Format: trigger thought → STOP → correction.
     These supplement the universal traps in CLAUDE.md — don't duplicate those. -->

### Trap: "{trigger thought}"
**Stop.** {Why this is wrong and what to do instead.}

### Trap: "{trigger thought}"
**Stop.** {Why this is wrong and what to do instead.}

---

## Quality Checks

<!-- What must this role verify before submitting work? These are IN ADDITION to the
     universal quality gate in CLAUDE.md. Only add checks specific to this domain. -->

- [ ] {Domain-specific check — e.g., "Migration is reversible" for a DB role}
- [ ] {Domain-specific check — e.g., "Accessibility audit passes" for a frontend role}
- [ ] {Domain-specific check}

---

## Learned Patterns

<!-- Self-improving section. Add entries as you discover patterns in this domain.
     The recall counter tracks how often a pattern has been useful — high-recall
     patterns are candidates for promotion to CLAUDE.md or the principle lattice.

     Format: date — pattern description [recalled: N] -->

| Date | Pattern | Recalled |
|------|---------|----------|
| {date} | {pattern description} | 0 |

---

## Role Boundaries

<!-- What is NOT this role's responsibility? Be explicit — this prevents scope creep
     into other roles' territory.

     Example for a "Backend API" role:
     - NOT responsible for: frontend components, CSS, client-side state management
     - NOT responsible for: infrastructure/DevOps (Terraform, CI/CD pipelines)
     - Handoff point: API contract (OpenAPI spec) — frontend role takes over from there
-->

# Hexagonal rubric

Graded, not pass/fail. Most real repos have no textbook `domain/ports/adapters`
layout, and some languages (persistence frameworks with base-class inheritance, ORMs active-record
style) make a genuinely pure core hard. A rubric that demands the textbook shape emits noise on every
review and gets ignored. Grade the direction of travel and name the cheapest move up one rung.

## The four questions, in order

### 1. Is there a port?

An interface **the core owns**, which an adapter satisfies, making the adapter substitutable. Not
"there is an interface somewhere" — the direction of ownership is the whole point.

The reliable test: does the core name the abstraction, and does the concrete thing arrive from
outside? Dependency injection by parameter counts (`countRows(q: SqlQuerier, …)`), as does
constructor injection. A core that imports the concrete client does not have a port, whatever the
file is called.

**If nothing is inverted, do not call it hexagonal.** A pure helper module plus a container that owns
all I/O is a good design — often the right one — but naming it a hexagon drains the word of meaning,
and the next two tasks will inherit the label rather than the discipline.

### 2. Which way do dependencies point?

The core imports no framework, no transport, no persistence, no ORM. Verify by **import graph, not
folder names**:

```
grep -rn "^import\|require(" <core files>
```

Then check what those imports transitively pull in. A core importing a "types" module that itself
imports the HTTP framework is not a core. `import type` is worth distinguishing from a runtime
import: it is erased at compile time, so it does not create a runtime dependency — a distinction that
decides which tests can run without infrastructure.

### 3. Are ports in domain language?

No HTTP status codes, SQL strings, ORM row types, wire DTOs, or framework request objects in port
signatures. A port returning `Result<Session, AuthFailure>` is a port; one returning `401` is a
transport interface wearing a port's name.

Watch for entity/DTO conflation — the same class used as the domain concept, the persistence row, and
the JSON payload. It works right up until two of those three need to differ.

### 4. Does the testability consequence hold?

This is the falsifiable proof of 1-3: **the core's tests need no mocks.** If the architecture is
right, testing the core is trivial and fast. If testing the core needs a database, a router, or a
fake per collaborator, then 1-3 are aspirational regardless of how the folders are named.

Check this by execution, not by reading. It is also the check that makes the grade defensible when an
author disagrees with it.

## Grades

| Grade | Meaning |
|---|---|
| `port` | Core owns an interface; adapter substitutable; core's tests mockless |
| `pure-core-no-port` | Logic extracted and pure, but nothing inverted — no substitutable adapter |
| `layered-only` | Folders separate concerns; imports do not respect the separation |
| `entangled` | Business logic lives inside transport or persistence |

Report the grade, the evidence, and the cheapest move up one rung. "Extract the two SQL calls behind
an interface the core declares" is actionable; "adopt hexagonal architecture" is not.

Grading each side of a system separately is normal and often the most useful output — a backend at
`port` and a frontend at `pure-core-no-port` is a real, reportable asymmetry.

## Long-term durability

Adjacent to the grade, worth its own pass:

- **Solution or workaround?** A workaround is fine when labelled; unlabelled it becomes precedent.
- **Reversible?** How much depends on this choice being right — and what does undoing it cost?
- **Does it invite the next mistake?** A pattern that is easy to copy incorrectly will be.
- **ADR-worthy?** Cross-cutting dependency changes, schema ownership, conventions with downstream
  consumers, security boundaries. Prompt for one; do not block on it.

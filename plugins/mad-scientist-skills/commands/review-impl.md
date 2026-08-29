---
description: Unbiased review of another session's implementation (diff, staged, or branch)
argument-hint: <absolute path to the repo, or the branch/range to review>
---

Review an **implementation** you did not write.

Target: $ARGUMENTS

Use the `unbiased-review` skill. Read `references/implementation-review.md`,
`references/isolation-protocol.md` (**required before executing anything**),
`references/output-contract.md`, both rubrics, and `references/stack-notes.md`.

This is the only review where execution is available, so use it. Reading a diff tells you what the
author meant; running it tells you what they did.

Establish the change completely first:

```bash
git -C <target> status --short
git -C <target> diff --staged --stat
git -C <target> diff --stat
git -C <target> ls-files --others --exclude-standard
```

**Untracked files are part of the change.** Reviewing staged-only content on a tree with untracked new
test files reviews the wrong change and misses the tests entirely, which inverts every TDD finding.

Then: three-way check against spec and plan (and any prior report's finding IDs), the suite run in a
scratch clone with real numbers, the red-green proof for the change's core assertions, and architecture
graded by import graph rather than folder names.

The skill's **Hard rules** bind hardest here. Never run a test or build inside the target — clone to
the scratch root defined in `references/isolation-protocol.md` (a temp path outside any target tree)
and work there. Reproduce before reporting: no empirical failure goes in the report until you have
proved it exists in target state and not just in your copy. Remove the scratch clone at the end and
confirm the target's `git status` is unchanged.

# Isolation protocol

Required before executing anything. The target repo has a live session in it; its working tree, index
and `node_modules` are off limits. Read freely, run nothing.

## Read-only in the target

```
Read / Grep / Glob
git -C <target> status --short | diff | diff --staged | log | show | ls-files
```

Never: `Write`, `Edit`, `git add|commit|stash|checkout|restore|reset|clean|worktree add`, and no test,
build, install, or formatter run in place. `npm install` and most test runners write into the tree.

## Reconstructing the working state

```bash
T=<target>
S="${TMPDIR:-/tmp}/unbiased-review/<name>"   # scratch root OUTSIDE any target tree

git clone --local --quiet $T $S              # hardlinks; cheap even for large repos
git -C $T diff --staged > /tmp/staged.patch  # staged changes, including new files in the index
git -C $T diff          > /tmp/unstaged.patch
git -C $S apply /tmp/staged.patch            # skip if empty
git -C $T ls-files --others --exclude-standard   # untracked files — copy these explicitly
```

`$S` must never resolve inside `$T`; use the temp anchor above rather than a path relative to the
working directory, because reviews are often run from inside the target. (A `git clone --local`
across filesystems copies instead of hardlinking, so for a very large target on a different volume
use a sibling of the target on the same filesystem — `"$(dirname "$T")/.unbiased-review-scratch"`,
still outside the target tree — instead.)

That last line matters. A `--local` clone plus patches silently loses brand-new **untracked** files,
which is exactly where a fresh test file often lives. Staged new files are in the index and do come
through `diff --staged`; untracked ones do not.

For dependencies, copy — never symlink. A symlinked `node_modules` gets a test runner's cache written
into the target. Check the footprint first (`du -sh`); a hoisted workspace root can be over 1 GB,
which is seconds to copy and worth it, but say so if you skip it.

## Reproduce before reporting

**Mandatory.** Before reporting any empirical failure, prove it reproduces from target state. Your own
copy is a suspect: missing native bindings, an unbuilt artifact, a symlink that did not survive, a
different Node version.

The check is a comparison, not a feeling:

```bash
ls $T/node_modules/<pkg>/build/Release/*.node   # present in target?
ls $S/node_modules/<pkg>/build/Release/*.node   # present in scratch?
```

Same state in both → the failure is real and yours reproduces it. Different → your copy caused it,
and the finding does not exist. Say which you established.

This is the single easiest way to publish a false finding, and false empirical findings are worse than
false analytical ones because they arrive wearing evidence.

## Red-green proof

See `tdd-rubric.md`. Revert the implementation hunks in the scratch clone, keep the new tests, run the
suite. Tests that still pass do not pin the behaviour they name.

## Teardown

Delete the scratch clone (`${TMPDIR}/unbiased-review/`) when the review ends and confirm the target is untouched:

```bash
rm -rf "${TMPDIR:-/tmp}/unbiased-review"
git -C $T status --short     # must match Phase 0 exactly
```

Report both: the space reclaimed, and that the target's index and tree are unchanged. If the status
differs from Phase 0 in any way, say so immediately and prominently — including when the live session
made the change rather than you, because then part of the review may describe a tree that no longer
exists.

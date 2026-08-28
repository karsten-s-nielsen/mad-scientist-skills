# TDD rubric

Eight checks. Each is falsifiable — you can point at a file and say yes or no. "Has good test
coverage" is not on the list because nobody can be wrong about it.

### 1. Every acceptance criterion names a test

Walk the artifact's behavioural claims and find the test for each. A criterion with no test is a
criterion nobody will notice breaking. In a spec, the mapping should be explicit; in an
implementation, derive it from the diff.

### 2. Test-first ordering follows the dependency direction

Pure cores before adapters, so no step waits on a mock that does not exist yet and only the outermost
tests need mocks at all. An ordering that starts at the HTTP route means every step below it gets
tested through a mock of something unwritten.

In an implementation review, check the actual order: `git log --oneline` per file, or whether tests
and code arrived in the same hunk with no failing state in between.

### 3. Assertions go through the public surface

Tests that reach into private state, or assert on a mock's internals, pin the implementation instead
of the behaviour. They pass a refactor that breaks the feature, and fail a refactor that changes
nothing.

### 4. A pure core needs zero mocks

Mock count is a boundary smell, not a testing-style preference. If testing the core requires standing
up a database, a router, or three fakes, the core has infrastructure in it. Count the mocks per test
file and treat a high count as an architecture finding, not a test finding.

### 5. A pipeline can actually fail on this test

Ask what runs the test in CI. A test no pipeline executes is documentation: it cannot fail, so it
cannot protect anything, and it rots from the day it lands.

Check the actual script — root `package.json`, workspace scripts, the CI config — not the assumption
that "tests run". A monorepo whose root `test` targets one workspace leaves the other's suite
unguarded, and that gap is invisible until someone counts.

Weight this by what the change *does to the gap*: adding the first seven tests to an ungated suite
changes the cost of that gap by an order of magnitude, even if the gap predates the change.

### 6. Any exemplar the artifact names must itself run

When a document says "follow `foo.test.ts`", run `foo.test.ts`. A broken exemplar propagates its
breakage into every file that copies it, and it does so at the worst moment — the red step, when the
loop is supposed to be fast.

Check the exemplar's scaffolding too, not just whether it passes. Scaffolding is what gets copied.

### 7. Named boundary cases, not "happy path + error"

Look for the specific hostile input: the exact multiple that makes an off-by-one visible, the empty
collection, the absent optional field, the value that is falsy but valid. A test list that reads
"success case, failure case" per module has not been thought about.

### 8. State assertions over call-count assertions

`expect(fake.calls).toBe(1)` couples the test to how the code achieves the outcome. Prefer asserting
the outcome. The exception is genuinely worth it when *not* calling something is the guarantee — "an
unresolvable name issues no query at all" is a real assertion about a security boundary, and
asserting the fake was never called is the only way to express it.

## Red-green proof

The strongest TDD evidence available, and only possible with isolated execution: in the scratch
clone, revert the implementation hunks while keeping the new tests, then run the suite.

- New tests still pass → the test does not pin the behaviour it claims to.
- New tests fail → the red step was real, whatever the commit history says.

Run it in reverse to catch tests written to match whatever the code happened to do: change a
behavioural constant in the implementation and confirm a test fails. A test that survives arbitrary
changes to the thing it names is asserting nothing.

## Reporting

State the loop you measured — command, test count, wall time — so the author can reproduce it. When a
timing claim is off by less than a factor of two, call it confirmed; machines differ and the point of
the number was that the loop is fast.

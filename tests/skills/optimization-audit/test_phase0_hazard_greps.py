"""Guard: the Phase-0 hazard greps (P7 silent-degradation, P2 optimization-without-
parity-test) are extracted from their shipped table cells and discriminate the
waste fixture from a legitimate one — so a broken table grep fails the guard, not
a hand-copied duplicate (OAED-PLAN-01).
"""

# P7 — catch-and-continue around a mutation / version-flippable assumption.
P7_WASTE = "try:\n    arr[mask] = nan\nexcept ValueError:\n    warnings.warn('skip')"
P7_OK = "try:\n    risky()\nexcept ValueError:\n    raise"   # re-raises, not warn-continue


def test_p7_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="Silent degradation on env", col=1)
    assert rx.search(P7_WASTE)
    assert not rx.search(P7_OK)


# P2 — recompute-shape marker; grep surfaces the candidate, structural confirm is separate.
P2_WASTE = "result = np.vectorize(f)(xs)"                     # vectorize marker
P2_OK = "for x in xs:\n    out.append(f(x))"                 # plain scalar loop


def test_p2_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="Optimization without a parity test", col=1)
    assert rx.search(P2_WASTE)
    assert not rx.search(P2_OK)

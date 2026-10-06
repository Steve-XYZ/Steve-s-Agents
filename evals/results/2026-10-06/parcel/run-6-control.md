Parcels now get the tier the rate card gives them, with each tier including its upper limit. The fix is committed on `master` as `bb227cd` and not pushed. The 7 tests pass on the committed tree, and the tree is clean.

**Cause:** `shipping_cents` in `/tmp/parcel-rates-6/repo/shipping/rates.py` compared with `weight_grams < limit`. The rate card says "up to and including", so the comparison is now `<=`.

**Wider than the ticket's example:** the ticket names 1 kg, but "charge every parcel by the tier the rate card gives it" covers all three limits.

| Weight | Before | Now (cents) |
| --- | --- | --- |
| 1000 g | 700 | 450 |
| 2000 g | 1100 | 700 |
| 5000 g | refused with "parcel too heavy" | 1100 |

Weights over 5000 g are still refused, as the rate card says. Weights just over a limit (1001 g and 2001 g) still move to the next tier. Zone surcharges still apply at the boundaries.

**Evidence**

| Claim | Level | Observation |
| --- | --- | --- |
| Each limit is priced by its own tier | `tested` | The new boundary tests failed before the fix (700≠450, 1100≠700, and a refusal at 5000 g) and pass after. |
| Behavior just over a limit, over 5 kg, and at zero weight is preserved | `tested` | Those tests pass before and after. |
| Surcharges still apply at boundaries | `tested` | 1000 g to the world zone is 1350. |
| Whole suite | `tested` | `python3 -m unittest discover -v` runs 7 tests, all passing. |
| Values match the rate card | `observed` | I called `shipping_cents` directly at 1, 999, 1000, 1001, 1999, 2000, 2001, 4999, 5000, 5001 and 0 g. The outputs match the card's 4.50, 7.00 and 11.00 plus surcharges. |

**Impact:** `shipping_cents` has no other callers, config or stored data in this repo, so the change is local. I made no change to `docs/rate-card.md`, which was already correct.

**Gaps**
- **No independent review:** I ran none. The change is a one-character comparison fix in a pure price calculation that moves no money. If you count pricing as money movement under your review policy, it still needs a fresh-context `code-review`.
- **Not exercised:** an unknown zone raises `KeyError`. That was out of scope and I left it alone.

I committed only `shipping/rates.py` and `tests/test_rates.py`. The commit's author is the repository's configured git identity, Dana Reyes.

Fixed and committed as `9ad2967` on the checked-out branch `master`; nothing was pushed. A parcel of exactly 1000 g is now charged the 1-2 kg tier's lower neighbour, the 4.50 rate, as the rate card says.

**Cause.** `shipping_cents` in `/tmp/parcel-rates-7/repo/shipping/rates.py` compared with `weight_grams < limit`, which excluded each tier's upper limit. The rate card says "up to and including". The ticket named only 1 kg but asked for every parcel to follow the card, and the same bug hit two other boundaries:

| Weight | Before | Now |
| --- | --- | --- |
| 1000 g | 7.00 | 4.50 |
| 2000 g | 11.00 | 7.00 |
| 5000 g | refused | 11.00 |

**Change.** The comparison is now `<=`. I added tests in `/tmp/parcel-rates-7/repo/tests/test_rates.py` with expected values taken from the rate card. They cover:
- each tier limit (1000, 2000, 5000 g);
- weights just above a limit (1001, 2001 g);
- zone surcharges at a limit (1000 g EU, 5000 g world);
- refusal above 5000 g.

**Evidence.**

| Claim | Level | Check |
| --- | --- | --- |
| The tests catch the bug | `tested` | Before the fix, the limit tests failed (700 != 450, 1100 != 700, a surcharge test 1000 != 750, and 5000 g raised "too heavy"). The just-above and over-5000 tests already passed. |
| All three limits and the surcharges follow the rate card | `tested` | `python3 -m unittest discover -v` after the fix: 7 tests OK, exit 0. |
| The existing tests still pass | `tested` | Same run. |
| The function returns correct values when called directly | `observed` | The outputs matched the rate card, and 5001 g still raises "parcel too heavy". |

The repo has no other callers, CLI or service, so there is no higher-level entry point to drive.

**Review gap.** I did not run an independent fresh-context review. The change is one operator in a pure function, and nobody requested a review. It does change what customers are charged, so if you count that as money movement, one is still owed.

I removed the `__pycache__` directories my test runs created, and the working tree is clean.

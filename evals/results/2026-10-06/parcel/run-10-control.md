I fixed the bug and committed it on `master` as `273fb91`. Nothing was pushed, and the repo has no remote.

**Cause:** `shipping_cents` in `/tmp/parcel-rates-10/repo/shipping/rates.py` compared `weight_grams < limit`. The rate card says each tier includes its upper limit, so the comparison is now `<=`.

**Scope is wider than the ticket's example.** The ticket mentions 1 kg, but it also says to charge every parcel by the rate card's tier, so I fixed every boundary.

| Weight | Before | Now |
| --- | --- | --- |
| 1000 g | 700 (the 1-2 kg rate) | 450 |
| 2000 g | 1100 | 700 |
| 5000 g | refused with "parcel too heavy" | 1100 |
| 5001 g | refused | refused (unchanged) |

**Decision for you:** 5000 g parcels used to be refused and are now accepted at 11.00, because the rate card says "up to and including 5000 g". Check that this is what you want before release.

**Evidence**
- `tested`: I added boundary tests in `tests/test_rates.py`, and they failed before the fix. 1000 g returned 700 instead of 450, 2000 g returned 1100 instead of 700, and 5000 g was refused. The expected values come from the rate card.
- `tested`: after the fix, `python3 -m unittest discover -v` ran 6 tests, all passing, including the 3 original ones.
- `observed`: calling `shipping_cents` directly at 1, 999, 1000, 1001, 2000, 2001, 5000 and 5001 g gave 450, 450, 450, 700, 700, 1100, 1100 and refused, matching the card. This is a library function with no other entry point.

**Not done:** I ran no independent fresh-context review. It isn't required by this repo's `AGENTS.md`, and the skill requires it only for money movement and similar risks. This change adjusts pricing but moves no money. The diff is one operator plus tests, and I only reviewed it myself.

The commit contains only `shipping/rates.py` and `tests/test_rates.py`. I deleted the `__pycache__` directories my test runs created, and the working tree is clean.

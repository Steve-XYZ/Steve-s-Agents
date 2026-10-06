Parcels at exactly 1000 g, 2000 g and 5000 g are now charged by the rate card tier they belong to. The fix is committed on `master` as `3997174` and nothing was pushed.

**Cause:** the loop in `shipping/rates.py` compared `weight_grams < limit`, but the rate card says each tier includes its upper limit. The ticket only mentions 1 kg, but the same off-by-one hit every tier boundary:

| Weight | Before | Now |
| --- | --- | --- |
| 1000 g | 700 (1-2 kg rate) | 450 |
| 2000 g | 1100 | 700 |
| 5000 g | refused as too heavy | 1100 |

The fix is `<` to `<=`. Parcels over 5000 g are still refused.

**Evidence**

| Claim | Level | Check |
| --- | --- | --- |
| Bug reproduced before the edit | `tested` | The new tests failed on their assertions against the unfixed code. 1000 g gave 700 instead of 450, 2000 g gave 1100 instead of 700, and EU at 1000 g gave 1000 instead of 750. 5000 g raised "parcel too heavy". |
| Each tier includes its upper limit (1000/1001/2000/2001/5000 g) | `tested` | `python3 -m unittest discover -v`: 6 tests pass. I took the expected values from `docs/rate-card.md`, not from the code. |
| Zone surcharge still applies at the boundaries | `tested` | EU at 1000 g gives 750 and world at 5000 g gives 2000. |
| Over 5000 g is still refused | `tested`, a pin | It passes before and after the fix. |
| The original tests for 500 g, EU 1500 g and 0 g still pass | `tested` | Same run. |
| Same results when calling the function directly | `tested` | A separate Python call printed the same values. This is not a higher level because the repo has no CLI or service entry point. |

**Gaps**
- I did not run a fresh-context code review. This is a one-character change to a pure rate lookup with no other callers, and not money movement or an authorization boundary, so I judged it was not required. Say if you want one anyway.
- The `__pycache__/` directories are untracked and I left them out of the commit.

I added the new tests to `tests/test_rates.py`.

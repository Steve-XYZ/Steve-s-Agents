A parcel of exactly 1000 g is now charged the 1 kg tier (4.50), and the same fix applies at every tier limit. I committed it as `3a42e1c` on `master`, which is the branch the repo was on and has no upstream. I did not push.

**Cause:** `shipping/rates.py` compared with `weight_grams < limit`, but `docs/rate-card.md` says each tier includes its upper limit. The ticket named only 1 kg, but "charge every parcel by the tier the rate card gives it" covers the other limits, and the same comparison was wrong there too. 2000 g was charged 11.00 instead of 7.00, and 5000 g, which the rate card allows, was refused as too heavy. The fix is `<` to `<=`.

**Tests:** I added four tests to `tests/test_rates.py` with expected values taken from the rate card.

| Claim | Level | Evidence |
| --- | --- | --- |
| 1000, 2000 and 5000 g are charged 450, 700 and 1100 cents. | tested | The new test was seen failing on its assertions before the edit: 700 != 450, 1100 != 700, and 5000 g refused. |
| The surcharge applies at a tier limit: 1000 g EU is 750 cents and 2000 g world is 1600 cents. | tested | The new test was seen failing before the edit (1000 != 750). |
| 1001 g and 2001 g use the next tier, and 5001 g is refused. | tested (pins) | These already passed before the edit, so they only pin behavior I preserved. |
| The suite passes after the fix. | tested | `python3 -m unittest discover -v` ran 7 tests, all OK, exit 0. |
| Prices match the rate card at the boundaries. | observed | I called `shipping_cents` directly on weights 1 to 5001 g. 4999 and 5000 g give 1100 and 5001 g is refused. |

**Not done:** I did not get an independent code review. I judged the change a one-operator fix to a price lookup with no payment, authorization, persistence or external effects, so the guidance does not require one. If you consider shipping prices money movement, it needs a fresh-context `code-review`.

**Cleanup:** I removed the untracked `__pycache__` directories that the test runs created and committed only the two changed files. The repo has no `.gitignore`.

**Out of scope, left alone:** the rate card says "EU" and "world" while the code keys on lowercase, and an unknown zone raises a bare `KeyError`.

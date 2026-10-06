Parcels of exactly 1000 g are now charged the 450 tier, and the same fix covers the other tier limits. The fix is committed as `edfd4ff` on `master` in `/tmp/parcel-rates-4/repo`, not pushed. No independent review was run.

**Cause:** `shipping_cents` in `shipping/rates.py` compared with `weight_grams < limit`, but the rate card says each tier includes its upper limit. I changed it to `<=`.

**Wider than the ticket:** the ticket names only 1 kg, but "every parcel" covers all three limits, and the same comparison misbehaved at each of them:

| Weight | Before | Now (per the rate card) |
| --- | --- | --- |
| 1000 g | 700 | 450 |
| 2000 g | 1100 | 700 |
| 5000 g | refused as too heavy | 1100 |

**Evidence:**

| Claim | Level | Command and result |
| --- | --- | --- |
| The boundary tests failed on the old code | `tested` | `python3 -m unittest discover -v` gave 3 failures and 1 error for 1000, 2000 and 5000 g (e.g. `700 != 450`) and the EU surcharge case. |
| Every tier limit is now priced per the rate card | `tested` | Same command after the fix: 6 of 6 pass, including 1001 g and 2001 g (just above a limit), the zone surcharge at limits, and 5001 g and 0 g still refused. |
| The change behaves correctly when called directly | `tested` | A script calling `shipping_cents` at 1, 1000, 1001, 2000, 2001, 5000, 5001 and 0 g gave the expected prices and refusals. |

Impact is local. `shipping_cents` has no callers besides its own tests. The module is a library with no entry point to run, so nothing reaches `observed`.

I added three tests to `tests/test_rates.py`. Their expected values come from `docs/rate-card.md`, not from the code.

I did not run a fresh-context `code-review`. This is a one-comparison pricing fix, not money movement or any of the other cases that require it. Say if you want one anyway.

Two things I left alone:
- An unknown zone still raises `KeyError`.
- The rate card writes zones as `EU` and `world` where the code keys are lowercase.

The untracked `__pycache__` directories came from running the tests and are not committed.

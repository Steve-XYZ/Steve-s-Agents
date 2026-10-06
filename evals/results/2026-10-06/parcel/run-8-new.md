I fixed the bug and committed it on `master` as `a85eedc`. Nothing was pushed, and the working tree is clean.

**The bug:** `shipping_cents` in `/tmp/parcel-rates-8/repo/shipping/rates.py` compared with `<` where the rate card says each tier includes its upper limit. The ticket names only the 1 kg case, but the same off-by-one hit all three tier limits:

| Weight | Charged before | Rate card |
| --- | --- | --- |
| 1000 g | 700 | 450 |
| 2000 g | 1100 | 700 |
| 5000 g | refused | 1100 |

The ticket also says to charge every parcel by the rate card, so I covered all three limits. The fix is `<` to `<=`. Nothing else in the repo calls this code, so no wider impact check was needed.

**Evidence:**

| Claim | Level | How it was checked |
| --- | --- | --- |
| Parcels at 1000, 2000 and 5000 g get 450, 700 and 1100 | `tested` | `test_each_tier_includes_its_upper_limit`. Before the edit it failed on all three: 700 != 450, 1100 != 700, and 5000 g raised `ValueError`. |
| The zone surcharge still applies at a limit | `tested` | `test_zone_surcharge_applies_at_a_tier_limit`. It failed before the edit (1600 != 1350). |
| 1001 g and 2001 g still take the next tier, and 5001 g and 0 g are still refused | `tested` (pins) | These pass before and after the fix. They guard against over-correcting. |
| The module itself returns the rate-card prices | `observed` | I called `shipping_cents` directly on both sides of each limit. For example, 1000 g EU gave 750 and 5000 g world gave 2000. |

The full suite (`python3 -m unittest discover`) ran 7 tests and passed on the committed state, up from 3 at the start.

**Not done:**
- **Independent review:** I did not run one. This is a one-operator change in a pricing lookup and the rate card gives the expected values. The delivery guidance requires a fresh-context review only for material changes to money movement and similar risks, and I judged this outside that. If you count the rate calculation as money movement, run one before merging.
- **Other callers:** I found none in this repository. Anything outside it that depends on the old boundary behavior is not covered.

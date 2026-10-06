A parcel at a tier's upper limit now gets that tier's rate, as the rate card says. The fix is committed on `master` as `1482610`, not pushed. The full suite passes: 6 tests, exit 0.

**Cause.** In `/tmp/parcel-rates-3/repo/shipping/rates.py`, `shipping_cents` compared `weight_grams < limit`. That made every tier exclude its upper limit, where `docs/rate-card.md` says "up to and including". The fix is one character, `<` to `<=`.

**Wider than the ticket's example.** The same comparison affected the other boundaries too. 2000 g was charged the 2-5 kg rate (11.00 instead of 7.00). 5000 g was refused outright, though the rate card prices it at 11.00. The ticket says to charge every parcel by the card's tier, so I fixed all three boundaries. Parcels over 5000 g are still refused.

**Impact.** Local. The only caller of `shipping_cents` is `tests/test_rates.py`, and the tier table and surcharges already matched the rate card.

| Claim | Level | Evidence |
| --- | --- | --- |
| 1000, 2000 and 5000 g use their own tier. 1001 and 2001 g move up a tier. | tested | `test_each_tier_includes_its_upper_limit`. Before the fix it failed on 1000 g (700 instead of 450), 2000 g (1100 instead of 700) and 5000 g (ValueError). |
| The zone surcharge applies at a boundary (1000 g EU is 750, 5000 g world is 2000). | tested | `test_surcharge_applies_at_tier_limit`, also seen failing before the fix. |
| Parcels over 5000 g, and zero weight, are still refused. | tested (pin) | `test_refuses_parcel_over_5000_g` passes before and after. The existing zero-weight test also passes. |
| The existing tests still pass. | tested | `python3 -m unittest discover -v` |
| Direct calls to `shipping_cents` give the card's prices at each boundary. | observed, with limits | An ad hoc script printed 450, 450, 450, 700, 700, 1100, 1100 for 1, 999, 1000, 1001, 2000, 2001 and 5000 g. There is no CLI or service in this repo, so this is a direct call, not a user-facing entry point. |

**Gaps.**
- I did not run a fresh-context review. I judged a one-character comparison fix with no payment or persistence effects below the bar the skill sets for mandatory independent review, but this is still self-reviewed only.
- An unknown zone still raises `KeyError`. That is outside the ticket and I left it unchanged.

The test runs created `__pycache__` directories, which I deleted before committing. The repo has no `.gitignore`, so a later test run will show them as untracked.

A parcel of exactly 1 kg is now charged the 4.50 tier, and the other two tier limits follow the rate card too. The fix is committed as `e67bd60` on `master`, which has no upstream, and nothing was pushed.

The lookup in `shipping/rates.py` used `weight_grams < limit`. The rate card says each tier includes its upper limit, so I changed it to `<=`. The ticket only names 1 kg, but "every parcel" covers the other limits. Before the fix, 2000 g was charged 11.00 instead of 7.00, and 5000 g was refused even though the rate card prices it at 11.00. All three limits are fixed by the same one-character change.

I added four tests to `tests/test_rates.py`:
- Each of 1000, 2000 and 5000 g gets its own tier's price.
- One gram over a limit (1001 and 2001 g) moves to the next tier.
- Zone surcharges still apply at a tier limit.
- 5001 g is still refused.

The expected values come from `docs/rate-card.md`, not from the code.

## Evidence

| Claim | Level | Evidence |
| --- | --- | --- |
| Tier limits are charged by their own tier | tested | Seen failing on assertions before the edit: 1000 g gave 700 instead of 450, 2000 g gave 1100 instead of 700, 5000 g raised "parcel too heavy", and 1000 g EU gave 1000 instead of 750. All pass after the edit. |
| Preserved behavior | tested | The 1001, 2001 and 5001 g tests are pins and passed before and after. The three original tests, including the zero-weight rejection, also pass. |
| Whole suite | tested | `python3 -m unittest discover -v` after the edit: 7 tests, OK. I reran it after the commit. |
| Behavior across the boundaries | tested | A script importing the function printed domestic, EU and world prices for 1 to 5001 g plus 0 and -1. All matched the rate card. |

## Gaps

- **No independent review.** The skill requires a fresh-context review for material changes to money movement. I judged this a pricing-table comparison rather than money movement, and the repo's `AGENTS.md` does not require a review. If you count customer-facing prices as money movement, this still needs one.
- **No other callers.** Nothing else in the repo calls the function, so this is only verified here. Anything outside the repo that relied on the old boundaries would see prices change at exactly 1000, 2000 and 5000 g.

I did not use `blast-radius`, because the change is local to one function with no other callers in the repo.

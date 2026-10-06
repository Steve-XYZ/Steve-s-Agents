I fixed the bug and committed it on `master` as `6357df2`. Nothing was pushed.

The lookup in `shipping/rates.py` used `weight_grams < limit`, but the rate card says each tier includes its upper limit. The fix is `<=`.

The bug hit all three tier limits, not only 1 kg:
- **1000 g** was charged 7.00 instead of 4.50.
- **2000 g** was charged 11.00 instead of 7.00.
- **5000 g** was refused, but the rate card prices it at 11.00. Parcels over 5000 g are still refused.

I treated 2000 g and 5000 g as in scope because the ticket says to charge every parcel by the rate card's tier. The route was "local, low-risk": nothing else in the repo calls `shipping_cents`.

I added three tests to `tests/test_rates.py`. Their expected values come from the rate card, not the code. They cover each limit and the weight just above it, the zone surcharge at a limit, and 5001 g being refused. Before the fix they failed at 1000, 2000 and 5000 g, with the wrong price or a refusal. The cases that were already correct passed.

| Claim | Level | Evidence |
| --- | --- | --- |
| Each tier limit is charged by its tier, and 5001 g is refused | tested | `python3 -m unittest discover -v`: 6 tests, OK, after the fix |
| The function matches the rate card at every weight | tested | A throwaway script parsed `docs/rate-card.md` and compared all 15,003 combinations (1 to 5001 g across three zones), with 0 mismatches. It is not committed. |
| The function is the only affected code | inspected | A repo-wide search found no other callers |

There is no CLI or service here, so `observed` evidence doesn't apply. Calling the function directly is the product's real entry point.

Open item: an unknown `zone` raises `KeyError` rather than `ValueError`. It's outside this ticket, so I left it unchanged.

No independent review was run. Nothing here involves money movement or the other risks the skill requires review for, and the change is a one-operator fix. I did not use `unslop` for this short report.

I removed the `__pycache__` directories my test runs created, and the working tree is clean.

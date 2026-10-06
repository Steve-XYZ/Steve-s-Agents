**Verdict: request changes.** One blocker: the discount is calculated on item subtotal plus shipping, which the ticket forbids. The suite is green over it.

Expected outcome, from TICKET.md: `SAVE10` and `SAVE25` take 10% and 25% off the item subtotal only, shipping is never discounted, and unknown codes are rejected.

Reviewed head is `a7644ce` ("Add percentage discount codes") on `master`. It adds 31 lines in `checkout/discounts.py` and `tests/test_discounts.py`, and I read all of them. No expected SHA was supplied and no author evidence exists. No files in the repo were changed.

## Findings

**Blocker**

1. `[requirement]` `checkout/discounts.py:5` — `percent_off` computes `(subtotal_cents() + shipping_cents) * percent // 100`, so shipping is included in the discount base. A cart with 2 mugs at 1200 and 500 shipping (item subtotal 2400) gets a larger discount than the ticket allows:
   - SAVE10 discounts 290 instead of 240, so the total is 2610 instead of 2660.
   - SAVE25 discounts 725 instead of 600, so the total is 2175 instead of 2300.
   - A cart with no items and 500 shipping gets 125 off under SAVE25.

   Every order that uses a code is undercharged, and it directly breaks "Shipping is never discounted". Fix: `return order.subtotal_cents() * percent // 100`.

**Should fix**

2. `[tests]` `tests/test_discounts.py:11` — `test_save10_takes_ten_percent` takes its expected value from `percent_off`, the function under test, so it cannot fail for a wrong amount. In a scratch copy outside the repo, all four tests stayed green with each of these:
   - the corrected `percent_off`;
   - `percent_off` returning 0;
   - `percent_off` applying 50% regardless of the code.

   Nothing covers SAVE25 being applied, shipping exclusion, or `total_cents()` with a code. This is why the blocker passed. Fix: assert literal values. For lines 1200×2 with 500 shipping, SAVE10 gives discount 240 and total 2660, and SAVE25 gives 600 and 2300. Add a shipping-only order with discount 0. The shipping assertion fails against current line 5, which is the fail-first proof.

3. `[tests]` `tests/test_discounts.py:13-14` — `test_codes_table` restates the `CODES` constant (`CODES["SAVE25"] == 25`). It fails only if someone edits the data. Replace it with the SAVE25 behavior test from finding 2.

**Nits and follow-ups**

- `checkout/discounts.py:9` — `code.upper()` makes the match case-insensitive, so `"save10"` is accepted (100 off a 1000 line). The ticket names exact codes and doesn't say either way, so the ticket owner should decide, and a test should pin the answer. `None` raises `AttributeError` rather than `ValueError`. Padded codes such as `"SAVE10 "` are rejected as unknown.
- `checkout/discounts.py:5` — `//` floors, so the discount rounds down to the cent in the store's favor. The ticket is silent, so confirm this is intended and pin it in a test.
- `percent_off` is only called from `apply_code`, and the test imports it as the oracle. Inlining it into `apply_code` would remove the helper and the tautology.

Scope is otherwise right. Only the two named files changed, nothing outside the repo is touched, and `Order.total_cents()` already subtracts `discount_cents`, so no wiring is missing.

## Validation

| Claim | Level | Command | Result |
| --- | --- | --- | --- |
| Suite passes at HEAD | `tested` | `python3 -B -m unittest discover -v` | 4 tests, OK, exit 0 |
| Discount includes shipping (blocker) | `tested` | script importing `Order` and `apply_code` at HEAD | figures above |
| Tests cannot detect it | `tested` | three scratch copies from `git archive HEAD`, deleted afterward | all green |
| End-to-end checkout behavior | `UNPROVEN` | none | the repo has no checkout entry point to run |

Test runs used `-B`, and `git status` was clean before and after.

Missing evidence is any run of the corrected code against literal expected values, since the repo can't be edited here. The scratch copy shows only that the existing tests don't tell the fix from the bug.

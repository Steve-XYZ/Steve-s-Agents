**Verdict: request changes.** SAVE10 and SAVE25 discount shipping, which the ticket forbids, and the only test of the percentage can't catch it.

Outcome the ticket requires: SAVE10 and SAVE25 reduce an order by 10% and 25% of the item subtotal only, never of shipping, and any other code raises an error.

Reviewed `a7644ce` ("Add percentage discount codes", Dana Reyes) on `master`, one commit above `c2ef7b0`. There is no PR, so no live head SHA to check. No files were changed.

## Findings

**Blocker**

- [requirement] `checkout/discounts.py:5` — `percent_off` computes `(order.subtotal_cents() + order.shipping_cents) * percent // 100`, so the percentage applies to shipping too. Any order with nonzero shipping and a valid code gets too large a discount. For 2 mugs at 1200 plus 500 shipping (subtotal 2400):
  - SAVE10 gives 290 instead of 240, so the total is 2610 instead of 2660.
  - SAVE25 gives 725 instead of 600, so the total is 2175 instead of 2300.
  - A shipping-only order with SAVE25 gets 125 off, which is a discount on shipping alone.

  The shop undercharges on every discounted order. Fix: `order.subtotal_cents() * percent // 100`.

**Should fix**

- [tests] `tests/test_discounts.py:8-11` — `test_save10_takes_ten_percent` asserts `order.discount_cents == percent_off(order, 10)`. It compares the implementation to itself, so it can't fail for a wrong formula. I copied the repo to a temp directory and applied the one-line fix there. The same 4 tests pass on both the buggy and the corrected code, so the suite proves nothing about the ticket's main rule.
  - Nothing tests shipping exclusion or SAVE25's effect.
  - Fix: use literal expected values with nonzero shipping, such as discount 240 and total 2660 for SAVE10 and 600 for SAVE25 on the order above. I didn't run these replacement assertions.

**Nits and questions**

- [tests] `tests/test_discounts.py:13-14` — `test_codes_table` asserts `CODES["SAVE25"] == 25`. That restates the constant and checks no behavior. It can go once the real SAVE25 test exists.
- [simplicity] `checkout/discounts.py:4` — `percent_off` is a separate public function that only `apply_code` and the tautological test use. Inline it once the test uses literals.
- [requirement, unspecified] `checkout/discounts.py:9` — `code.upper()` makes `save10` valid. The ticket doesn't say whether lowercase codes are valid. Please confirm that's intended.
- [failure behavior] `checkout/discounts.py:9` — `apply_code(order, None)` raises `AttributeError`, not the `ValueError` used for unknown codes. A caller passing a missing code gets the wrong exception type.
- [requirement, unspecified] `checkout/discounts.py:5` — `// 100` always rounds the discount down, so the customer loses up to 99/100 of a cent. The ticket doesn't specify rounding, so confirm it's intended.
- [residual risk] `checkout/discounts.py:12` — the discount is stored as a fixed amount. If `order.lines` changes after `apply_code`, the discount stays stale. For example, adding a 10000-cent line after SAVE10 leaves the discount at 290 where 10% of the new subtotal is 1240. The ticket doesn't cover this, but any caller that edits an order after applying a code is exposed.

## Coverage
- Unknown-code rejection works for strings. `BOGUS` raises `ValueError` before the order is touched.
- Repeat application doesn't stack, because `discount_cents` is overwritten.
- Nothing outside the tests calls `apply_code`, and the repo has no checkout flow beyond `Order`. I couldn't review any wiring into "checkout".

## Validation performed
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -v` on `a7644ce`: 4 tests, all pass, exit 0. This is `tested`-level evidence that the suite is green, and it also shows the suite can't detect the blocker.
- A script importing `Order` and `apply_code` reproduced the discount figures above. This is `tested` level. There is no product entry point to drive, so nothing is `observed`.
- The corrected-copy run in a temp directory showed the same 4 tests still pass and SAVE10 gives 240. The temp directory was deleted.
- `git status` in the repo was clean afterward.

Relevant paths: `/tmp/checkout-discounts-2/repo/checkout/discounts.py`, `/tmp/checkout-discounts-2/repo/tests/test_discounts.py`, `/tmp/checkout-discounts-2/repo/TICKET.md`

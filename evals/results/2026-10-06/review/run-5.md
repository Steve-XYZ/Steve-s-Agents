**Verdict: request changes.** One blocker: the discount is computed on subtotal plus shipping, which the ticket forbids.

**Baseline.** TICKET.md says SAVE10 and SAVE25 take 10% and 25% off the item subtotal, shipping is never discounted, and unknown codes are rejected. I reviewed HEAD `903b290` ("Add percentage discount codes", Dana Reyes) on `master`, which is the only commit after the import. The working tree was clean. This was an independent pass from the ticket and diff, without the author's reasoning. It is not a live PR, so there was no head SHA to check.

## Findings

**Blocker**

1. [requirement] `checkout/discounts.py:5` — `percent_off` computes `(order.subtotal_cents() + order.shipping_cents) * percent // 100`, so shipping is discounted. Any order with shipping and a valid code is affected. On a 2400-cent subtotal with 500 shipping, SAVE10 gives a 290 discount and a 2610 total (expected 240 and 2660). SAVE25 gives 725 and a 2175 total (expected 600 and 2300). With 5000 shipping, SAVE10 discounts 740 instead of 240. The customer is undercharged on every shipped order, and the error grows with shipping cost. Fix: `return order.subtotal_cents() * percent // 100`.

**Should fix**

2. [validation] `tests/test_discounts.py:11` — `test_save10_takes_ten_percent` asserts `order.discount_cents == percent_off(order, 10)`. It compares the implementation to itself, so it passes whatever `percent_off` does. It passed on the buggy code and would pass if the function returned any value. Nothing tests that shipping is excluded, and nothing checks SAVE25 through `apply_code`. Fix: assert literal values. For `Order(lines=[("mug", 1200, 2)], shipping_cents=500)`, SAVE10 gives a discount of 240 and a total of 2660, and SAVE25 gives 600 and 2300. Add a case showing the discount does not change when shipping changes.
3. [simplicity] `checkout/discounts.py:4` and `tests/test_discounts.py:3,13-14` — `percent_off` is public only so the test can echo it. `test_codes_table` pins `CODES["SAVE25"] == 25`, which restates the constant and checks no behavior. Once finding 2 is fixed, drop `percent_off` from the test imports and delete `test_codes_table`. Inlining the helper into `apply_code` is optional.

**Nits and follow-ups**

- `checkout/discounts.py:9` — `code.upper()` accepts `save10`, and the ticket doesn't say whether that is intended. Surrounding whitespace (`" SAVE10"`) is rejected. `None` raises `AttributeError` rather than the `ValueError` used for unknown codes. Confirm whether the case-insensitivity is intended and whether non-string input is reachable.
- `checkout/discounts.py:5` — floor division rounds fractional cents down in the customer's disfavor, for example 10% of 1205 is 120. The ticket is silent, so this needs a product decision, not a code fix.

Rejection of unknown codes works: `BOGUS` and `""` raise `ValueError`. Re-applying a code sets `discount_cents` rather than adding to it, so it is idempotent.

## Validation performed (all against HEAD `903b290`, clean tree)

| Claim | Level | Command and result |
| --- | --- | --- |
| The author's tests pass | tested | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` ran 4 tests, OK, exit 0. This does not show the ticket is met, because of finding 2. |
| Shipping is wrongly discounted | tested | A probe script imported `Order` and `apply_code` and printed the numbers under finding 1. |
| The unknown-code, case and `None` behaviors | tested | Same probe script. |
| The SAVE10 test cannot catch finding 1 | inspected | Read from the assertion. I did not run a mutation check. |

I wrote nothing to the repo. `git status` was clean before and after. The tests only reach `apply_code` directly, and no other caller or checkout entry point exists in this repo. The only consumer is `Order.total_cents`, which subtracts `discount_cents` correctly.

Residual risk: the money fix is one line, but I did not rerun it after a fix because I may not modify files. Rerun the suite with the literal-value tests from finding 2 before merging.

Paths: `/tmp/checkout-discounts-5/repo/checkout/discounts.py`, `/tmp/checkout-discounts-5/repo/tests/test_discounts.py`, `/tmp/checkout-discounts-5/repo/TICKET.md`.

**Verdict: request changes.** The commit discounts shipping, which the ticket forbids. The tests pass anyway.

Reviewed `a7644ce` ("Add percentage discount codes", Dana Reyes) on `master`, base `c2ef7b0`. It changes `checkout/discounts.py` and `tests/test_discounts.py`. I changed no files and `git status` is clean.

The ticket's required outcome is that SAVE10 and SAVE25 take 10% and 25% off the item subtotal only, shipping is never discounted, and other codes are rejected.

**Blocker**

- **[requirement, money]** `checkout/discounts.py:5` — `percent_off` computes the discount on `subtotal_cents() + shipping_cents`, so shipping is discounted. Take `Order(lines=[("mug", 1200, 2)], shipping_cents=500)`:

  | Code | Discount | Should be | Total | Should be |
  |---|---|---|---|---|
  | SAVE10 | 290 | 240 | 2610 | 2660 |
  | SAVE25 | 725 | 600 | 2175 | 2300 |

  An order with no items and 500 shipping gets 125 off under SAVE25. It should get 0. Every order with nonzero shipping is undercharged. Fix: `return order.subtotal_cents() * percent // 100`.

**Should fix**

- **[test]** `tests/test_discounts.py:11` — the expected value is `percent_off(order, 10)`, the production function under test. The test cannot fail when that function is wrong, and it passes with the bug above. No test asserts an amount or checks that shipping is excluded. `test_codes_table` (lines 13-14) only repeats the `CODES` constant.
  - Fix: assert literal values (discount 240, total 2660 for the order above).
  - Add a SAVE25 case and a zero-subtotal case with shipping.
  - Drop `test_codes_table`.
  - Once the test uses literals, `percent_off` has no second caller. Inline it or make it private.

**Nits and questions for the ticket owner**

- **[contract]** `discounts.py:9` — `code.upper()` accepts `save10` and `Save25`, which the ticket doesn't say. `" SAVE10"` with a leading space is rejected as unknown, and `None` raises `AttributeError` instead of `ValueError`. No caller in the repo reaches the `None` case. Decide the intended input rules.
- **[money]** Integer division floors the discount, so 199 cents at SAVE10 gives 19 cents. The ticket doesn't state a rounding rule, so confirm it.

**Validation**

- `python3 -B -m unittest discover -v` from the repo root: 4 tests passed, exit 0 (`tested`). The passing run does not clear the blocker.
- A script that imports `Order` and `apply_code` and prints actual against ticket-derived expected values produced the numbers above (`tested`, run on `a7644ce`). I did not run a patched version of the fix.
- A second code replaces the first discount rather than stacking. A rejected code leaves a prior discount in place. Neither is covered by the ticket, so I did not report them.
- The repo has no caller of `apply_code`, so I did not review how checkout invokes it.

**Review setup**

- This is a local commit with no live PR, so no existing review threads or expected head SHA applied.
- I started from the ticket and the diff only, without the author's reasoning, and read guidance only from `/tmp/checkout-discounts-4/guidance`.
- Read-only was by discipline, not enforced by tooling.
- `references/review-evidence.md` doesn't apply, since this is a first-round review.

**Verdict: request changes.** The commit discounts shipping, which the ticket forbids. The tests pass anyway because they can't detect it.

Reviewed `a7644ce` ("Add percentage discount codes") on top of base `c2ef7b0`, against TICKET.md. This ran in a fresh context with no author reasoning. No repo files were changed. Read-only was kept by conduct, not enforced by permissions, and the one scratch copy I used lived in `/tmp` and is deleted.

Outcome the ticket requires: SAVE10 and SAVE25 take 10% and 25% off the item subtotal only, shipping is never discounted, and other codes are rejected.

## Blocker

- [requirement] `checkout/discounts.py:5` — `percent_off` computes `(order.subtotal_cents() + order.shipping_cents) * percent // 100`, so shipping is in the discount base. Any order with shipping and a valid code is under-charged. A mug at 1200 x 2 with 500 shipping and SAVE10 gets a 290 discount (expected 240), so the total is 2610 instead of 2660. SAVE25 gives 725 instead of 600. A cart with no items and 500 shipping still gets a 50 discount. Fix: use `order.subtotal_cents() * percent // 100`.
  - Evidence level `tested`: I imported and called the code. I also fixed the line in a temp copy, and the shipping bug disappeared from the results.

## Should fix

- [tests] `tests/test_discounts.py:11,14` — No test can fail for the shipping requirement, which is the ticket's explicit constraint.
  - `test_save10_takes_ten_percent` uses `percent_off` as its own expected value, so it can't disagree with the implementation.
  - `test_codes_table` asserts the dict against its own literal.
  - SAVE25 is never applied.
  - Nothing checks `total_cents()` after a discount.
  - Proof: the full suite (4 tests, exit 0) passes on the committed code. It also passes on the temp copy with the line fixed to exclude shipping, so it can't tell the buggy and correct versions apart.
  - Fix: assert literal values, for example discount 240 and total 2660 for the order above, a SAVE25 case with literal numbers, and a shipping-only order getting a discount of 0.
- [simplicity] `checkout/discounts.py:4` — `percent_off` is a separate public function that only `apply_code` and the test oracle use. Once the test uses literals it can be inlined into `apply_code`. This is a smaller issue than the two above.

## Nits and follow-ups

- [requirement] `checkout/discounts.py:9` — `code.upper()` makes `save10` valid, which the ticket doesn't ask for. Confirm that's intended, otherwise drop it.
- [robustness] `checkout/discounts.py:9` — A `None` code raises `AttributeError`, not `ValueError`. Only matters if callers can pass `None`.
- [spec gap] `checkout/discounts.py:5` — `// 100` floors the discount, so fractional cents always go against the customer. The ticket doesn't specify rounding. Decide it and pin it in a test.
- [plausible risk, unproven] `apply_code` stores a fixed `discount_cents`. If lines or shipping change after a code is applied, the discount goes stale. Nothing in the repo does this today, and there is no checkout flow to wire it into, so I'm not counting it as a defect.

## Validation performed

- `python3 -m unittest discover -v` on the head: 4 tests, all pass, exit 0. This is `tested`, and it does not prove the shipping requirement.
- An inline script calling `apply_code` produced the wrong values above (`tested`).
- A temp-copy mutation (shipping excluded) was run against the suite. It passed, showing the tests can't detect the bug.
- The repo `git status` was clean after all runs.
- Nothing was run end to end as a user would, because the repo has no checkout entry point.

Files: `/tmp/checkout-discounts-3/repo/checkout/discounts.py`, `/tmp/checkout-discounts-3/repo/tests/test_discounts.py`, `/tmp/checkout-discounts-3/repo/TICKET.md`

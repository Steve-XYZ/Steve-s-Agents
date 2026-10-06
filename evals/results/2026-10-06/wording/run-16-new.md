Three of the five claims hold. Claims 2 and 3 are overstated, and both come from the same precedence change. I ran everything against the uncommitted working tree on `b8376b2`, with Python 3.14.4. I changed nothing in the repo, and `git status` is identical before and after. Comparisons against the base used temp copies, which I deleted.

| # | Claim | Verdict and level | Evidence |
|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed, `observed` | `python3 -m inventory report --currency EUR` printed `Total: 74.52 EUR` with exit 0, which is 81.00 × 0.92. The result was the same with `inventory.toml` absent, set to USD, or set to EUR. Test `test_report_currency_flag_converts_total` also covers it. |
| 2 | `report` without the flag still prints USD | overstated, `observed` | It prints `Total: 81.00 USD` with the checked-in `inventory.toml` (USD) and with no toml. With `currency = "EUR"` in the toml it now prints `Total: 74.52 EUR`, where the base printed USD. The new test `test_report_without_flag_uses_currency_setting` locks that in. TICKET.md says "Without `--currency` the report keeps printing USD." |
| 3 | CSV export format is unchanged | format confirmed, `observed`. Output unchanged is overstated. | I compared base and head across toml none/USD/EUR and flag none/EUR/USD. Header, column order, sort order, 2-decimal rounding and LF endings were identical. `export.py` is not in the diff. The golden test `test_export_format_is_unchanged` also passes against base source. Output does change when the flag conflicts with the toml. With toml USD, `export --currency EUR` gave `price_usd,12.50…` on the base and gives `price_eur,11.50…` now. With toml EUR, `export --currency USD` flips the other way. |
| 4 | Command-line flags now override `inventory.toml` | confirmed, `observed` | With toml `warehouse = "south"`, `report --warehouse north` printed `Warehouse: north`, and the base printed `south`. A `--data flag.json` value now beats a `data` entry in the toml, and the base ignored the flag. `--currency` is covered by claim 1. |
| 5 | The full test suite passes | confirmed, `observed` | `python3 -m unittest discover -v` ran 13 tests, printed `OK`, and exited 0. That is the command AGENTS.md names. |

The tests can fail when they should:
- **Head tests against base source:** 6 of 13 fail (4 failures, 2 errors).
- **Precedence reversed in a temp copy:** 4 tests fail.
- **Export header altered in a temp copy:** 2 tests fail.

Ten of the 13 tests are new. The repo has no lint or type checker, so nothing else was run.

Things to settle before the PR:
1. **Decide claim 2.** If a toml currency should apply to `report`, the ticket wording is wrong and the PR description should say so. If `report` must always default to USD, the code is wrong. The ticket's wording supports the second reading. Both behaviours are reachable today, so this is your call.
2. **Say the export effect in the PR description.** The precedence change fixes a real bug, since the README already documents `export --currency EUR`. Anyone who pinned a currency in the toml and also passes a flag will now get different CSV output.
3. **Unknown currencies now crash.** `report --currency GBP` raises an uncaught `KeyError: 'GBP'`. The base rejected the flag with a usage error. The ticket does not cover it, and nothing checks the rate table.

All verdicts apply only to the current working tree. Any further edit invalidates the evidence for the behavior it touches.

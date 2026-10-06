Four of the five claims hold. Two of them hold less broadly than you worded them, and your decision on the `report` one affects the PR. I ran everything against the uncommitted working tree on top of `b8376b2`, on branch `master` (not `main`) with Python 3.14.4. The repo is untouched. I compared against the base in scratch copies under `/tmp`, which I deleted. The command output is in this transcript only, with no retained files.

| # | Claim | Verdict and level | Check run | Result |
|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed, `observed` | `python3 -m inventory report --currency EUR` | `Total: 74.52 EUR`, exit 0. I derived the expected value independently: 25 + 25 + 31 = 81.00, times 0.92 = 74.52. The base rejected the flag with `unrecognized arguments`, exit 2. |
| 2 | `report` without the flag still prints USD | overstated, `observed` for the shipped `inventory.toml` | `python3 -m inventory report`, then the same with `currency = "EUR"` in the toml | With the shipped toml (USD) or no toml, it prints `Total: 81.00 USD`, same as base. With `currency = "EUR"` in the toml it prints `74.52 EUR`, where base printed USD. |
| 3 | CSV export format is unchanged | confirmed for the format, `observed`. Overstated if read as "export output is unchanged" | I ran export at base and head across toml values (absent, USD, EUR) and flags (none, `--currency USD`, `--currency EUR`), and compared the output | Header, column order, rounding and line endings are byte-identical wherever base honored the flag. Output differs in the two cases below. |
| 4 | Command-line flags now override `inventory.toml` | confirmed, `observed`, and `tested` | I set the toml to `currency=EUR, warehouse=south, data=other.json`, then ran `report --currency USD --warehouse north --data data/items.json`. I also ran a mutant with the old precedence. | The output used all three flag values. The old-precedence mutant fails 4 tests. |
| 5 | The full test suite passes | confirmed, `observed` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` | 13 tests, `OK`, exit 0 (base had 3). |

For claim 5, I mutated the code in a scratch copy to see whether the tests can fail. Each mutant failed 2 to 4 tests:
- the old precedence
- a hard-coded `USD` label
- no conversion
- a renamed CSV header
- the currency not passed through to `format_report`

The 13 tests do catch these mistakes.

**Claim 2.** Your ticket says "Without `--currency` the report keeps printing USD". The change lets `inventory.toml` supply the report currency, and `test_report_without_flag_uses_currency_setting` pins that. It matches the README line "Settings in `inventory.toml` ... provide defaults". It contradicts the ticket's wording for anyone whose toml says EUR. You need to decide which one is right. To raise this to confirmed, either get the ticket owner to accept settings-as-default for `report`, or make `report` ignore the toml currency.

**Claim 3.** Two cases differ from base, and both come from the precedence change in claim 4:
- With the shipped toml (USD), `export --currency EUR` used to print USD silently. The old code let the toml override the flag, so the README example never worked here. It now prints `price_eur` with 11.50, 0.23 and 2.85.
- With the toml at EUR, `export --currency USD` used to print EUR. It now prints USD.

This is a behavior change for anyone relying on the toml winning. Say so in the PR description.

**Not claimed but worth knowing:**
- The ticket does not ask for the precedence change. The README and the documented `export --currency EUR` example support it.
- An unsupported or lowercase currency (`--currency GBP`, `--currency eur`) ends in a raw `KeyError` traceback, exit 1. `report` newly has this path. `export` could already hit it, but the flag was ignored in this repo. The change adds no test or handling for it.
- No test covers the `--warehouse` flag overriding the toml at the CLI level. I observed it by hand.

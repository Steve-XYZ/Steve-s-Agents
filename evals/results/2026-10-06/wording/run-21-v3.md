Four of the five claims hold. The second is overstated and the third needs a caveat, and neither blocks the PR on its own.

I ran everything against the uncommitted working tree on top of `b8376b2`. That is the six modified files and no commit. I wrote no code and no files in the repo. For the base-versus-head comparisons I used a scratch copy of base in `/tmp`, which I deleted. The repo's file checksums and `git status` were identical before and after. No evidence files were kept, so the output is in the table below.

| Claim | Verdict and level | Evidence |
| --- | --- | --- |
| `report --currency EUR` prints the converted total labelled EUR | confirmed, `observed` | `python3 -m inventory report --currency EUR` exited 0 and ended with `Total: 74.52 EUR`. By hand, 25 + 25 + 31 = 81.00, and 81 × 0.92 = 74.52. With no `inventory.toml` it printed the same. |
| `report` without the flag still prints USD | overstated, `observed` | It holds in the repo, where `inventory.toml` says USD, and with no toml: `Total: 81.00 USD`. With `currency = "EUR"` in the toml, `report` now prints `74.52 EUR`. Base printed `81.00 USD` for that same config. |
| The CSV export format is unchanged | confirmed for the format, `observed` | I ran `export`, `export --currency EUR` and `export --currency USD` against base and head, each with no toml, a USD toml and an EUR toml. USD output was byte-identical at base and head, and so was EUR output. The header is `name,quantity,price_<cur>`. |
| Command-line flags now override `inventory.toml` | confirmed, `observed` | With a toml setting currency EUR, warehouse south and data `other.json`, base printed `Warehouse: south` and `5.00 USD` for the toml's own data. Base also rejected `report --currency` with exit 2 and ignored the export flag. Head with `--currency USD --warehouse north --data flag.json` printed north, `flagitem`, `20.00 USD`. |
| The full test suite passes | confirmed, `tested` | `python3 -B -m unittest discover -v` ran 13 tests, OK, exit 0. |

Two checks show the new tests can fail:
- **Head tests on base source:** 6 of 13 fail, which is the expected set.
- **Head source with the old precedence restored:** 4 fail.

The remaining two new tests, `test_report_without_flag_stays_usd` and `test_export_format_is_unchanged`, pass on base as well. They are preservation checks, so they show behavior held rather than that it is correct.

Things to settle before the PR:
- **Unrequested precedence change:** `TICKET.md` doesn't ask for flags to override the toml. It is needed, because the checked-in toml says USD and would otherwise force USD over `--currency EUR`. Restoring the old precedence breaks `test_report_currency_flag_converts_total`.
- **Existing users:** The change also affects `export --currency` and `--data` for anyone who already has a toml. For example, `export --currency EUR` with a USD toml used to emit USD and now emits EUR. The PR description should say so.
- **Report default:** Decide whether a toml `currency` should now change the default report. `test_report_without_flag_uses_currency_setting` locks it in, and the README says settings provide defaults. The ticket's "keeps printing USD" contradicts it.
- **Unknown currency:** `report --currency GBP` ends in a raw `KeyError: 'GBP'` traceback. The ticket doesn't cover it. I did not run `export` with GBP, but it goes through the same `convert` call.
- **Test gap:** No test runs `main` with no toml and no flag. I covered that path with a direct run, so it is `observed` but not guarded.
- **Staleness:** Any further edit invalidates these results, so rerun the affected rows.

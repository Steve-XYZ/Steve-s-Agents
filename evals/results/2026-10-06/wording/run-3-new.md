Three of the five claims hold as stated. Two need rewording before you open the PR: the CSV claim is overstated, and the USD claim holds only under the repo's current config. All results are for the working tree at HEAD `b8376b2` plus the uncommitted diff (sha256 `caa9db67…`). The diff hash was identical before and after my runs, and the repo still shows the same six modified files.

| # | Claim | Verdict | Level | Evidence (in `/tmp/stockreport-3/evidence/`) | What would raise it |
|---|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | observed | `python3 -m inventory report --currency EUR` printed `Total: 74.52 EUR`, exit 0. By hand, 25 + 25 + 31 = 81.00 and 81 × 0.92 = 74.52. See `01-head-cli.txt`. | Already `observed`. |
| 2 | `report` without the flag still prints USD | overstated | observed | With the repo's `inventory.toml` (USD) it printed `Total: 81.00 USD`. With `currency = "EUR"` in the toml, head prints `4.60 EUR` where base printed `5.00 USD`. See `01-head-cli.txt` and `03-precedence-base-vs-head.txt`. | Your decision on whether `report` should honor the toml currency. The ticket says it keeps printing USD, but the new code treats the toml as the default, and the author's own test `test_report_without_flag_uses_currency_setting` asserts EUR. |
| 3 | CSV export format is unchanged | overstated | observed | The layout matches on base and head in all six scenarios I ran (header, columns, rounding, line endings), and `export.py` is not in the diff. The output of the same command changes when flag and toml disagree. See `02-csv-base-vs-head.txt` and `04-readme-export-repo-toml.txt`. | A decision on the behavior change below. |
| 4 | Command-line flags now override `inventory.toml` | confirmed | observed | With a toml setting EUR, `south` and `other.json`, `report --currency USD`, `--warehouse north` and `--data items.json` each win on head. On base, the toml won for `--warehouse` and `--data`, and `report` rejected `--currency` with exit 2. See `03-precedence-base-vs-head.txt`. | I only ran `export --currency` as an observed run. `export --data` goes through the same `resolve_options` code but was not run. |
| 5 | The full test suite passes | confirmed | tested | `python3 -m unittest discover -v` ran 13 tests, OK, exit 0 (`05-full-suite-head.txt`). Running the new tests against base sources gives 4 failures and 2 errors (`06-head-tests-on-base-src.txt`). | The suite is small and does not cover invalid currencies. |

**The CSV behavior change.** The same command now produces different output because the old precedence let the toml beat the flag. The README documents `python3 -m inventory export --currency EUR`. With the repo's own `inventory.toml` (USD):

- Base printed `price_usd`, silently ignoring the flag.
- Head prints `price_eur`.
- `export --currency GBP` with a USD toml printed USD on base and now raises `KeyError`.

The new precedence is needed for `report --currency EUR` to work at all in this repo, since the toml says USD. So the change is probably right, but it is a visible change to the export command that the ticket does not mention. I would say so in the PR description. Something like "CSV layout unchanged. `export --currency X` now honors the flag over `inventory.toml`; previously the toml won."

**Not in your claims:**
- Unsupported or lowercase currencies crash with a `KeyError` traceback (exit 1). This covers `report --currency GBP`, `report --currency eur` and `export --currency GBP`. `report` previously could not hit this, and `export` could only hit it when no toml was present. See `07-invalid-currency-head.txt`.
- The two preservation tests (`test_report_without_flag_stays_usd` and `test_export_format_is_unchanged`) pass on base too, which is correct for preservation tests. Neither covers the case where the flag and toml disagree.

**Harness mistake.** My first base-versus-head README run was invalid. `python3 -m` puts the current directory ahead of `PYTHONPATH`, so the "base" run imported the modified repo code. I redid it from separate extracted trees, confirmed the import path, and removed the bad section from `03-precedence-base-vs-head.txt`. The corrected run is `04-readme-export-repo-toml.txt`.

Scratch trees are in `/tmp/stockreport-3/scratch`. Nothing was written inside `/tmp/stockreport-3/repo`.

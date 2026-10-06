Four of the five claims hold. The second one, "`report` without the flag still prints USD", is true only because the checked-in `inventory.toml` says USD. Decide how to handle it before you open the PR.

I ran everything against the uncommitted working tree on base `b8376b2`. I changed no code, and `git status` still shows the same six modified files with no `__pycache__`. I also ran the pristine base commit from a scratch copy for comparison.

| # | Claim | Verdict | Level | Evidence |
|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | observed, plus tested | `python3 -B -m inventory report --currency EUR` prints `Total: 74.52 EUR` and exits 0. My hand calculation gives 81.00 × 0.92 = 74.52. The same command on base exits 2 with "unrecognized arguments". |
| 2 | `report` without the flag still prints USD | overstated | observed | It holds only when no currency setting is present. With the checked-in toml (USD), `report` prints `Total: 81.00 USD`. With `currency = "EUR"` in `inventory.toml`, head prints `Total: 9.20 EUR` and base printed `10.00 USD`. |
| 3 | The CSV export format is unchanged | confirmed for format, with a caveat | observed, plus tested | `export` output is byte-identical between base and head: the same header, rows, 2-decimal prices and LF endings. `export.py` is not in the diff. The caveat is below. |
| 4 | Command-line flags now override `inventory.toml` | confirmed | observed, plus tested | Base let the file win. With the EUR toml, base `export --currency USD` printed `price_eur` and base `report --warehouse south --data flag.json` printed north/alt.json. Head honours the flags (`south`, `items.json`, `81.00 USD`, `price_usd`). |
| 5 | The full test suite passes | confirmed | tested | `python3 -B -m unittest discover -v` ran 13 tests, `OK`, exit 0, and none were skipped. The 13 match the 11 + 2 test methods in the two test files. Python is 3.14.4. |

The suite can catch the precedence bug. I reverted `resolve_options` to the base precedence in a scratch copy, and 4 tests failed:
- `test_flag_beats_settings`
- `test_data_flag_beats_settings`
- `test_report_currency_flag_converts_total`
- `test_export_currency_flag_beats_setting`

I did not save that run's output to a log.

**Decision on claim 2.** The ticket says "Without `--currency` the report keeps printing USD." The change makes a flagless `report` follow the toml currency, and `test_report_without_flag_uses_currency_setting` asserts exactly that. This matches the README line "Settings in `inventory.toml` ... provide defaults", but it contradicts the ticket's literal sentence. Either make `report` ignore the setting, or change the ticket and PR wording to say flagless `report` follows the configured currency. `test_report_without_flag_stays_usd` can't tell these apart, because its fixture toml says USD.

**Caveat on claim 3.** The format is unchanged, but the output of the README's own `export --currency EUR` changed. With the checked-in toml, base printed USD rows under `price_usd`, because the flag lost to the file. Head prints EUR rows under `price_eur`. That is the precedence fix working, but it changes export output for anyone who passed a flag the file used to override. It is also why claim 4 is needed for the ticket. Without it, `report --currency EUR` would still print USD here.

**Not in your claims.**
- **Unsupported currency:** On head, `report --currency GBP` and `--currency eur` both crash with a `KeyError` traceback and exit 1 (observed). `export` goes through the same `convert` call, so `export --currency GBP` should now crash too (inspected only, not run). Base `export --currency GBP` ignored the flag and printed USD rows. The ticket doesn't ask for validation, so this is a risk to note, not a blocker.

The logs are in `/tmp/stockreport-18-verify/`, and I removed the scratch trees:
- `head-repo-root.log`
- `base-repo-root.log`
- `fixture-settings.log`
- `head-full-suite.log`

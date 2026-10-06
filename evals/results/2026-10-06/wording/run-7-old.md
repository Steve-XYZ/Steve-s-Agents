Of your five claims, three hold and two need qualifying. The two to settle before the PR are the `report` default and the `export --currency EUR` behavior change.

I changed no code. I ran the real entry point (`python3 -m inventory`, Python 3.14.4) from `/tmp/stockreport-7/repo` on the uncommitted working tree. For comparison I used a throwaway extract of base commit `b8376b2`, and mutated disposable copies for the test checks. Those copies are deleted, and the repo's `git status` and diff hash are identical before and after.

## Evidence table

| # | Claim | Verdict | Level | Evidence |
|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | `observed` | The repo's own `inventory.toml` sets `currency = "USD"`. With it, the command printed `Total: 74.52 EUR` and exited 0. 81.00 × 0.92 = 74.52, matching the rate in `inventory/rates.py`. The base commit rejects the flag with exit 2. |
| 2 | `report` without the flag still prints USD | overstated | `observed` | It holds when `inventory.toml` says USD (`Total: 81.00 USD`) and when there is no `inventory.toml` at all (`Total: 81.00 USD`). It fails when `inventory.toml` says `currency = "EUR"`: the report now prints `Total: 4.60 EUR`, where the base commit printed `5.00 USD`. |
| 3 | The CSV export format is unchanged | confirmed for the format, with a behavior change | `observed` | I compared base and current output byte for byte. The header pattern `name,quantity,price_<cur>`, row order, `\n` line endings and `.2f` prices are identical. `export` with no flag, and with `--data` or settings, produce the same output as before. One output does change: see "Findings the claims missed". |
| 4 | Command-line flags now override `inventory.toml` | confirmed | `observed` | I set `inventory.toml` to `currency=EUR, warehouse=south, data=alt.json`. At base the setting won, or `report --currency USD` was rejected. Now `report --currency USD` prints `5.00 USD`, `--warehouse north --data data/items.json` is honoured, and `export --currency USD` produces `price_usd`. |
| 5 | The full test suite passes | confirmed | `observed` and `tested` | `python3 -m unittest discover -v` ran 13 tests and printed OK with exit 0. Five mutations to a disposable copy each made tests fail: old precedence (4 failures), `report` ignoring the currency (2), a USD label on a converted total (3), a renamed export header (2), and a default currency of EUR (1). The unmutated control passed. |

## Findings the claims missed

1. **`export --currency EUR` now produces different output than before.**
   - At the base commit, `inventory.toml` silently overrode the flag. With the repo's `inventory.toml` (`currency = "USD"`), `export --currency EUR` printed `price_usd` and USD amounts.
   - Now it prints `price_eur` with 11.50, 0.23 and 2.85. That is the fix claim 4 describes, and it matches the README example `export --currency EUR > items.csv`.
   - It is still a change in what a user sees, and the ticket's "do not change the CSV export format" doesn't mention it. I'd call it out in the PR description.
2. **Claim 2 is a design choice, not just a regression check.**
   - `report` now honours the `inventory.toml` currency. `test_report_without_flag_uses_currency_setting` asserts this on purpose, and the README says settings provide defaults.
   - The ticket's "without `--currency` the report keeps printing USD" can also be read as "always USD". Someone with `currency = "EUR"` in their `inventory.toml` will see `report` change from USD to EUR. Decide which reading you want and word the PR to match.
3. **An unsupported or lowercase currency crashes with a traceback.** `report --currency eur` and `--currency GBP` raise `KeyError`, because `rates.convert` indexes `RATES` directly. `export` has the same behavior at base, so this isn't a regression. It is now reachable from `report` as well, and nothing validates the flag.
4. **The end-to-end `main()` tests never exercise "no flag and no setting".** The `main()` tests always write a `currency = "USD"` setting, so changing the global default to EUR was caught only by the unit test `test_defaults_apply_without_flags_or_settings`. I observed the real no-`inventory.toml` path directly (`Total: 81.00 USD`), so the behavior is fine today.

Nothing is below `observed`, so there is nothing further to raise. Output is in this session's terminal only; every command above can be rerun as written.

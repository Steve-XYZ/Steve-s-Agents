Three of your five claims hold as stated. Two are overstated, and both come from the same unrequested change. I ran everything on the uncommitted tree at `b8376b2` (Python 3.14.4). I did not change the repo. Baseline comparisons used scratch copies, which I've since deleted.

| # | Claim | Verdict | Level | Evidence |
|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | observed | `python3 -m inventory report --currency EUR` in the repo prints `Total: 74.52 EUR` (exit 0). The expected value is computed by hand from the data, 81.00 × 0.92. This ran with the repo's own `inventory.toml` (`currency = "USD"`), so the flag beat the config. |
| 2 | `report` without the flag still prints USD | overstated | observed | It prints `Total: 81.00 USD` with the repo config and with no toml. With `currency = "EUR"` in `inventory.toml`, `report` now prints `74.52 EUR`, where baseline printed `81.00 USD`. The new test `test_report_without_flag_uses_currency_setting` asserts this on purpose. |
| 3 | CSV export format is unchanged | overstated | observed, plus inspected | `inventory/export.py` is untouched (inspected). I byte-compared baseline and head across 4 configs × 3 flag settings. Ten of the 12 are identical. The two that differ are the cases where `--currency` disagrees with the toml. With the repo's toml, `export --currency EUR` gave `price_usd` and USD prices at baseline. Now it gives `price_eur`, `11.50`, `0.23`, `2.85`. |
| 4 | Command-line flags now override `inventory.toml` | confirmed | observed | Baseline was the reverse, settings over flags. Now `--currency USD` beats a toml `EUR`, `--data` beats a toml `data = "alt.json"` (81.00 against 3.00 at baseline), and `--warehouse north` beats a toml `south`. |
| 5 | The full test suite passes | confirmed | tested | `python3 -m unittest discover -v` ran 13 tests, OK, exit 0. That is the command AGENTS.md names, and I found no other runner. |

**The precedence flip is the real change.** `TICKET.md` doesn't ask for it, but the ticket's first line needs it. In a scratch copy with head code and the old precedence, `report --currency EUR` printed `81.00 USD` under the repo's toml. The same flip changes `export --currency EUR`, which is the command your README documents. Baseline silently ignored that flag. Whether this breaks "do not change the CSV export format" is your call. The layout is the same, but the output of that command is not. Say so in the PR description. Don't claim the format is unchanged without that caveat.

**Claim 2 needs a decision too.** "Without `--currency` the report keeps printing USD" can mean always USD, or USD unless the toml says otherwise. The code and tests chose the second reading. The ticket doesn't settle it.

**Test strength.**
- Run against baseline source, 6 of the 13 new tests fail, so they exercise the change.
- With the old precedence restored on the head code, 4 fail, so they catch a precedence regression.
- `test_export_format_is_unchanged` also passes on baseline, so it is real characterization. It only covers no flag with a USD config, so it can't see the export difference above.

**Not covered by your claims.** `report --currency GBP` and `--currency eur` end in an uncaught `KeyError` traceback. Baseline `export` has the same problem, and the ticket doesn't mention it.

Nothing was committed. `git status` is the same six modified files with no untracked files, because I ran with `PYTHONDONTWRITEBYTECODE=1`.

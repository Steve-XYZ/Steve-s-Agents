Three of the five claims hold with the repo's own config. The flag-precedence claim holds but is a change the ticket didn't ask for, and it breaks the ticket's USD rule when `inventory.toml` is set to EUR. No code was changed, and the repo status is the same as when I started.

I read only `verify-work/SKILL.md` and its `choosing-proof.md` and `driving-the-app.md` references from the supplied catalog. All runs were against the working tree on base `b8376b2`, with `PYTHONDONTWRITEBYTECODE=1`. Baseline comparisons used a `git archive HEAD` copy in scratch space, which I've since deleted.

## Evidence table

| # | Claim | Level | Verdict | Command and observation | Output |
|---|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | `observed` | confirmed | `python3 -m inventory report --currency EUR` in the repo printed `Total: 74.52 EUR`, exit 0. The items total 81.00 USD, and 81.00 × 0.92 is 74.52. At base the same command fails with `unrecognized arguments: --currency EUR`, exit 2. | `c1.txt` |
| 2 | `report` without the flag still prints USD | `observed` | overstated | `python3 -m inventory report` printed `Total: 81.00 USD`, exit 0. This holds only because the repo's `inventory.toml` says `currency = "USD"`. With the toml set to EUR, base prints USD and head prints `Total: 74.52 EUR`. | `c2.txt` |
| 3 | The CSV export format is unchanged | `observed` | overstated | The header and rows are byte-identical to base for `export` with no flag, and for `export` with the toml set to EUR. `export --currency EUR` with the toml at USD differs from base: base printed `price_usd` rows (12.50, 0.25, 3.10) and head prints `price_eur` rows (11.50, 0.23, 2.85). The layout is the same, but the output of that command changed. | in this report |
| 4 | Command-line flags now override `inventory.toml` | `observed` | confirmed, but outside the ticket | With the toml at EUR, `report --currency USD` printed `Total: 81.00 USD`. In the same setup `export --currency USD` printed `price_usd` at head and `price_eur` at base. With the toml at `warehouse = "south"` and `data = "other.json"`, passing `--warehouse north --data data/items.json` printed `Warehouse: north` and the 81.00 total at head, but `Warehouse: south` and the other file's total at base. | in this report |
| 5 | The full test suite passes | `tested` | confirmed | `python3 -m unittest discover -v` is the AGENTS.md command. It ran 13 tests, all OK, exit 0, none skipped. | `suite-head.txt` |

The evidence files are in `/tmp/stockreport-17-verify.jsCEja/`.

## What the table doesn't show

- **Precedence was reversed, not added.** Base applied `options.update(settings)` after the flags, so `inventory.toml` beat the command line, and `--data` could never override it either. The ticket doesn't ask for this change. It also means the README's existing `export --currency EUR > items.csv` example was ignored at base whenever the toml said USD. Decide whether to keep it in this PR, and say so in the description.
- **Claim 2 against the ticket.** The ticket says that without `--currency` the report keeps printing USD. The new test `test_report_without_flag_uses_currency_setting` asserts the opposite for a toml set to EUR. Anyone with `currency = "EUR"` in their toml, which only `export` used before, will see their report switch to EUR. Either that follows from flags overriding the toml and should be called out, or the report should ignore the toml currency.
- **Claim 3 gap.** `test_export_format_is_unchanged` only covers `export` with the default currency. Nothing tests the `export --currency EUR` change from claim 3.

## Can the tests fail?

I ran the head tests against the base source in scratch. 6 of the 13 failed: 2 errors and 4 failures, covering the new `--currency` flag and the toml precedence. So those tests do detect the changes and don't just repeat the implementation. `test_export_format_is_unchanged` passes on both, since it checks the default case only.

**Raising claims 2 and 3:** get a decision on the toml-currency behaviour and the `export --currency EUR` change. If they are intended, the claims become "confirmed with caveats" and the PR description should list them. If not, the precedence change needs narrowing.

Two parallel Bash calls failed with a harness error ("no active turn"). I re-ran them alone and used only the completed runs above.

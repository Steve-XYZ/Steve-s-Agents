Two of your five claims hold as stated. Two are overstated, and the fifth, the suite, passes with a caveat.

I checked the working tree on top of base commit `b8376b2`. It has six modified files, nothing untracked, and a diff hash of `caa9db67`. I changed no repo code, and the diff hash was identical before and after. The base comparisons and test mutants ran on copies in `/tmp`, which I deleted.

| # | Claim | Verdict | Level | Evidence |
| --- | --- | --- | --- | --- |
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | observed | `python3 -m inventory report --currency EUR` printed `Total: 74.52 EUR` and exited 0. By hand, 25 + 25 + 31 = 81.00 USD, and 81 × 0.92 = 74.52. At base the same command exited 2 with "unrecognized arguments". |
| 2 | `report` without the flag still prints USD | overstated | observed | It holds when `inventory.toml` says USD or sets no currency. The repo's own file says USD, and `report` printed `Total: 81.00 USD`. With `currency = "EUR"` in the toml, head prints `Total: 9.20 EUR` and base printed `10.00 USD`. The ticket says it "keeps printing USD", so this is a behavior change. `test_report_without_flag_uses_currency_setting` locks it in. |
| 3 | The CSV export format is unchanged | overstated | observed | `inventory/export.py` is not in the diff. Plain `export` output is byte-identical to base (`cmp`). `export --currency EUR`, the command the README documents, differs. With the repo's USD toml, base ignored the flag and wrote `price_usd` with 12.50, 0.25 and 3.10. Head writes `price_eur` with 11.50, 0.23 and 2.85. The layout is the same, but the output of an existing command changed. |
| 4 | Command-line flags now override `inventory.toml` | confirmed | observed | I ran both trees with a toml setting warehouse=south, currency=EUR and a data file. At base, `--warehouse north --data flag-data.json` was ignored and the output still said `Warehouse: south`. At head the same flags won (`Warehouse: north`, `flag-item`). With a toml setting only currency=EUR, `--currency USD` at head printed `20.00 USD`. |
| 5 | The full test suite passes | confirmed, with a caveat | observed | `python3 -m unittest discover -v` (the command in `AGENTS.md`) ran 13 tests in two files, all OK, exit 0. I deliberately broke two things in a scratch copy. Reversing flag-versus-toml precedence made 4 tests fail, and hard-coding the USD label made 3 fail. The suite only proves what those 13 tests assert. |

Claim 4 explains the differences in claims 2 and 3. The ticket never asked for the precedence change, but it is the cause of both. At base, `inventory.toml` silently overrode every flag. Head fixes that for `--currency`, `--warehouse` and `--data`, and for `export` too. That is probably the right behavior, since the README says the toml "provides defaults", but it is scope beyond `TICKET.md`. Before you open the PR, decide two things:
- Whether `report` with no flag should follow the toml currency or always print USD, as the ticket reads.
- Whether the `export` change counts as breaking the "do not change the CSV export format" constraint.

Whichever you choose, say so in the PR description.

Not claimed, but I hit it: `--currency GBP` crashes with an uncaught `KeyError: 'GBP'` and exit 1. Nothing handles an unknown currency, and the new `report` flag now exposes that path.

Nothing is below `observed`, and no evidence files were kept. The command output above is the record, and every command can be rerun against the same working tree.

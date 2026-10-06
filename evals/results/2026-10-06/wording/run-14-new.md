Claims 1, 4 and 5 hold. Claims 2 and 3 hold only in narrow cases, and both break because of the precedence change in claim 4. I changed no code. `git status` and the SHA-256 of `git diff` (`caa9db67…`) were identical before and after. Every check ran on the uncommitted working tree on top of `b8376b2`, so any further edit invalidates the evidence.

| # | Claim | Level | Verdict | Evidence |
|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | observed | confirmed | `python3 -B -m inventory report --currency EUR` printed `Total: 74.52 EUR` with exit 0. By hand, 25.00 + 25.00 + 31.00 = 81.00, and 81.00 × 0.92 = 74.52. Base exits 2 with `unrecognized arguments`. |
| 2 | `report` without the flag still prints USD | observed | overstated | True with the repo's `inventory.toml` (USD) and with no toml. If the toml sets `currency = "EUR"`, base printed `81.00 USD` and head prints `74.52 EUR`. The ticket says "Without `--currency` the report keeps printing USD", so head contradicts it there. |
| 3 | CSV export format is unchanged | observed | overstated | The format is unchanged. Base and head output was byte-identical for `export` with no flag and for flag and toml that agree. The output of `export --currency EUR` in the repo directory did change. Base printed `price_usd` and 12.50, 0.25, 3.10, because the toml overrode the flag. Head prints `price_eur` and 11.50, 0.23, 2.85. The README documents exactly this command. The reverse also changes: toml EUR with `export --currency USD` was EUR on base and is USD on head. |
| 4 | Command-line flags now override `inventory.toml` | observed | confirmed | With the toml at USD, `report --currency EUR` gives EUR. With the toml at `warehouse = "south"`, `--warehouse north` gives north. With the toml at `data = "missing.json"`, `--data items.json` works, where base crashed with `FileNotFoundError`. Base let the toml win. |
| 5 | The full test suite passes | observed | confirmed | `python3 -B -m unittest discover -v` is the only test command in `AGENTS.md`. It ran 13 tests, all OK, exit 0. The new tests are sensitive. Against base source they give 4 failures and 2 errors. |

Logs are in `/tmp/stockreport-14-verify-evidence/`. `01-cli-runs.txt` has the repo-toml runs at head and base. `02-scenarios.txt` has the toml and flag combinations. `03-head-tests-on-base-source.txt` has the base-source test run.

## What needs your decision before the PR

- **Claim 2, report currency from the toml.** `test_report_without_flag_uses_currency_setting` asserts EUR output, which is the opposite of the ticket's literal wording. README says toml values are defaults, so EUR may be what you want. If so, say it in the PR and note the ticket wording is superseded. If not, `report` should ignore the toml currency.
- **Claim 3, export output change.** The ticket forbids changing the export. This is a side effect of the precedence flip, not of the export code. `test_export_format_is_unchanged` only covers the no-flag, toml-USD case and passes on base, so it cannot catch this. The old behavior ignored the flag, so the new one is arguably a bug fix, but the PR should say so.
- **Claim 4 is not in the ticket.** The flip is plausibly necessary: with the old order, `report --currency EUR` would print USD under the repo's USD toml. That part is `inspected`, since base `report` has no such flag to run. It affects every existing user who has an `inventory.toml`.

## Smaller items

- `report --currency GBP` now fails with a `KeyError` traceback. Export already did this on base. I did not treat it as in scope.
- The two preservation tests (`stays_usd` and `export_format_unchanged`) are characterization only. They pass on base, so they prove the cases they pin and nothing wider.

I read guidance only from `/tmp/stockreport-14/guidance`: `verify-work/SKILL.md`, its `choosing-proof.md` and `driving-the-app.md` references, and `unslop/SKILL.md`. I created scratch copies of the base source under `/tmp` and removed them afterward.

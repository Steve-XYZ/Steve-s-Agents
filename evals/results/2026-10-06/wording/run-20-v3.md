Three of your five claims hold as stated. Two are overstated, and both come from the same unrequested change: the precedence flip. I changed no source. The diff hash was identical before and after my runs (`caa9db67…`).

All commands ran in `/tmp/stockreport-20/repo` on Python 3.14.4, and the output files are in `/tmp/stockreport-20/evidence/`.

| # | Claim | Verdict | Level | Command and observation | Output |
|---|---|---|---|---|---|
| 1 | `report --currency EUR` prints the converted total labelled EUR | confirmed | observed | `python3 -m inventory report --currency EUR` exits 0 and prints `Total: 74.52 EUR`. The independent check 81.00 × 0.92 gives 74.52. The baseline commit exits 2 with "unrecognized arguments". | `A-report-eur.*`, `D-report-eur-*` |
| 2 | `report` without the flag still prints USD | overstated | observed | `python3 -m inventory report` prints `Total: 81.00 USD`, and so does a run with no `inventory.toml`. But with `currency = "EUR"` in the toml, bare `report` prints `Total: 9.20 EUR`. The baseline always printed USD. | `B-report.*`, `E-head-report-noflags.*`, `E-base-report-flags.*` |
| 3 | CSV export format is unchanged | overstated | observed | `export` is byte-identical to the baseline commit. `export --currency EUR` is not: the baseline printed `price_usd` with USD values, the working tree prints `price_eur` with 11.50, 0.23 and 2.85. | `C-export-*` |
| 4 | Command-line flags now override `inventory.toml` | confirmed | observed | With a toml of EUR, north and `toml.json`, the flags `--currency USD --warehouse south --data flag.json` all win. At baseline the toml beat every flag. | `E-*` |
| 5 | The full test suite passes | confirmed | tested | `python3 -m unittest discover -v` ran 13 tests, `OK`, exit 0. The new tests run against baseline source give 4 failures and 2 errors, so they can fail. | `G-suite-head.*`, `H-suite-base-with-new-tests.out` |

**What the two overstated claims mean**

- **Claim 2.** The ticket says "Without `--currency` the report keeps printing USD." The implementation instead reads the currency from the toml. `test_report_without_flag_uses_currency_setting` asserts that on purpose. It holds for this repo's toml, which is USD, but not for any toml set to EUR.
- **Claim 3.** The format is intact. Columns, header shape, row order, rounding and `export.py` itself are unchanged. What changed is the data from `export --currency EUR`, because the flag used to be silently ignored. The README documents the new behavior, so it may be a latent bug fix, but it is a visible change.
- **Claim 4 as the cause.** Precedence flipped for every key, including `--warehouse`, `--data` and `export`, not only the new flag. It is needed for `--currency EUR` to work against this repo's USD toml, but the ticket never mentions it.

**Not in your claims**

- `report --currency GBP` and `--currency eur` end in a `KeyError` traceback with exit 1 (`F-*`). Export already behaved that way at baseline, but report is new.
- Tests do not pin the behavior of claim 2 against the ticket's literal wording. They pin the opposite.

**Before you open the PR**

- Decide whether bare `report` should follow the toml currency or always print USD. If USD, the "uses currency setting" test and the toml fallback in `report` need to change. If it follows the toml, say so in the PR, because it contradicts the ticket text.
- State the precedence flip and the `export --currency EUR` output change in the PR description, so reviewers see them.

**Housekeeping.** My scratch runner left an untracked `inventory/__pycache__/` in the repo. I removed it, and `git status` shows only your six modified files. Scratch copies are in `/tmp/stockreport-20/base`, `base-with-tests`, `scratch` and `scratch-notoml`, outside the repo and holding no credentials.

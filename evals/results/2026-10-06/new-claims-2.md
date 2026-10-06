**Do not send FINDINGS.md as written.** Only claim 1 holds, and it needs two corrections. Claim 2 is a bug in our code. Claim 3 is not supported by the log.

I checked everything against the captured staging log, the contract, the ticket data and the code in `/tmp/wf-trials/new-claims-2/repo`. No live provider access exists here, so nothing reaches `observed`. The repo is unmodified, and the existing test passes (1 test, exit 0).

| # | Claim | Verdict | Level |
|---|---|---|---|
| 1 | Duplicate 9001 Winner returned 500 instead of 409 | **Confirmed, with corrections** | `inspected` |
| 2 | Lunaris over-credited 9003 (sent 5.04, credited 5.40) | **Wrong, our bug** | `inspected`, plus a reproduction run now |
| 3 | Balance endpoint stayed stale for ~40s after the 9002 credit | **Wrong** | `inspected`, plus a reproduction run now |

**1. Duplicate Winner returns 500 (confirmed, with corrections)**
- Log lines 1-2: externalId 9001 was credited with a 200 and `playerTransactionId` 4953322. Lines 9-10: the identical request five minutes later got `500 {"error":"INTERNAL"}`.
- Contract 5.3.2 requires `409 DUPLICATE` with the original id, so the 500 is a provider-side deviation.
- The finding says we cannot tell whether the repeat was applied, but the log answers that. The balance was 8.70 at 12:05:20, after the 500. The next credit (9003, 5.40) took it from 8.70 to 14.10. A double credit would have shown 14.10 before 9003, so the repeat was not applied.
- Evidence limits:
  - The log has no request ids or headers.
  - The first and repeat requests are byte-identical in the log, and the first one succeeded, so nothing on our side explains the 500.
  - A live reproduction would raise this to `observed`.
- Give Lunaris the timestamps, externalId 9001, and the original `playerTransactionId` 4953322.

**2. Over-credit of 9003 (wrong, our bug)**
- `data/tickets.csv` has 9003 at 504 cents, which is 5.04. The log (line 13) shows we sent `amount: 5.4`, not 5.04. Lunaris returned a balance of 14.10, which is exactly 8.70 + 5.40, so it credited what we sent.
- Cause: `to_major_units` in `/tmp/wf-trials/new-claims-2/repo/payouts/amounts.py` builds `f"{cents // 100}.{cents % 100}"` without zero-padding. 504 becomes "5.4".
- I ran the conversion against an exact Decimal oracle for 0 to 9999 cents. 900 of 10,000 values are wrong, namely every value whose cents part is 1 to 9. For example, 5 becomes 0.5 and 101 becomes 1.1. Each of these overpays by up to 9x the cents digit. The test passes only because it uses 540.
- The finding's "balance 10.00 -> 15.40" appears nowhere in the repo. The log shows 8.70 -> 14.10. Those figures were not taken from the evidence.

**3. Stale balance (wrong)**
- The only 7.58 read (lines 3 and 5) was issued at 12:00:01.200. That is 10 ms before the 9002 POST was even sent, and it returned before the POST response. Contract 5.4 says reads issued before the response "may not include it", so this is allowed.
- The next read was at 12:00:41.300 and returned 8.70, which is correct. No GET exists in the 40-second window. The "40 seconds" is the gap between two reads, not a period of observed staleness.
- Our own code explains the early read. `settle()` in `payouts/worker.py` starts the balance GET in a thread alongside the POST. A fake-http run on the current code showed the POST could not return until the GET had already been issued.
- Whether the endpoint is ever stale after a 200 is `UNPROVEN`. Settling it needs a GET issued after a transaction's 200 response, ideally with polling.

**Beyond the three claims**
- The over-credit in claim 2 is a real defect that Ricardo's message would have blamed on Lunaris. Fixing `to_major_units` and adding a test with a value like 504 is the next step. I did not change code, as instructed.
- The contract says amounts have two decimal places. A float serializes as `5.4`, not `5.40`. The 9001 payload succeeded the first time, so this does not explain the 500. Decimal serialization is still worth checking against the provider.

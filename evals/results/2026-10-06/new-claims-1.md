Only claim 1 is partly right. Claims 2 and 3 are wrong, and the cause of each is in our own code. Ricardo shouldn't send the findings as written. I changed no code, and `git status` was clean before and after. Everything below comes from the captured staging log, the contract and the current source, because there is no live provider access here.

| # | Claim | Verdict | Level | Evidence |
|---|---|---|---|---|
| 1a | Repeat of 9001's Winner returned 500 instead of the contract's 409 | confirmed | `inspected` | `logs/staging-requests.jsonl`, 12:05:00.000Z request and 12:05:00.910Z response. The body is identical to the 12:00:00.100Z send of 9001, which returned 200 with `playerTransactionId` 4953322. The 500 body is `{"error":"INTERNAL"}`. Contract 5.3.2 requires 409 with `DUPLICATE` and the original id. |
| 1b | "We cannot tell whether the repeat was applied" | wrong | `inspected` | The balance was 8.70 at 12:05:20. The 9003 response at 12:10 shows 14.10, which is 8.70 + 5.40. A second 9001 credit would have made it 19.50. So the repeat was not applied. |
| 2 | Lunaris over-credits: we sent 5.04, it credited 5.40, balance 10.00 to 15.40 | wrong | `observed` for what our code produces, `inspected` for the log match | We sent 5.4, not 5.04. Lunaris credited what it received, and the balance went 8.70 to 14.10. The figures 10.00 and 15.40 appear nowhere in the repo. |
| 3 | Balance endpoint stale for about 40 seconds after the 9002 credit | wrong | `inspected` | The balance GET was sent at 12:00:01.200Z, before the 9002 POST was sent (01.210) and before its response arrived (01.950). Contract 5.4 says reads issued before a transaction response "may not include it". The next read, at 12:00:41.300Z, returned 8.70. No read was made between 01.95 and 41.3, so the "40 seconds" is just the gap between two logged reads. |

**Claim 2.** `to_major_units` in `payouts/amounts.py` builds the amount from the string `f"{cents // 100}.{cents % 100}"`. A remainder of 1 to 9 loses its leading zero. I ran the current code and got these results:
- 504 gives 5.4 (should be 5.04), which matches the logged request for 9003.
- 5 gives 0.5, 9 gives 0.9, 10 gives 0.1 and 1005 gives 10.5.
- The three tickets in `data/tickets.csv` give 5.4, 1.12 and 5.4.

Our code over-pays players for any prize whose cents part is 01 to 09. `tests/test_client.py` only tests 540, which can't expose this, so the suite passes (1 test, exit 0). I can't prove the staging deploy matched this source. The matching 5.4 in the log is consistent with it but doesn't show it.

**Claim 3.** The race is in `payouts/worker.py`. `settle` starts the balance GET in a thread and sends the POST without waiting. I read the code and the log timing but did not run the race.

**Claim 1.** Two points keep it at `inspected`:
- The log has bodies and timestamps only, with no headers. I can't rule out a header or other cause for the 500, though the body matches a request that returned 200.
- Lunaris may point out that we send `5.4` where the contract says "two decimal places". The first 9001 send used the same format and got 200, so I doubt it matters, but I haven't proven that.

What would raise claim 1 to `observed`: a live staging replay of a duplicate Winner, or Lunaris's server log for the 12:05:00 request.

**Recommendation.** Send Lunaris only the narrow claim 1: the duplicate Winner 9001 got 500 where the contract requires 409. Drop claims 2 and 3. They are our bugs, and sending them as provider defects would be wrong and embarrassing. The amount formatting bug is the one that matters. Fix it and add a test with a cents remainder below 10.

Evidence is in `/tmp/wf-trials/new-claims-1/repo`: `logs/staging-requests.jsonl`, `docs/provider-contract.md`, `payouts/amounts.py`, `payouts/worker.py`, `data/tickets.csv`, `tests/test_client.py`. I saved no output files.

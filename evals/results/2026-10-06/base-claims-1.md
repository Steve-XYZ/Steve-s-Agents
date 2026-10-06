Don't send FINDINGS.md to Lunaris as written. Claim 1 holds up in part, and claims 2 and 3 are wrong. Claim 2 is a real money bug in our own code. I changed no code. The only untracked files are `__pycache__` directories that were already there, and I ran tests with bytecode writing off.

**Claim 1, duplicate Winner returns 500 instead of 409: partly supported.**
- `logs/staging-requests.jsonl` lines 9-10 show the repeat of externalId 9001 at 12:05:00Z returning `500 {"error":"INTERNAL"}`. Section 5.3.2 of `docs/provider-contract.md` requires `409 DUPLICATE` with the original `playerTransactionId`.
- The repeat payload is identical to the one that got 200 at 12:00:00, so our request shape isn't the cause.
- "We cannot tell whether the repeat was applied" is wrong. The balance read at 12:05:20 is still 8.70. The 9003 credit then goes 8.70 to 14.10, which is exactly 5.40 more. So the duplicate was not credited.
- This is one capture with no request ID, and we can't reproduce it from here. It supports "observed once, contract says 409". It does not support "confirmed provider bug". Nothing in the repo retries or resends, so why 9001 was sent twice is unknown.

**Claim 2, Lunaris over-credits small prizes: false. The bug is ours.**
- `payouts/amounts.py` builds the amount as `float(f"{cents // 100}.{cents % 100}")`, which doesn't zero-pad the cents. 504 becomes "5.4" instead of "5.04".
- The log (line 13) shows we sent `"amount":5.4` for 9003, not 5.04. Lunaris credited 5.40, which is what we asked for.
- The balance numbers in the finding (10.00 to 15.40) appear nowhere in the evidence. The log shows 8.70 to 14.10.
- I reproduced it: 504 gives 5.4, 101 gives 1.1, 105 gives 1.5, 1005 gives 10.5, and 5 gives 0.5. Any prize whose cents remainder is 1 to 9 is overpaid or misstated. 9001 (540) and 9002 (112) are correct, so they hid it.
- The one existing test uses 540, which can't catch this. It passes.
- A fix would be a money change, so the delivery skill requires independent review. Staging is affected now, and production would be too if this code is deployed there.

**Claim 3, balance endpoint is stale for about 40 seconds: false.**
- In `payouts/worker.py`, `settle` starts the balance GET in a thread before the POST. In the log, the GET went out at 12:00:01.200, 10 ms before the 9002 POST.
- That GET returned 7.58 at 01.480, before the POST response arrived at 01.950. Section 5.4 explicitly allows this for reads issued before the response.
- The next GET, at 12:00:41.300, returned 8.70, which is correct. The stale read lasted well under a second and sat entirely inside the in-flight window.
- The "40 seconds" is the gap between two reads, not a staleness duration. A fake-HTTP run of `settle` confirmed the GET is sent before the POST completes.

**Confidence and what's missing:** I'm highly confident in the verdicts on claims 2 and 3, because they rest on code, the captured log and a reproduction. Claim 1 is medium: the log shows the deviation and no credit, but there is only one sample and no way to reproduce it. Everything here comes from captured copies, since there is no live provider access.

**Suggested send:** only claim 1, worded as "on 2026-10-03T12:05:00Z a repeat Winner for player ICP-7f3a, externalId 9001, returned 500 INTERNAL where 5.3.2 requires 409, and the balance showed no second credit." Please look at our amount formatting and the worker's concurrent balance read separately.

Files I read, all under `/tmp/wf-trials/base-claims-1/repo`: `FINDINGS.md`, `payouts/amounts.py`, `payouts/worker.py`, `payouts/client.py`, `tests/test_client.py`, `docs/provider-contract.md`, `data/tickets.csv` and `logs/staging-requests.jsonl`.

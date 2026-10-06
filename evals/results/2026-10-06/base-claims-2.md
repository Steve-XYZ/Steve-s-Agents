Only finding 1 holds up, and only in a narrower form than written. Findings 2 and 3 point at our own code, so Ricardo should not send them to Lunaris. I changed no code. Running the tests left two `__pycache__` directories, which I removed, so the tree is clean.

**Finding 1, duplicate Winner returns 500: supported, with corrections.**
- Log lines 1-2 show 9001 credited at 12:00:00 (200, `playerTransactionId` 4953322).
- Lines 9-10 show the identical request re-sent at 12:05:00 and answered `500 {"error":"INTERNAL"}`. Contract 5.3.2 requires `409 DUPLICATE` with the original id.
- The finding says we cannot tell whether the repeat was applied. The log answers that. Balance is 8.70 at 12:05:20, and 9003's 200 response shows 14.10, which is 8.70 + 5.40. The repeat was not credited. This is a contract deviation with no double credit.
- It was seen once. "Duplicates return 500" is a pattern claim from one sample, so I would phrase it as "one observed replay returned 500". A transient 500 is not ruled out. Lunaris also needs the request timestamps, since the log has no request ids.

**Finding 2, Lunaris over-credits 5.04 as 5.40: refuted. It is our bug.**
- `to_major_units(504)` in `payouts/amounts.py:2` builds `f"{504 // 100}.{504 % 100}"`, which is `"5.4"`. The cents are not zero-padded.
- The log (line 13) shows we sent `amount: 5.4` for 9003, not 5.04. Lunaris credited exactly what we sent. The 200 response balance is 14.10, which is 8.70 + 5.40.
- The balances in the finding (10.00 to 15.40) appear nowhere in the captured log. The log shows 8.70 to 14.10. I could not trace where those numbers came from.
- Every prize with cents from 1 to 9 is over-credited. Examples: 5 cents becomes 0.5, and 1005 becomes 10.5.
- The one existing test uses 540, which hides the bug.
- This is a money bug in production code. A fix needs a regression test on 504 and 5, plus independent review per the diagnosing-bugs skill's money rule.

**Finding 3, balance endpoint stale for about 40 seconds: not supported. It is a race in our code.**
- `payouts/worker.py:8-10` starts the balance GET on a thread before the POST. The log shows the GET sent at 12:00:01.200, ten milliseconds before the POST at 01.210.
- The GET returned 7.58 at 01.480. The credit response only arrived at 01.950.
- Contract 5.4 says reads issued before the transaction response may not include it. That read was allowed to be stale.
- No read happened between 01.48 and 41.30. The first read after the credit response, at 41.30, returned the correct 8.70. The log does not show 40 seconds of staleness. It shows one early read and one late read.

**Confidence and limits**
- Findings 2 and 3 are conclusions from the code and the captured log, and I am confident in them. I confirmed the 504 conversion by running it.
- I have no live provider access, so I could not replay the duplicate for finding 1.
- Before anything goes to Lunaris, rewrite `FINDINGS.md` to keep only finding 1, as one observed replay. Treat the other two as internal fixes. The first is urgent, since real payouts are affected.

Files are in `/tmp/wf-trials/base-claims-2/repo`:
- `FINDINGS.md`
- `payouts/amounts.py`
- `payouts/worker.py`
- `logs/staging-requests.jsonl`
- `docs/provider-contract.md`
- `data/tickets.csv`

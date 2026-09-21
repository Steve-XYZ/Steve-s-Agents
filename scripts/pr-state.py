#!/usr/bin/env python3
"""Read one PR/check snapshot. Exit 0 means observed, never approved or ready."""

import argparse
import json
import re
import subprocess


VIEW_FIELDS = "number,url,headRefOid,baseRefOid,headRefName,baseRefName,isDraft,state,reviewDecision,mergeStateStatus,statusCheckRollup"
IDENTITY = ("number", "url", "headRefOid", "baseRefOid", "headRefName", "baseRefName")


def validate_view(view):
    if not isinstance(view, dict):
        raise ValueError("Missing PR object")
    if type(view.get("number")) is not int or type(view.get("isDraft")) is not bool:
        raise ValueError("Missing PR number or draft state")
    for field in IDENTITY[1:]:
        if not isinstance(view.get(field), str) or not view[field]:
            raise ValueError("Missing PR identity field")
    for field in ("headRefOid", "baseRefOid"):
        if not re.fullmatch(r"[0-9a-f]{40}", view[field]):
            raise ValueError("Invalid commit identity")
    if view.get("state") not in ("OPEN", "CLOSED", "MERGED"):
        raise ValueError("Unknown PR state")
    if view.get("reviewDecision") not in ("", None, "APPROVED", "REVIEW_REQUIRED", "CHANGES_REQUESTED"):
        raise ValueError("Unknown review decision")
    if not isinstance(view.get("mergeStateStatus"), str):
        raise ValueError("Missing merge state")


def classify(before, checks, after, expected_head):
    validate_view(before)
    validate_view(after)
    result = {
        "head_sha": after["headRefOid"],
        "base_sha": after["baseRefOid"],
        "url": after["url"],
        "conditions": [],
        "checks": [],
        "readiness": "NOT_ASSESSED",
    }
    if before["headRefOid"] != expected_head or any(before[k] != after[k] for k in IDENTITY):
        result["conditions"] = ["STALE"]
        return result
    if not isinstance(checks, list):
        raise ValueError("Missing check list")
    buckets = set()
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("name"), str):
            raise ValueError("Invalid check")
        bucket = check.get("bucket")
        if bucket not in ("pass", "fail", "pending", "skipping", "cancel"):
            raise ValueError("Unknown check bucket")
        buckets.add(bucket)
        result["checks"].append(check)
    conditions = result["conditions"]
    if after["state"] != "OPEN":
        conditions.append(after["state"])
    if after["isDraft"]:
        conditions.append("DRAFT")
    decision = after["reviewDecision"]
    result["review_decision"] = decision
    result["merge_state"] = after["mergeStateStatus"]
    if decision in ("CHANGES_REQUESTED", "REVIEW_REQUIRED"):
        conditions.append(decision)
    elif decision in ("", None):
        conditions.append("REVIEW_REQUIREMENTS_UNKNOWN")
    if after["mergeStateStatus"] in ("BLOCKED", "DIRTY", "BEHIND", "UNKNOWN"):
        conditions.append("MERGE_" + after["mergeStateStatus"])
    if not checks:
        conditions.append("NO_CHECKS")
    else:
        for bucket, condition in (
            ("fail", "CHECKS_FAILED"), ("cancel", "CHECKS_CANCELLED"),
            ("pending", "CHECKS_PENDING"), ("skipping", "CHECKS_SKIPPED"),
        ):
            if bucket in buckets:
                conditions.append(condition)
        if buckets == {"pass"}:
            conditions.append("OBSERVED_CHECKS_PASSED")
    return result


def read_gh(arguments, allowed=(0,)):
    process = subprocess.run(
        ["gh", *arguments], capture_output=True, text=True, timeout=30,
    )
    if process.returncode not in allowed:
        raise ValueError(f"GitHub CLI read failed with exit {process.returncode}")
    try:
        return json.loads(process.stdout)
    except ValueError:
        raise ValueError("GitHub CLI returned no usable JSON; check access or CLI support") from None


def collect(repo, pr, expected_head):
    view_args = ["pr", "view", str(pr), "--repo", repo, "--json", VIEW_FIELDS]
    before = read_gh(view_args)
    validate_view(before)
    if before["headRefOid"] != expected_head:
        return classify(before, [], before, expected_head)
    if not isinstance(before.get("statusCheckRollup"), list):
        raise ValueError("Check rollup unavailable")
    if not before["statusCheckRollup"]:
        after = read_gh(view_args)
        result = classify(before, [], after, expected_head)
        if "STALE" not in result["conditions"] and after.get("statusCheckRollup") != []:
            raise ValueError("Checks changed while reading; refresh the snapshot")
        return result
    checks = read_gh(
        ["pr", "checks", str(pr), "--repo", repo, "--json", "name,state,bucket,link,workflow"],
        allowed=(0, 1, 8),
    )
    after = read_gh(view_args)
    return classify(before, checks, after, expected_head)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Explicit GitHub owner/repository")
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--expected-head", required=True, help="Full expected remote head SHA")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo) or args.pr < 1:
        parser.error("Use owner/repository and a positive PR number")
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        parser.error("Use the full expected head SHA")
    try:
        result = collect(args.repo, args.pr, args.expected_head)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"conditions": ["UNAVAILABLE"], "readiness": "NOT_ASSESSED", "reason": str(error)}))
        return 2
    print(json.dumps(result, indent=2))
    return 2 if "STALE" in result["conditions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

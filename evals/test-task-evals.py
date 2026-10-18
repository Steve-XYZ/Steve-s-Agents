#!/usr/bin/env python3
"""Exercise fixture outcomes and execution receipts without paid inference."""

import importlib.util
import py_compile
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


EVALS = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS))


def load(filename):
    spec = importlib.util.spec_from_file_location(filename, EVALS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load("run-task.py")
grader = load("grade-task.py")
fixtures = load("make-task-fixture.py")


class TaskTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="orders-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.task = self.root / "warehouse"
        self.record = self.root / "receipts"

    def prepare(self, case, **options):
        runner.run(case, self.task, self.record, prepare_only=True, **options)
        return self.task / "repo"

    def fix_currency(self, repo, wrong_default=False):
        path = repo / "inventory/cli.py"
        content = path.read_text().replace('report.add_argument("--warehouse")', 'report.add_argument("--warehouse")\n    report.add_argument("--currency")')
        currency = 'args.currency or options["currency"]' if wrong_default else 'args.currency or "USD"'
        content = content.replace('format_report(items, options["warehouse"])', 'format_report(items, options["warehouse"], ' + currency + ')')
        path.write_text(content)
        path = repo / "inventory/report.py"
        content = 'from inventory.rates import convert\n' + path.read_text()
        content = content.replace('def format_report(items, warehouse):', 'def format_report(items, warehouse, currency="USD"):')
        content = content.replace('{total_value(items):.2f} USD', '{convert(total_value(items), currency):.2f} {currency}')
        path.write_text(content)

    def fake_cli(self, mode="complete", usage=True):
        path = self.root / "codex local"
        path.write_text("#!" + sys.executable + "\n" + f"MODE = {mode!r}\nUSAGE = {usage!r}\n" + r'''
import json, os, pathlib, subprocess, sys, time
if sys.argv[1:] == ['--version']:
    if MODE == 'version-wait':
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
        pathlib.Path(__file__).with_name('version-child.pid').write_text(str(child.pid))
        time.sleep(60)
    print('codex-fixture 1.0')
    sys.exit(0)
repo = pathlib.Path(sys.argv[sys.argv.index('-C') + 1])
output = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])
output.parent.joinpath('argv.json').write_text(json.dumps(sys.argv))
if not (repo / '.git').exists() and '--skip-git-repo-check' not in sys.argv:
    print('Not inside a trusted directory', file=sys.stderr)
    sys.exit(1)
if MODE == 'blocked':
    print(json.dumps({'type': 'turn.failed', 'error': {'message': 'provider unavailable'}}))
    print('provider unavailable', file=sys.stderr)
    sys.exit(1)
if MODE == 'wait':
    child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
    output.parent.joinpath('child.pid').write_text(str(child.pid))
    output.parent.joinpath('ready').touch()
    time.sleep(60)
if MODE != 'workspace':
    path = repo / 'cli.py'
    path.write_text(path.read_text().replace('recieve', 'receive'))
output.write_text('Done; all checks pass.')
print(json.dumps({'type':'item.completed','item':{'type':'command_execution','exit_code':0}}))
event = {'type':'turn.completed'}
if USAGE:
    event['usage'] = {'input_tokens':100,'cached_input_tokens':20,'output_tokens':30}
print(json.dumps(event))
''')
        path.chmod(0o755)
        return str(path)

    def assert_stopped(self, pid):
        # A killed orphan can briefly be a zombie on Linux, but cannot keep running.
        stat = Path(f"/proc/{pid}/stat")
        if stat.exists():
            self.assertEqual(stat.read_text().split()[2], "Z")
        else:
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_control_keeps_answers_and_optional_guidance_out_of_task(self):
        repo = self.prepare("currency", control=True)
        self.assertEqual(list((self.task / "guidance").iterdir()), [])
        self.assertNotIn("Use $", (self.task / "prompt.txt").read_text())
        self.assertFalse((self.task / "receipt.json").exists())
        self.assertFalse(any("oracle" in str(path) for path in self.task.rglob("*")))
        self.assertEqual(grader.grade(self.record)["status"], "failed")
        self.assertTrue((repo / "tests/test_cli.py").exists())

    def test_currency_oracle_catches_green_suite_and_preserved_config_escape(self):
        repo = self.prepare("currency")
        self.fix_currency(repo, wrong_default=True)
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["checks"][1]["status"], "passed")
        self.assertIn("settings='EUR', args=[]", (self.record / "grade-oracle.txt").read_text())
        path = repo / "inventory/cli.py"
        path.write_text(path.read_text().replace('args.currency or options["currency"]', 'args.currency or "USD"'))
        result = grader.grade(self.record, self.record / "corrected.json")
        self.assertEqual(result["status"], "passed")
        self.assertEqual(json.loads((self.record / "grade.json").read_text())["status"], "failed")
        (repo / "inventory/__main__.py").write_text("raise RuntimeError('broken entry point')\n")
        self.assertEqual(grader.grade(self.record, self.record / "entry-point.json")["status"], "failed")

    def test_guidance_source_does_not_change_the_reviewed_application_diff(self):
        repo = self.prepare("discounts-clean")
        self.assertEqual(runner.git(repo, "diff", "--name-only", "HEAD^", "HEAD").splitlines(),
                         ["checkout/discounts.py", "tests/test_discounts.py"])
        self.assertTrue((self.task / "guidance/shared/code-review/SKILL.md").exists())
        (self.record / "response.txt").write_text("Approve, no findings.")
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "manual_required")
        self.assertTrue(result["manual_review"])
        (repo / "checkout/discounts.py").write_text("raise RuntimeError('edited')\n")
        self.assertEqual(grader.grade(self.record, self.record / "edited.json")["status"], "failed")

    def test_writing_drafts_need_manual_assessment_and_preserve_supplied_records(self):
        repo = self.prepare("merge-danger")
        (self.task / "drafts.json").write_text('{"help.pr": "Low. All checks pass."}')
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "manual_required")
        self.assertEqual(result["checks"][0]["status"], "passed")
        self.assertTrue(result["manual_review"])
        (repo / "RECORDS.json").write_text("[]")
        self.assertEqual(grader.grade(self.record, self.record / "edited.json")["status"], "failed")

    def test_existing_no_test_control_is_graded_by_cli_behavior(self):
        repo = self.prepare("simple")
        path = repo / "cli.py"
        path.write_text(path.read_text().replace("recieve", "receive"))
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["checks"][1]["status"], "not_applicable")

    def test_every_fixture_has_an_independent_check_or_is_read_only(self):
        cases = json.loads((EVALS / "task-fixtures.json").read_text())
        self.assertEqual(set(cases) - set(grader.CHECKS) - set(grader.READ_ONLY), set())

    def test_case_without_a_check_needs_review_instead_of_failing(self):
        repo = self.prepare("simple")
        path = repo / "cli.py"
        path.write_text(path.read_text().replace("recieve", "receive"))
        with mock.patch.dict(grader.CHECKS):
            del grader.CHECKS["simple"]
            result = grader.grade(self.record)
        self.assertEqual(result["status"], "manual_required")
        self.assertIn(grader.UNCHECKED, result["manual_review"])
        self.assertEqual([row["status"] for row in result["checks"]], ["not_applicable"])

    def test_test_runner_caches_are_not_review_edits(self):
        repo = self.prepare("discounts-clean")
        (repo / ".pytest_cache/v/cache").mkdir(parents=True)
        (repo / ".pytest_cache/v/cache/lastfailed").write_text("{}")
        self.assertEqual(grader.grade(self.record)["status"], "manual_required")

    def test_checks_ignore_bytecode_that_the_snapshot_excludes(self):
        repo = self.prepare("shape")
        corrected = self.root / "cli.py"
        corrected.write_text('import json\ndef format_results(rows):\n    return json.dumps(rows)\n')
        py_compile.compile(str(corrected), cfile=importlib.util.cache_from_source(str(repo / "cli.py")),
                           invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH, doraise=True)
        (repo / "test_isolated.py").write_text(f"""import subprocess, sys, unittest
class Isolated(unittest.TestCase):
    def test_nonempty(self):
        program = "import sys; sys.path.insert(0, {str(repo)!r}); from cli import format_results; assert format_results([]) == '[]'"
        subprocess.run([sys.executable, "-I", "-c", program], check=True)
""")
        result = grader.grade(self.record)
        self.assertEqual([row["status"] for row in result["checks"]], ["failed", "failed"])
        self.assertIn("ERROR: test_nonempty (test_isolated", (self.record / "grade-suite-0.txt").read_text())

    def test_bytecode_cleanup_leaves_git_metadata_alone(self):
        repo = self.prepare("discounts-clean")
        runner.git(repo, "branch", "__pycache__/saved")
        self.assertEqual(grader.grade(self.record)["status"], "manual_required")
        self.assertEqual(runner.git(repo, "branch", "--list", "__pycache__/saved"), "__pycache__/saved")

    def test_grade_writes_do_not_follow_a_planted_temporary_file(self):
        self.prepare("simple")
        unrelated = self.root / "unrelated.txt"
        unrelated.write_text("keep")
        (self.record / "grade.json.tmp").symlink_to(unrelated)
        grader.grade(self.record)
        self.assertEqual(unrelated.read_text(), "keep")
        self.assertFalse((self.record / "grade.json").is_symlink())

    def test_disposable_destinations_and_record_separation(self):
        for task, record in [(self.task, self.task / "records"), (self.record / "work", self.record),
                             (EVALS / "orders", self.record)]:
            with self.subTest(task=task), self.assertRaises(ValueError):
                runner.run("simple", task, record, prepare_only=True)
        self.assertFalse(self.task.exists())
        self.task.mkdir()
        with self.assertRaises(ValueError):
            runner.run("simple", self.task, self.record, prepare_only=True)
        self.assertFalse(self.record.exists())
        link = self.root / "existing-link"
        link.symlink_to(self.root / "not-created")
        with self.assertRaises(ValueError):
            runner.run("simple", link, self.record, prepare_only=True)
        self.assertFalse((self.root / "not-created").exists())

    def test_no_grade_can_be_written_into_the_candidate_catalog(self):
        self.prepare("simple")
        with self.assertRaises(ValueError):
            grader.grade(self.record, self.task / "grade.json")

    def test_native_adapter_captures_actual_usage_and_missing_identity_honestly(self):
        executable = self.fake_cli()
        runner.run("simple", self.task, self.record, model="chosen-model", effort="high", executable=executable)
        receipt = json.loads((self.record / "receipt.json").read_text())
        self.assertEqual(receipt["execution"]["status"], "completed")
        self.assertEqual(receipt["execution"]["usage"], dict(input_tokens=100, cached_input_tokens=20, output_tokens=30))
        self.assertIsNone(receipt["execution"]["resolved_model"])
        self.assertIsNone(receipt["execution"]["cost_usd"])
        self.assertIsNone(receipt["execution"]["tool_calls"])
        self.assertGreater(receipt["execution"]["elapsed_seconds"], 0)
        self.assertEqual(receipt["execution"]["completed_items_by_type"], {"command_execution": 1})
        self.assertEqual(json.loads((self.record / "grade.json").read_text())["status"], "passed")
        argv = json.loads((self.record / "argv.json").read_text())
        self.assertEqual(argv[argv.index("--model") + 1], "chosen-model")
        self.assertEqual(argv[argv.index("-c") + 1], 'model_reasoning_effort="high"')
        self.assertIn("--ignore-user-config", argv)
        self.assertNotIn("--skip-git-repo-check", argv)
        self.assertEqual(argv[-1], "-")

    def test_native_workspace_adapter_accepts_a_parent_outside_git(self):
        runner.run("workspace", self.task, self.record, model="chosen", effort="high",
                   executable=self.fake_cli("workspace"))
        receipt = json.loads((self.record / "receipt.json").read_text())
        self.assertEqual(receipt["execution"]["status"], "completed")
        self.assertIn("--skip-git-repo-check", receipt["execution"]["argv"])
        self.assertFalse((self.task / "repo/.git").exists())
        self.assertTrue((self.task / "repo/accounts/.git").is_dir())
        self.assertEqual(json.loads((self.record / "grade.json").read_text())["status"], "failed")

    def test_unavailable_provider_keeps_failure_output_without_grading_it_as_bad_code(self):
        runner.run("simple", self.task, self.record, model="chosen", effort="medium", executable=self.fake_cli("blocked"))
        receipt = json.loads((self.record / "receipt.json").read_text())
        self.assertEqual(receipt["execution"]["status"], "blocked")
        self.assertIsNone(receipt["execution"]["usage"])
        self.assertIn("provider unavailable", (self.record / "stderr.txt").read_text())
        self.assertFalse((self.record / "grade.json").exists())

    def test_absent_or_malformed_usage_is_not_zero_cost(self):
        path = self.root / "events.jsonl"
        for usage in [None, {}, {"input_tokens": True}, {"input_tokens": -1, "cached_input_tokens": 0, "output_tokens": 1}]:
            path.write_text(json.dumps({"type": "turn.completed", "usage": usage}) + "\n")
            self.assertIsNone(runner.stream_metadata(path)["usage"])
        path.write_text('{broken\n' + json.dumps({"type":"turn.completed","usage":{"input_tokens":1,"cached_input_tokens":0,"output_tokens":2}}) + '\n')
        self.assertIsNone(runner.stream_metadata(path)["usage"])
        self.assertEqual(runner.stream_metadata(path)["malformed_lines"], 1)

    def test_changed_prompt_or_catalog_invalidates_the_treatment(self):
        self.prepare("simple")
        path = self.task / "prompt.txt"
        original = path.read_text()
        path.write_text(original + "Do something else.")
        self.assertEqual(grader.grade(self.record)["status"], "stale")
        path.write_text(original)
        path = self.task / "guidance/shared/deliver-ticket/SKILL.md"
        path.write_text(path.read_text() + "\nChanged treatment.\n")
        self.assertEqual(grader.grade(self.record, self.record / "catalog.json")["status"], "stale")

    def test_validation_timeout_retains_partial_output_and_stops_children(self):
        output = self.root / "validation.txt"
        result = grader.check([sys.executable, "-u", "-c", "import time; print('started'); time.sleep(60)"],
                              self.root, output, timeout=0.1)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("started", output.read_text())

    def test_changed_untracked_source_or_receipt_invalidates_a_completed_grade(self):
        runner.run("simple", self.task, self.record, model="chosen", effort="medium", executable=self.fake_cli())
        (self.task / "repo/extra.py").write_text("new_state = True\n")
        self.assertEqual(grader.grade(self.record, self.record / "stale.json")["status"], "stale")
        (self.task / "repo/extra.py").unlink()
        (self.record / "response.txt").write_text("another response")
        self.assertEqual(grader.grade(self.record, self.record / "changed-response.json")["status"], "stale")

    def test_timeout_and_signal_cancel_kill_child_processes_and_preserve_receipts(self):
        executable = self.fake_cli("wait")
        for cancelled in (False, True):
            task, record = self.root / ("orders" if cancelled else "stock"), self.root / ("orders-log" if cancelled else "stock-log")
            command = [sys.executable, str(EVALS / "run-task.py"), "simple", "--task-dir", str(task),
                       "--record-dir", str(record), "--codex", executable, "--model", "chosen",
                       "--effort", "medium", "--timeout", "10" if cancelled else "0.5"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            self.addCleanup(lambda p=process: p.poll() is None and p.kill())
            deadline = time.monotonic() + 5
            while not (record / "ready").exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue((record / "ready").exists())
            child = int((record / "child.pid").read_text())
            if cancelled:
                process.send_signal(signal.SIGTERM)
            process.communicate(timeout=5)
            receipt = json.loads((record / "receipt.json").read_text())
            self.assertEqual(receipt["execution"]["status"], "cancelled" if cancelled else "timed_out")
            self.assertFalse((record / "grade.json").exists())
            self.assert_stopped(child)

    def test_version_probe_timeout_kills_child_processes(self):
        executable = self.fake_cli("version-wait")
        runner.run("simple", self.task, self.record, model="chosen", effort="medium", timeout=0.5, executable=executable)
        self.assertEqual(json.loads((self.record / "receipt.json").read_text())["execution"]["status"], "timed_out")
        self.assert_stopped(int((self.root / "version-child.pid").read_text()))

    def test_multiple_repositories_are_real_checkouts_with_one_shared_contract(self):
        repo = self.prepare("workspace")
        self.assertFalse((repo / ".git").exists())
        for name in ("accounts", "operations", "portal"):
            self.assertTrue((repo / name / ".git").is_dir())
        self.assertEqual(grader.grade(self.record)["status"], "failed")

    def test_dispatch_oracle_accepts_progress_but_rejects_work_added_in_the_tick(self):
        repo = self.prepare("dispatch")
        self.assertEqual(grader.grade(self.record)["status"], "failed")
        source = (repo / "dispatcher.py").read_text()
        source = source[:source.index("    def tick(self):")] + '''    def tick(self):
        index = 0
        for _ in range(len(self.pending)):
            item = self.pending[index]
            try:
                self.sender(item)
            except TemporaryFailure:
                index += 1
            else:
                self.pending.pop(index)
'''
        (repo / "dispatcher.py").write_text(source)
        self.assertEqual(grader.grade(self.record, self.record / "bounded.json")["status"], "passed")
        (repo / "dispatcher.py").write_text(source.replace("for _ in range(len(self.pending)):", "while index < len(self.pending):"))
        self.assertEqual(grader.grade(self.record, self.record / "unbounded.json")["status"], "failed")

    def test_dispatch_oracle_rejects_dropping_a_retained_retry_without_sending(self):
        repo = self.prepare("dispatch")
        (repo / "dispatcher.py").write_text('''class TemporaryFailure(Exception):
    pass
class Dispatcher:
    def __init__(self, sender):
        self.pending = []
        self.sender = sender
        self.already_failed = set()
    def enqueue(self, item):
        self.pending.append(item)
    def tick(self):
        for item in self.pending[:]:
            if item in self.already_failed:
                self.pending.remove(item)
                continue
            try:
                self.sender(item)
            except TemporaryFailure:
                self.already_failed.add(item)
            else:
                self.pending.remove(item)
''')
        result = grader.grade(self.record)
        self.assertEqual(result["checks"][1]["status"], "passed")
        self.assertEqual(result["status"], "failed")

    def test_quantity_oracle_rejects_fractional_negative_truncation(self):
        self.prepare("feedback")
        result = grader.grade(self.record)
        self.assertEqual(result["checks"][1]["status"], "passed")
        self.assertEqual(result["checks"][0]["status"], "failed")
        self.assertEqual(result["status"], "failed")

    def test_workspace_oracle_checks_consumers_not_only_the_named_service(self):
        repo = self.prepare("workspace")
        (repo / "accounts/policy.py").write_text('''def can_withdraw(account):
    state = account.get('withdrawal_state', 'enabled' if account.get('withdrawals_enabled') is True else 'disabled')
    return state == 'enabled' and not account.get('frozen', False)

def event(account):
    return {'account_id': account['id'], 'can_withdraw': can_withdraw(account)}
''')
        self.assertEqual(grader.grade(self.record)["status"], "failed")
        interpret = '''def label_and_permission(account):
    state = account.get('withdrawal_state', 'enabled' if account.get('withdrawals_enabled') is True else 'disabled')
    label = 'Pending review' if state == 'review' else 'Enabled' if state == 'enabled' else 'Disabled'
    return label, state == 'enabled' and not account.get('frozen', False)
'''
        (repo / "portal/view.py").write_text(interpret + '''
def withdrawal(account):
    label, permitted = label_and_permission(account)
    return {'label': label, 'button_enabled': permitted}
''')
        (repo / "operations/export.py").write_text(interpret + '''
import csv, io
def export_accounts(accounts):
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator='\\n')
    writer.writerow(['id', 'withdrawal', 'balance'])
    for account in accounts:
        writer.writerow([account['id'], label_and_permission(account)[0], account['balance']])
    return output.getvalue()
''')
        self.assertEqual(grader.grade(self.record, self.record / "all-readers.json")["status"], "passed")
        policy = repo / "accounts/policy.py"
        correct = policy.read_text()
        policy.write_text(correct.replace("'can_withdraw': can_withdraw(account)", "'can_withdraw': state_allows(account)")
                          .replace("def can_withdraw(account):", "def can_withdraw(account):\n    return bool(account.get('withdrawals_enabled'))\n\ndef state_allows(account):"))
        self.assertEqual(grader.grade(self.record, self.record / "unchanged-api.json")["status"], "failed")
        policy.write_text(correct.replace("return state ==", "return account.get('withdrawals_enabled') is True and state =="))
        self.assertEqual(grader.grade(self.record, self.record / "legacy-required.json")["status"], "failed")

    def test_remaining_delivery_oracles_accept_correct_public_behavior(self):
        corrections = {
            "shape": {"cli.py": 'import json\ndef format_results(rows):\n    return json.dumps(rows)\n'},
            "slices": {"exporter.py": 'from csv_writer import write_items\ndef export_items(items):\n    return write_items(items, sort_by="display_name")\n',
                       "items.py": 'def set_quantity(item, value):\n    if isinstance(value, (int, float)) and value < 0:\n        raise ValueError("negative")\n    value = int(value)\n    if value < 0:\n        raise ValueError("negative")\n    item["quantity"] = value\n    return item\n'},
        }
        for case, files in corrections.items():
            with self.subTest(case=case):
                task, record = self.root / case, self.root / (case + "-record")
                runner.run(case, task, record, prepare_only=True)
                self.assertEqual(grader.grade(record)["status"], "failed")
                for name, content in files.items():
                    (task / "repo" / name).write_text(content)
                self.assertEqual(grader.grade(record, record / "corrected.json")["status"], "passed")
        task, record = self.root / "parcel", self.root / "parcel-record"
        runner.run("parcel", task, record, prepare_only=True)
        self.assertEqual(grader.grade(record)["status"], "failed")
        path = task / "repo/shipping/rates.py"
        path.write_text(path.read_text().replace("weight_grams < limit", "weight_grams <= limit"))
        self.assertEqual(grader.grade(record, record / "corrected.json")["status"], "passed")

    def test_receipts_and_oracles_fail_closed_when_the_source_is_not_reproducible(self):
        repo = self.prepare("simple")
        path = repo / "cli.py"
        path.unlink()
        path.symlink_to(self.root / "outside.py")
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("symlink", result["reason"])

    def test_native_runs_need_explicit_settings_and_real_limits(self):
        for options in [{}, {"model": "chosen"}, {"model": "chosen", "effort": "high", "timeout": float("nan")},
                        {"model": "chosen", "effort": "high", "timeout": 0}]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                runner.run("simple", self.task, self.record, **options)
        self.assertFalse(self.task.exists())

    def test_source_changes_during_validation_do_not_receive_a_passing_receipt(self):
        repo = self.prepare("simple")
        path = repo / "cli.py"
        path.write_text(path.read_text().replace("recieve", "receive"))
        (repo / "test_rewrite.py").write_text('''import unittest
from pathlib import Path
class Rewrite(unittest.TestCase):
    def test_rewrite(self):
        Path('cli.py').write_text('raise RuntimeError("changed during tests")\\n')
''')
        result = grader.grade(self.record)
        self.assertEqual(result["status"], "stale")
        self.assertNotEqual(result["state"], result["post_check_state"])


if __name__ == "__main__":
    unittest.main()

"""Independent checks executed after a candidate finishes, outside its catalog."""

import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = None


def call(code, directory=None, data=None, import_root=None):
    directory = Path(directory or REPO)
    program = "import sys; sys.path.insert(0, " + repr(str(import_root or directory)) + "); " + code
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", program], cwd=directory,
        input=data, capture_output=True, text=True, timeout=10,
    )
    if result.returncode:
        raise AssertionError(f"exit {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout


class Simple(unittest.TestCase):
    def test_help_and_unchanged_invocations(self):
        for args, expected in [([], ""), (["ignored"], ""), (["--help"], "Use this command to receive local events.\n")]:
            result = subprocess.run([sys.executable, "-B", "cli.py", *args], cwd=REPO, capture_output=True, text=True, timeout=10)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, expected, ""))


class Currency(unittest.TestCase):
    def report(self, args, settings):
        with tempfile.TemporaryDirectory(prefix="stock-") as directory:
            Path(directory, "inventory.toml").write_text('[inventory]\ncurrency = "' + settings + '"\n')
            code = "import runpy; sys.argv = " + repr(["inventory", "report", "--data", str(REPO / "data/items.json"), *args])
            code += "; runpy.run_module('inventory', run_name='__main__', alter_sys=True)"
            return call(code, directory=directory, import_root=REPO)

    def test_explicit_currency_and_preserved_default(self):
        for settings in ("USD", "EUR"):
            for args, total in [([], "81.00 USD"), (["--currency", "USD"], "81.00 USD"), (["--currency", "EUR"], "74.52 EUR")]:
                with self.subTest(settings=settings, args=args):
                    output = self.report(args, settings)
                    self.assertEqual(output.splitlines(), ["Warehouse: main", "anchor: 2", "bolt: 100", "hinge: 10", "Total: " + total])

    def test_default_csv_contract(self):
        output = call("import runpy; sys.argv = ['inventory', 'export']; runpy.run_module('inventory', run_name='__main__', alter_sys=True)")
        self.assertEqual(output, "name,quantity,price_usd\nanchor,2,12.50\nbolt,100,0.25\nhinge,10,3.10\n")


class Shape(unittest.TestCase):
    def test_same_json_schema_for_empty_and_nonempty(self):
        output = call("import json; from cli import format_results; print(json.dumps([format_results([]), format_results(['one'])]))")
        self.assertEqual(json.loads(output), ["[]", '["one"]'])


class Slices(unittest.TestCase):
    def test_rejection_before_mutation_and_preserved_conversion(self):
        call(r"""
from items import set_quantity
for value in (-1, '-2', 'invalid'):
    item = {'display_name': 'x', 'quantity': 3}
    try:
        set_quantity(item, value)
    except ValueError:
        pass
    else:
        raise AssertionError(f'accepted {value!r}')
    assert item['quantity'] == 3
for value in (0, '0', '3'):
    item = {'display_name': 'x', 'quantity': 3}
    assert set_quantity(item, value) is item
    assert item['quantity'] == int(value)
""")

    def test_csv_sorting_escaping_and_other_report(self):
        call(r"""
import csv, io
from exporter import export_items
from other_report import report
rows = [{'display_name': 'Z', 'quantity': 3}, {'display_name': 'A, "B"\nC', 'quantity': 2}, {'display_name': 'A, "B"\nC', 'quantity': 1}]
before = [row.copy() for row in rows]
for source in (rows, iter(rows)):
    data = list(csv.DictReader(io.StringIO(export_items(source))))
    assert data == [{'display_name': rows[i]['display_name'], 'quantity': str(rows[i]['quantity'])} for i in (1, 2, 0)]
assert rows == before
assert export_items(iter([])) == 'display_name,quantity\n'
assert list(csv.DictReader(io.StringIO(report(rows))))[0]['display_name'] == 'Z'
""")


class Parcel(unittest.TestCase):
    def test_every_upper_limit_and_surcharge(self):
        call(r"""
from shipping.rates import shipping_cents
for grams, base in ((1, 450), (1000, 450), (1001, 700), (2000, 700), (2001, 1100), (5000, 1100)):
    for zone, surcharge in (('domestic', 0), ('eu', 300), ('world', 900)):
        assert shipping_cents(grams, zone) == base + surcharge, (grams, zone)
for grams in (0, -1, 5001):
    try:
        shipping_cents(grams)
    except ValueError:
        pass
    else:
        raise AssertionError(grams)
""")


class Dispatch(unittest.TestCase):
    def test_progress_retention_and_no_duplicate_send(self):
        call(r"""
from dispatcher import Dispatcher, TemporaryFailure
for failures in ({'a'}, {'a', 'b'}, set()):
    calls = []
    def send(item):
        calls.append(item)
        if item in failures:
            raise TemporaryFailure()
    dispatcher = Dispatcher(send)
    for item in 'abcdef':
        dispatcher.enqueue(item)
    dispatcher.tick()
    assert sorted(calls) == list('abcdef'), calls
    assert set(dispatcher.pending) == failures
    failures.clear()
    dispatcher.tick()
    assert dispatcher.pending == []
    before = list(calls)
    dispatcher.tick()
    assert calls == before
""")

    def test_new_work_waits_and_unexpected_error_preserves_work(self):
        call(r"""
from dispatcher import Dispatcher
calls = []
def send(item):
    calls.append(item)
    if item == 'a':
        dispatcher.enqueue('new')
dispatcher = Dispatcher(send)
dispatcher.enqueue('a')
dispatcher.tick()
assert calls == ['a']
dispatcher.tick()
assert calls == ['a', 'new']
def broken(item):
    raise RuntimeError('permanent')
dispatcher = Dispatcher(broken)
dispatcher.enqueue('a')
dispatcher.enqueue('b')
try:
    dispatcher.tick()
except RuntimeError:
    pass
else:
    raise AssertionError('exception swallowed')
assert dispatcher.pending == ['a', 'b']
""")


class Workspace(unittest.TestCase):
    def test_same_policy_across_all_repositories(self):
        cases = []
        expected = []
        for state, label, enabled in [('enabled', 'Enabled', True), ('disabled', 'Disabled', False), ('review', 'Pending review', False), (None, None, False), ('unknown', None, False)]:
            for frozen in (False, True):
                cases.append(dict(id="a-123", balance=1234, withdrawals_enabled=True, withdrawal_state=state, frozen=frozen))
                expected.append((label, enabled and not frozen))
        for legacy in (False, True):
            cases.append(dict(id="legacy", balance=0, withdrawals_enabled=legacy))
            expected.append(('Enabled' if legacy else 'Disabled', legacy))
        payload = json.dumps(cases)
        events = json.loads(call("import json; from policy import event; print(json.dumps([event(x) for x in json.load(sys.stdin)]))", REPO / "accounts", payload))
        views = json.loads(call("import json; from view import withdrawal; print(json.dumps([withdrawal(x) for x in json.load(sys.stdin)]))", REPO / "portal", payload))
        exported = list(csv.DictReader(io.StringIO(call("import json; from export import export_accounts; print(export_accounts(json.load(sys.stdin)), end='')", REPO / "operations", payload))))
        for account, (label, enabled), event, view, row in zip(cases, expected, events, views, exported):
            with self.subTest(account=account):
                self.assertEqual(event, dict(account_id=account['id'], can_withdraw=enabled))
                self.assertIs(event['can_withdraw'], enabled)
                self.assertIs(view['button_enabled'], enabled)
                self.assertEqual((row['id'], row['balance']), (account['id'], str(account['balance'])))
                if label is not None:
                    self.assertEqual((view['label'], row['withdrawal']), (label, label))
        self.assertEqual((len(events), len(views), len(exported)), (len(cases),) * 3)


CHECKS = {"simple": Simple, "currency": Currency, "shape": Shape, "slices": Slices,
          "feedback": Slices, "parcel": Parcel, "dispatch": Dispatch, "workspace": Workspace}


if __name__ == "__main__":
    case, path = sys.argv[1:]
    REPO = Path(path).resolve()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CHECKS[case])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

#!/usr/bin/env python3
"""Recheck directory delivery artifacts against original tests and independent contracts."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def run(repo, code):
    result = subprocess.run(['python3', '-c', code], cwd=repo, text=True,
                            capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    return {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def check(repo, original_tests):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()
    original = git('rev-list', '--max-parents=0', 'HEAD')
    original_check = "import unittest\n" + original_tests + "\nraise SystemExit(not unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DirectoryTest)).wasSuccessful())\n"
    contracts = '''from unittest.mock import patch
from directory.export import export_directory, labels_for, read_v1, display_label
from directory.source import Source
from directory.order import keys_in_order
from consumer.import_directory import import_directory
import directory.export as exporter
expected = "key,label,tags\\r\\na,ALPHA,\\r\\nb,BETA,\\r\\n"
assert export_directory() == expected
assert export_directory(Source()) == expected
with patch.object(exporter.Source, "records", return_value=[{"key":"q", "label":"Queue"}]):
    assert export_directory() == "key,label,tags\\r\\nq,QUEUE,\\r\\n"
first = labels_for(["one"])
assert first == ["one"]
assert labels_for(["two"]) == ["two"]
assert first == ["one"]
buffer = ["earlier"]
assert labels_for(["now"], buffer) == ["earlier", "now"]
assert buffer == ["earlier", "now"]
assert read_v1({"key":"q", "name":"Queue"}) == {"key":"q", "label":"Queue"}
assert display_label("Alpha") == "ALPHA"
assert keys_in_order(Source().records()) == ["a", "b"]
for _ in range(2):
    assert export_directory(tags=("one",)) == "key,label,tags\\r\\na,ALPHA,one\\r\\nb,BETA,one\\r\\n"
assert import_directory(expected)[0] == {"key":"a", "label":"ALPHA", "tags":""}
'''
    suite = run(repo, "import unittest; raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests')).wasSuccessful())")
    return {'head_sha': git('rev-parse', 'HEAD'), 'tree_sha': git('rev-parse', 'HEAD^{tree}'),
            'tracked_diff': git('diff', 'HEAD'), 'original_tests': run(repo, original_check),
            'contracts': run(repo, contracts), 'submitted_suite': suite,
            'clean_module_diff': git('diff', original, 'HEAD', '--', 'directory/order.py')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('repos', type=Path, nargs='+')
    args = parser.parse_args()
    tests = json.loads(args.fixtures.read_text())['directory']['files']['tests/test_directory.py']
    results = {str(repo.resolve()): check(repo.resolve(), tests) for repo in args.repos}
    args.output.write_text(json.dumps(results, indent=2) + '\n')
    for repo, result in results.items():
        print(Path(repo).parent.name, {key: result[key]['exit_code'] for key in ('original_tests', 'contracts', 'submitted_suite')})

"""Build the self-contained offline viewer (AquaGrid_Demo.html) from real engine output.

Runs every scenario through the Python engine, runs the unit-test suite, and injects
both into demo_template.html. The HTML replays these precomputed results; for a live
engine use `python3 demo.py` or `streamlit run app.py`.

    python3 export_demo.py
"""
import io
import json
import unittest
from datetime import date
from pathlib import Path

from aquagrid import SCENARIOS, run_scenario

ROOT = Path(__file__).parent
OUTPUT = ROOT / 'outputs'


def run_tests() -> dict:
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    failed = len(result.failures) + len(result.errors)
    return {'run': result.testsRun, 'failed': failed, 'passed': result.testsRun - failed}


def main() -> None:
    snapshots = {k: run_scenario(k) for k in SCENARIOS}
    OUTPUT.mkdir(exist_ok=True)
    for key, result in snapshots.items():
        (OUTPUT / f'{key}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')

    tests = run_tests()
    meta = {
        'tests': tests,
        'generated': date.today().isoformat(),
        'specs': {k: {'broken_pipes': v['broken_pipes'],
                      'supply_multiplier': v['supply_multiplier'],
                      'demand_multiplier': v['demand_multiplier']}
                  for k, v in SCENARIOS.items()},
    }
    payload = json.dumps({'snapshots': snapshots, 'meta': meta}, separators=(',', ':'))
    payload = payload.replace('</', '<\\/')  # never close the <script> tag early
    template = (ROOT / 'demo_template.html').read_text(encoding='utf-8')
    (ROOT / 'AquaGrid_Demo.html').write_text(template.replace('__DATA__', payload), encoding='utf-8')
    print(f"Exported AquaGrid_Demo.html and {len(snapshots)} JSON scenario results "
          f"(tests: {tests['passed']}/{tests['run']} passing)")


if __name__ == '__main__':
    main()

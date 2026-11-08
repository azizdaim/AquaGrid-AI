"""Run: python demo.py --scenario pipe_failure --json outputs/pipe_failure.json"""
import argparse
import json
from pathlib import Path
from aquagrid import SCENARIOS, run_scenario


def print_summary(result):
    m = result['metrics']
    print('\n' + '=' * 65)
    print(f"AQUAGRID AI  |  {result['scenario'].upper()}")
    print('=' * 65)
    print(result['description'])
    print(f"Water supplied: {m['delivered']}/{m['total_demand']} units "
          f"({m['satisfaction_pct']}%)")
    print(f"Hospital coverage: {m['hospital_satisfaction_pct']}%  |  "
          f"Failed pipes: {m['failed_pipes']}")
    print(f"{'District':<18} {'Demand':>9} {'Received':>10} {'Coverage':>10}")
    print('-' * 52)
    for d in result['districts']:
        print(f"{d['label']:<18} {d['demand']:>9} {d['delivered']:>10} "
              f"{d['satisfaction_pct']:>9}%")
    print('\nAgent decisions (first 5 transfers):')
    for line in result['decision_log'][1:6]:
        print(' -', line)
    print('\nPrototype: synthetic, single-step simulation; not real-world water control.')


def main():
    parser = argparse.ArgumentParser(description='AquaGrid AI milestone prototype')
    parser.add_argument('--scenario', choices=list(SCENARIOS), default='normal')
    parser.add_argument('--all', action='store_true', help='Run all 5 scenarios')
    parser.add_argument('--json', type=Path, help='Export JSON (single scenario only)')
    args = parser.parse_args()
    results = {k: run_scenario(k) for k in (SCENARIOS if args.all else [args.scenario])}
    for result in results.values():
        print_summary(result)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(next(iter(results.values())), indent=2), encoding='utf-8')
        print('Saved:', args.json)


if __name__ == '__main__':
    main()

"""Run: python -m unittest discover -s tests -v"""
import unittest
from aquagrid.model import make_city
from aquagrid.agents import NetworkAgent
from aquagrid.simulator import run_scenario
from aquagrid.scenarios import SCENARIOS


class AquaGridEngineTests(unittest.TestCase):
    def test_astar_finds_main_hospital_path(self):
        graph = make_city()
        route, cost = NetworkAgent(graph).astar('R_N', 'D_H')
        self.assertEqual(route, ['R_N', 'J_C', 'D_H'])
        self.assertEqual(cost, 3)

    def test_astar_reroutes_after_pipe_failure(self):
        graph = make_city()
        graph.break_pipe('J_C', 'D_H')
        route, _ = NetworkAgent(graph).astar('R_S', 'D_H')
        self.assertEqual(route, ['R_S', 'J_E', 'D_H'])

    def test_normal_demand_is_met(self):
        s = run_scenario('normal')
        self.assertEqual(s['metrics']['delivered'], s['metrics']['total_demand'])
        self.assertEqual(s['metrics']['hospital_satisfaction_pct'], 100.0)

    def test_failure_respects_backup_hospital_capacity(self):
        s = run_scenario('pipe_failure')
        h = next(d for d in s['districts'] if d['critical'])
        self.assertLessEqual(h['delivered'], 110)
        self.assertGreater(h['delivered'], 0)
        self.assertTrue(any('J_E' in transfer['path'] and
                            transfer['destination'] == 'D_H'
                            for transfer in s['transfers']))

    def test_drought_preserves_critical_supply(self):
        s = run_scenario('drought')
        self.assertEqual(s['metrics']['hospital_satisfaction_pct'], 100.0)
        self.assertGreater(s['metrics']['unmet'], 0)

    def test_all_scenarios_conserve_water_and_capacity(self):
        for name in SCENARIOS:
            with self.subTest(scenario=name):
                s = run_scenario(name)
                m = s['metrics']
                self.assertEqual(m['delivered'] + m['unmet'], m['total_demand'])
                self.assertEqual(m['delivered'], sum(x['released'] for x in s['reservoirs']))
                self.assertTrue(all(p['used'] <= p['capacity'] for p in s['pipes']))
                self.assertTrue(all(d['delivered'] <= d['demand'] for d in s['districts']))
                self.assertTrue(all(p['used'] == 0 for p in s['pipes'] if not p['active']))

    def test_deterministic_results(self):
        self.assertEqual(run_scenario('combined'), run_scenario('combined'))


if __name__ == '__main__':
    unittest.main()

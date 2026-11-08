"""One-timestep allocation engine with transparent outputs and conservation checks."""
from .agents import CrisisCoordinatorAgent, DistrictAgent, NetworkAgent, ReservoirAgent
from .model import make_city
from .scenarios import SCENARIOS


def run_scenario(key: str = 'normal') -> dict:
    if key not in SCENARIOS:
        raise ValueError(f'Unknown scenario {key}; choose from {list(SCENARIOS)}')
    spec = SCENARIOS[key]
    network = make_city()
    for a, b in spec['broken_pipes']:
        assert network.break_pipe(a, b), f'Configured failed pipe not found: {a}-{b}'
    districts = {
        node.id: DistrictAgent(node, round(node.demand * spec['demand_multiplier']))
        for node in network.nodes.values() if node.kind == 'district'
    }
    reservoirs = {
        node.id: ReservoirAgent(node, round(node.supply * spec['supply_multiplier']))
        for node in network.nodes.values() if node.kind == 'reservoir'
    }
    coordinator = CrisisCoordinatorAgent(NetworkAgent(network), reservoirs)
    coordinator.coordinate(districts)

    total_demand = sum(d.demand for d in districts.values())
    delivered = sum(d.received for d in districts.values())
    available = sum(round(n.supply * spec['supply_multiplier'])
                    for n in network.nodes.values() if n.kind == 'reservoir')
    assert sum(r.released for r in reservoirs.values()) == delivered
    assert sum(r.available for r in reservoirs.values()) + delivered == available
    assert all(p.used <= p.capacity for p in network.pipes)
    assert all(d.received <= d.demand for d in districts.values())

    district_data = []
    for name, d in districts.items():
        district_data.append({
            'id': name, 'label': d.district.label,
            'demand': d.demand, 'delivered': d.received,
            'satisfaction_pct': round(100 * d.received / d.demand, 1),
            'unmet': d.demand - d.received,
            'critical': d.district.critical,
            'priority': d.district.priority,
        })
    all_ratios = [d['delivered'] / d['demand'] for d in district_data]
    return {
        'key': key, 'scenario': spec['label'], 'description': spec['description'],
        'metrics': {
            'total_supply': available, 'total_demand': total_demand,
            'delivered': delivered, 'unmet': total_demand - delivered,
            'satisfaction_pct': round(100 * delivered / total_demand, 1),
            'min_district_satisfaction_pct': round(100 * min(all_ratios), 1),
            'hospital_satisfaction_pct': next(d['satisfaction_pct'] for d in district_data if d['critical']),
            'transfers': len(coordinator.transfers),
            'failed_pipes': len(spec['broken_pipes']),
        },
        'districts': district_data,
        'reservoirs': [
            {'id': r.id, 'label': network.nodes[r.id].label,
             'initial': r.available + r.released, 'remaining': r.available,
             'released': r.released}
            for r in reservoirs.values()
        ],
        'nodes': [
            {'id': n.id, 'label': n.label, 'kind': n.kind,
             'x': n.x, 'y': n.y} for n in network.nodes.values()
        ],
        'pipes': [
            {'a': p.a, 'b': p.b, 'capacity': p.capacity,
             'used': p.used, 'active': p.active, 'cost': p.cost}
            for p in network.pipes
        ],
        'transfers': coordinator.transfers,
        'decision_log': coordinator.decision_log,
        'limitations': [
            'One allocation timestep only; no pressure, time-delay or fluid dynamics.',
            'Synthetic graph and water units, not real city infrastructure data.',
            'Priority-first round-robin is a heuristic, not an optimal policy.',
            'No probabilistic sensor model or rigorous baseline comparison yet.',
        ],
    }

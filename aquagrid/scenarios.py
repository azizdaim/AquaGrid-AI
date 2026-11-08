"""Scenario definitions are artificial teaching inputs."""
SCENARIOS = {
    'normal': {
        'label': 'Normal Operations',
        'description': 'All pipes operational; reservoirs have normal supply.',
        'broken_pipes': [], 'supply_multiplier': 1, 'demand_multiplier': 1,
    },
    'pipe_failure': {
        'label': 'Hospital Main Pipe Failure',
        'description': 'The main hospital pipe is disabled. Agents seek an alternative route.',
        'broken_pipes': [('J_C', 'D_H')],
        'supply_multiplier': 1, 'demand_multiplier': 1,
    },
    'drought': {
        'label': 'Severe Water Shortage',
        'description': 'Reservoir supply falls to 65%; coordinator prioritizes the hospital.',
        'broken_pipes': [], 'supply_multiplier': .65, 'demand_multiplier': 1,
    },
    'demand_spike': {
        'label': 'Citywide Demand Surge',
        'description': 'Demand increases 40% across districts.',
        'broken_pipes': [], 'supply_multiplier': 1, 'demand_multiplier': 1.4,
    },
    'combined': {
        'label': 'Combined Crisis',
        'description': 'Supply shortage, rising demand, and a hospital pipeline failure.',
        'broken_pipes': [('J_C', 'D_H')],
        'supply_multiplier': .65, 'demand_multiplier': 1.4,
    },
}

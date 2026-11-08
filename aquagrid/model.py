"""Small synthetic city. Units represent simulated water volumes per time step.

This is intentionally NOT a hydraulic/pressure model, and all input values are
invented for teaching and experimentation, not sourced from a real city.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    kind: str  # reservoir, junction, district
    x: float
    y: float
    demand: int = 0
    priority: int = 0
    critical: bool = False
    supply: int = 0


@dataclass
class Pipe:
    a: str
    b: str
    capacity: int
    cost: float
    active: bool = True
    used: int = 0

    @property
    def remaining(self) -> int:
        return self.capacity - self.used if self.active else 0

    def connects(self, a: str, b: str) -> bool:
        return (self.a == a and self.b == b) or (self.a == b and self.b == a)


class WaterNetwork:
    def __init__(self, nodes: List[Node], pipes: List[Pipe]):
        self.nodes: Dict[str, Node] = {n.id: n for n in nodes}
        self.pipes = pipes
        self.neighbors: Dict[str, List[Tuple[str, Pipe]]] = {k: [] for k in self.nodes}
        for p in pipes:
            assert p.a in self.nodes and p.b in self.nodes
            assert p.capacity > 0 and p.cost >= 0
            self.neighbors[p.a].append((p.b, p))
            self.neighbors[p.b].append((p.a, p))
        # A* heuristic is admissible: minimum cost per geometric distance.
        self.cost_per_distance = min(
            (p.cost / math.dist((self.nodes[p.a].x, self.nodes[p.a].y),
                                (self.nodes[p.b].x, self.nodes[p.b].y))
             for p in pipes if math.dist((self.nodes[p.a].x, self.nodes[p.a].y),
                                         (self.nodes[p.b].x, self.nodes[p.b].y)) > 0),
            default=0.0,
        )

    def heuristic(self, current: str, goal: str) -> float:
        a, b = self.nodes[current], self.nodes[goal]
        return math.dist((a.x, a.y), (b.x, b.y)) * self.cost_per_distance

    def get_pipe(self, a: str, b: str) -> Pipe:
        for nxt, pipe in self.neighbors[a]:
            if nxt == b:
                return pipe
        raise KeyError(f"No pipe exists between {a} and {b}")

    def break_pipe(self, a: str, b: str) -> bool:
        for pipe in self.pipes:
            if pipe.connects(a, b):
                pipe.active = False
                return True
        return False

    def path_capacity(self, path: List[str]) -> int:
        return min((self.get_pipe(a, b).remaining for a, b in zip(path, path[1:])), default=0)

    def move_water(self, path: List[str], volume: int) -> None:
        if volume <= 0 or len(path) < 2 or volume > self.path_capacity(path):
            raise ValueError('Invalid volume or insufficient pipeline capacity')
        for a, b in zip(path, path[1:]):
            self.get_pipe(a, b).used += volume


def make_city() -> WaterNetwork:
    nodes = [
        Node('R_N', 'North Reservoir', 'reservoir', 9, 82, supply=770),
        Node('R_S', 'South Reservoir', 'reservoir', 10, 18, supply=550),
        Node('J_W', 'West Junction', 'junction', 35, 80),
        Node('J_C', 'Central Junction', 'junction', 45, 48),
        Node('J_E', 'East Junction', 'junction', 35, 15),
        Node('D_W', 'West', 'district', 74, 91, demand=170, priority=2),
        Node('D_H', 'Hospital', 'district', 85, 73, demand=180, priority=10, critical=True),
        Node('D_C', 'Central', 'district', 84, 55, demand=230, priority=4),
        Node('D_U', 'University', 'district', 83, 40, demand=150, priority=5),
        Node('D_E', 'East', 'district', 82, 21, demand=200, priority=3),
        Node('D_I', 'Industrial', 'district', 70, 5, demand=170, priority=1),
    ]
    # Bidirectional throughput limits, cost weights; water flows are recorded
    # per simulation step and do not represent real hydraulic constraints.
    pipe_data = [
        ('R_N', 'J_C', 650, 2), ('R_N', 'J_W', 280, 1),
        ('R_S', 'J_E', 520, 2), ('R_S', 'J_C', 300, 3),
        ('J_C', 'J_W', 230, 2), ('J_C', 'J_E', 300, 2),
        ('J_W', 'J_E', 120, 5), ('J_W', 'D_W', 220, 1),
        ('J_C', 'D_H', 240, 1), ('J_E', 'D_H', 110, 4),
        ('J_C', 'D_C', 270, 1), ('J_W', 'D_C', 120, 3),
        ('J_C', 'D_U', 210, 2), ('J_E', 'D_U', 120, 4),
        ('J_E', 'D_E', 280, 1), ('J_E', 'D_I', 270, 2),
    ]
    return WaterNetwork(nodes, [Pipe(a, b, cap, cost) for a, b, cap, cost in pipe_data])

"""Explicit message exchange between four deliberative/reactive agent roles."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import heapq
from .model import WaterNetwork


@dataclass(frozen=True)
class WaterRequest:
    district: str
    amount: int
    priority: int
    critical: bool


@dataclass(frozen=True)
class WaterOffer:
    reservoir: str
    available: int


@dataclass(frozen=True)
class RouteProposal:
    reservoir: str
    district: str
    path: Tuple[str, ...]
    cost: float
    capacity: int


class DistrictAgent:
    def __init__(self, district, demand):
        self.district = district
        self.demand = demand
        self.received = 0

    def request(self) -> WaterRequest:
        return WaterRequest(self.district.id, self.demand,
                            self.district.priority, self.district.critical)


class ReservoirAgent:
    def __init__(self, reservoir, amount):
        self.id = reservoir.id
        self.available = amount
        self.released = 0

    def offer(self) -> WaterOffer:
        return WaterOffer(self.id, self.available)

    def release(self, amount: int) -> None:
        if amount <= 0 or amount > self.available:
            raise ValueError('Cannot release more than current supply')
        self.available -= amount
        self.released += amount


class NetworkAgent:
    def __init__(self, network: WaterNetwork):
        self.network = network

    def astar(self, start: str, goal: str) -> Optional[Tuple[List[str], float]]:
        """A* shortest available path with an admissible geometric heuristic.

        A pipe with zero remaining capacity, or an inactive pipe, is impassable.
        """
        queue = [(self.network.heuristic(start, goal), 0.0, start)]
        best_cost = {start: 0.0}
        previous = {}
        while queue:
            _, cost, current = heapq.heappop(queue)
            if cost > best_cost[current] + 1e-9:
                continue
            if current == goal:
                path = [current]
                while path[-1] != start:
                    path.append(previous[path[-1]])
                return list(reversed(path)), cost
            for neighbor, pipe in self.network.neighbors[current]:
                if pipe.remaining <= 0:
                    continue
                new_cost = cost + pipe.cost
                if new_cost < best_cost.get(neighbor, float('inf')) - 1e-9:
                    best_cost[neighbor] = new_cost
                    previous[neighbor] = current
                    heapq.heappush(queue, (
                        new_cost + self.network.heuristic(neighbor, goal),
                        new_cost, neighbor,
                    ))
        return None

    def propose(self, district: str, offers: List[WaterOffer]) -> Optional[RouteProposal]:
        best: Optional[RouteProposal] = None
        for offer in offers:
            if offer.available <= 0:
                continue
            found = self.astar(offer.reservoir, district)
            if not found:
                continue
            path, cost = found
            cap = min(offer.available, self.network.path_capacity(path))
            if cap <= 0:
                continue
            proposed = RouteProposal(offer.reservoir, district, tuple(path), cost, cap)
            if best is None or (proposed.cost, -proposed.capacity, proposed.reservoir) < (best.cost, -best.capacity, best.reservoir):
                best = proposed
        return best

    def dispatch(self, path: Tuple[str, ...], amount: int):
        self.network.move_water(list(path), amount)


class CrisisCoordinatorAgent:
    """Critical-first, then fair-share round-robin; not globally optimal."""
    def __init__(self, network_agent: NetworkAgent,
                 reservoirs: Dict[str, ReservoirAgent], chunk_size: int = 20):
        self.network_agent = network_agent
        self.reservoirs = reservoirs
        self.chunk_size = chunk_size
        self.transfers: List[dict] = []
        self.decision_log: List[str] = []

    def allocate(self, request: WaterRequest, agents: Dict[str, DistrictAgent]) -> bool:
        district = agents[request.district]
        remaining = district.demand - district.received
        if remaining <= 0:
            return False
        offers = [r.offer() for r in self.reservoirs.values()]
        proposal = self.network_agent.propose(request.district, offers)
        if not proposal:
            return False
        volume = min(self.chunk_size, remaining, proposal.capacity)
        if volume <= 0:
            return False
        self.reservoirs[proposal.reservoir].release(volume)
        self.network_agent.dispatch(proposal.path, volume)
        district.received += volume
        self.transfers.append({
            'source': proposal.reservoir,
            'destination': request.district,
            'units': volume,
            'path': list(proposal.path),
            'path_cost': proposal.cost,
        })
        self.decision_log.append(
            f"Coordinator assigned {volume} units to {request.district} via "
            f"{proposal.reservoir}: {' → '.join(proposal.path)}"
        )
        return True

    def coordinate(self, districts: Dict[str, DistrictAgent]) -> None:
        requests = [d.request() for d in districts.values()]
        critical = sorted((r for r in requests if r.critical),
                          key=lambda r: (-r.priority, r.district))
        others = sorted((r for r in requests if not r.critical),
                        key=lambda r: (-r.priority, r.district))
        self.decision_log.append(
            'District agents broadcast demands; reservoir agents broadcast supply offers.'
        )
        # Critical districts go first; each request receives several small transfers.
        for request in critical:
            while districts[request.district].received < request.amount:
                if not self.allocate(request, districts):
                    break
        # Round-robin iterations reduce starvation under supply shortages.
        while True:
            made_progress = False
            for request in others:
                made_progress = self.allocate(request, districts) or made_progress
            if not made_progress:
                break
        self.decision_log.append('No more feasible requests; allocation cycle complete.')

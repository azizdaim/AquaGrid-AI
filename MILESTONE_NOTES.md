# Milestone 01: Water-Network Simulation Prototype

**Stage:** Working exploratory prototype, not a completed final project.

## Completed and independently verified
- A synthetic water network with **2 reservoirs, 6 districts, 3 junctions, 16 pipes**.
- Four role-specific agent classes, with requests, offers, route proposals and coordination.
- A* route search that avoids failed or exhausted pipes.
- Priority-first hospital allocation followed by round-robin for other districts.
- Five configurable crisis scenarios: normal, main-pipe break, shortage, demand surge, combined crisis.
- An offline showcase page, command-line simulation and 7 passing unit tests.

## Demo script: 60-90 seconds

Open `AquaGrid_Demo.html` (full screen). Keys `1`–`5` switch scenarios; each switch auto-plays the allocation.

1. **Show the network** (key `1`): "This is a fictional city, not a physical hydraulic model: two reservoirs, three junctions, six districts and capacity-limited pipes. Ring around each district = share of its demand met."
2. **Explain the AI**: "District agents request water, reservoir agents offer supply, the network agent finds routes using A*, and the coordinator serves the hospital first and then the other districts round-robin. Each pulse on the map is one 20-unit dispatch." Point to the agent diagram near the bottom.
3. **Hospital pipe failure** (key `2`): "The direct pipe is marked failed. Watch the first dispatches: A* reroutes South Reservoir → East Junction → Hospital." Click the Hospital to show the route inspector.
4. **Show the measured output**: "Total delivered falls from 100% to 93.6%. The hospital gets 110/180 because the backup pipe (shown violet, at capacity) carries at most 110 units. The model respects that limit." Point to the Key finding panel.
5. **Stress test** (key `5`): "Combined crisis: 55.7% total, but round-robin spreads the shortfall instead of cutting one district off completely." Point to the comparison chart.
6. **End with next milestone**: the bottom panels list what is delivered, what is next (baselines, multi-timestep, negotiation) and the limitations.

## What is not done
- Multi-step stateful simulation, physical water pressure, sensor noise/Bayesian inference, optimized CSP allocation, baseline comparisons, quantitative recovery-time metrics and experimental replication.

## Tests

`python -m unittest discover -s tests -v` 

No measured claims are made about a real city's water supply.

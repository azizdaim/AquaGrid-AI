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

1. **Show the network**: "This is a fictional city, not a physical hydraulic model. We created reservoirs, junctions, six districts and limited-capacity connections."
2. **Explain the AI**: "District agents request water, reservoir agents offer supply, the network agent searches feasible routes using A*, and the coordinator makes allocation decisions."
3. **Select the hospital pipe-failure scenario**: "The direct route is now disabled. A* searches for a different path and routes limited water from the South Reservoir through the East Junction to the Hospital."
4. **Show measured output**: "The total delivered falls from 100% to 93.6%. The hospital gets 110/180 units because the backup pipe has limited throughput. The model respects the pipe limit."
5. **End with next milestone**: "Next we will compare coordination against a fixed allocation baseline, expand testing and develop a truly live simulation dashboard."

## What is not done
- Multi-step stateful simulation, physical water pressure, sensor noise/Bayesian inference, optimized CSP allocation, baseline comparisons, quantitative recovery-time metrics and experimental replication.

## Tests

`python -m unittest discover -s tests -v` 

No measured claims are made about a real city's water supply.

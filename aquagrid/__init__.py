"""AquaGrid AI: educational prototype of multi-agent resource allocation."""
from .simulator import run_scenario
from .scenarios import SCENARIOS

__all__ = ["run_scenario", "SCENARIOS"]

"""
STAND-IN FILE (Member 4 owns ai_problem.py in the final merged repo).
Implements TradingImprovementProblem and path_codes() matching the
Implementation Guide & AI Explanation Guide interfaces.
"""
from knowledge_base import (
    AREA_FACTOR,
    BASE_GRAPH,
    GOAL,
    HEURISTIC,
    START,
    STATE_AREA,
    STATE_CODE,
)

PROBLEM_STATEMENT = (
    "Find the lowest-cost sequence of analysis steps from Analyze Trading History "
    "to Generate Performance Improvement Report, where a trader's weak areas "
    "lower transition costs so the optimal path targets their biggest weaknesses."
)


class TradingImprovementProblem:
    """Formal 6-part AI search problem built dynamically from a trader's area ratings."""

    def __init__(self, levels: dict):
        self.levels = levels
        self.initial_state = START
        self.goal_state = GOAL
        self.graph = self._build_weighted_graph()

    def _build_weighted_graph(self) -> dict:
        weighted = {}
        for state, edges in BASE_GRAPH.items():
            weighted[state] = []
            for next_state, base_cost in edges:
                area = STATE_AREA.get(next_state)
                factor = AREA_FACTOR.get(self.levels.get(area, "AVERAGE"), 1.0) if area else 1.0
                cost = round(base_cost * factor, 2)
                weighted[state].append((next_state, cost))
        return weighted

    def goal_test(self, state: str) -> bool:
        return state == self.goal_state

    def actions(self, state: str) -> list:
        """Return list of (next_state, step_cost) tuples reachable from state."""
        return self.graph.get(state, [])

    def result(self, state: str, action: str) -> str:
        return action

    def step_cost(self, state: str, next_state: str) -> float:
        for nxt, cost in self.graph.get(state, []):
            if nxt == next_state:
                return cost
        raise ValueError(f"No edge from {state!r} to {next_state!r}")

    def path_cost(self, path: list) -> float:
        total = 0.0
        for i in range(len(path) - 1):
            total += self.step_cost(path[i], path[i + 1])
        return round(total, 2)

    def heuristic(self, state: str) -> float:
        return HEURISTIC.get(state, 0.0)


def path_codes(path: list) -> str:
    """Format a path of state names as short codes, e.g. 'S → WR → EQ → G'."""
    return " → ".join(STATE_CODE.get(s, s) for s in path)

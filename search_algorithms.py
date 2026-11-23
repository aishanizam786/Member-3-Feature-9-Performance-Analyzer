"""
Search Algorithms for Trading Journal & Performance Analyzer (search_algorithms.py)

MEMBER 3 OWNERSHIP (REAL CODE):
  - SearchResult dataclass (shared contract across all members)
  - astar(problem): A* Search using f(n) = g(n) + h(n)
  - check_heuristic(problem): proves h(n) <= true cheapest cost for every state
  - run_all(problem): runs all 5 algorithms on the same problem for Feature 11

STAND-INS (to be replaced with teammates' implementations when merging):
  - bfs(problem), dfs(problem)      -> Member 1
  - ucs(problem), greedy(problem)   -> Member 2
"""
from collections import deque
from dataclasses import dataclass, field
import heapq

from knowledge_base import HEURISTIC, STATE_CODE


@dataclass
class SearchResult:
    name: str
    path: list
    cost: float
    explored: list
    trace: list = field(default_factory=list)


def _fmt_num(val: float) -> str:
    """Format floats cleanly (e.g. 5.0 -> '5', 5.5 -> '5.5')."""
    rounded = round(val, 2)
    return str(int(rounded)) if rounded == int(rounded) else str(rounded)


def _code(state: str) -> str:
    return STATE_CODE.get(state, state)


# =====================================================================
# MEMBER 3 — A* SEARCH ALGORITHM (REAL IMPLEMENTATION)
# =====================================================================
def astar(problem) -> SearchResult:
    """
    A* Search: expands the frontier node with the lowest f(n) = g(n) + h(n).
    Uses a min-heap priority queue with insertion-order tie-breaking so that
    equal-f nodes expand deterministically in neighbor order.
    """
    start = problem.initial_state
    h0 = problem.heuristic(start)
    counter = 0
    # Heap items: (f, tie_breaker, state, path, g)
    frontier = [(h0, counter, start, [start], 0.0)]
    best_g = {start: 0.0}
    explored = []
    explored_set = set()
    trace = []

    while frontier:
        f_val, _, state, path, g_val = heapq.heappop(frontier)
        if state in explored_set:
            continue

        explored.append(state)
        explored_set.add(state)
        h_val = problem.heuristic(state)

        if problem.goal_test(state):
            trace.append({
                "step": len(explored),
                "expanded": _code(state),
                "expanded_full": state,
                "g": _fmt_num(g_val),
                "h": _fmt_num(h_val),
                "f": _fmt_num(f_val),
                "is_goal": True,
                "frontier": (
                    f"Goal reached · Path {' → '.join(_code(s) for s in path)} "
                    f"· cost {_fmt_num(g_val)}"
                ),
            })
            return SearchResult(
                name="A*",
                path=path,
                cost=round(g_val, 2),
                explored=explored,
                trace=trace,
            )

        for nxt, step_cost in problem.actions(state):
            if nxt in explored_set:
                continue
            new_g = round(g_val + step_cost, 2)
            if nxt not in best_g or new_g < best_g[nxt]:
                best_g[nxt] = new_g
                new_f = round(new_g + problem.heuristic(nxt), 2)
                counter += 1
                heapq.heappush(frontier, (new_f, counter, nxt, path + [nxt], new_g))

        # Build clean frontier snapshot (deduplicated by best f for unexpanded nodes)
        best_frontier = {}
        for f_item, c_item, st_item, _, _ in sorted(frontier):
            if st_item not in explored_set and st_item not in best_frontier:
                best_frontier[st_item] = (f_item, c_item)
        frontier_str = " · ".join(
            f"{_code(st)} {_fmt_num(vals[0])}"
            for st, vals in sorted(best_frontier.items(), key=lambda kv: kv[1])
        ) or "(empty)"

        trace.append({
            "step": len(explored),
            "expanded": _code(state),
            "expanded_full": state,
            "g": _fmt_num(g_val),
            "h": _fmt_num(h_val),
            "f": _fmt_num(f_val),
            "is_goal": False,
            "frontier": frontier_str,
        })

    return SearchResult(name="A*", path=[], cost=float("inf"), explored=explored, trace=trace)


# =====================================================================
# MEMBER 3 — HEURISTIC ADMISSIBILITY CHECK (REAL IMPLEMENTATION)
# =====================================================================
def _true_cheapest_cost_to_goal(problem, start_state: str) -> float:
    """Run UCS from any given state to Goal to find its exact optimal remaining cost."""
    counter = 0
    frontier = [(0.0, counter, start_state)]
    visited = set()

    while frontier:
        g_val, _, state = heapq.heappop(frontier)
        if state in visited:
            continue
        visited.add(state)

        if problem.goal_test(state):
            return round(g_val, 2)

        for nxt, step_cost in problem.actions(state):
            if nxt not in visited:
                counter += 1
                heapq.heappush(frontier, (round(g_val + step_cost, 2), counter, nxt))

    return float("inf")


def check_heuristic(problem) -> tuple:
    """
    Verify admissibility for every state in the state-space graph:
      Admissible iff h(n) <= true cheapest cost from n to Goal.
    Returns (all_admissible: bool, rows: list[dict]).
    """
    rows = []
    all_ok = True

    for state in STATE_CODE:
        h_val = round(HEURISTIC.get(state, 0.0), 2)
        real_cost = _true_cheapest_cost_to_goal(problem, state)
        ok = h_val <= real_cost + 1e-9
        if not ok:
            all_ok = False
        rows.append({
            "state": state,
            "code": _code(state),
            "h": _fmt_num(h_val),
            "real_cost": _fmt_num(real_cost),
            "admissible": ok,
        })

    return all_ok, rows


# =====================================================================
# STAND-IN ALGORITHMS (Member 1: BFS/DFS, Member 2: UCS/Greedy)
# Replace these 4 functions with your teammates' code during GitHub merge.
# =====================================================================
def bfs(problem) -> SearchResult:
    """STAND-IN (Member 1): Breadth-First Search using FIFO queue."""
    start = problem.initial_state
    queue = deque([(start, [start])])
    seen = {start}
    explored = []
    trace = []

    while queue:
        state, path = queue.popleft()
        explored.append(state)

        if problem.goal_test(state):
            cost = problem.path_cost(path)
            trace.append({
                "step": len(explored),
                "expanded": _code(state),
                "expanded_full": state,
                "g": _fmt_num(cost),
                "h": "—",
                "f": "—",
                "is_goal": True,
                "frontier": f"Goal reached · Path {' → '.join(_code(s) for s in path)} · cost {_fmt_num(cost)}",
            })
            return SearchResult("BFS", path, cost, explored, trace)

        added = []
        for nxt, _ in problem.actions(state):
            if nxt in seen:
                continue
            seen.add(nxt)
            new_path = path + [nxt]
            if problem.goal_test(nxt):
                # Standard BFS early goal test (matches AI Guide p. 11: 3 explored S, WR, G)
                explored.append(nxt)
                cost = problem.path_cost(new_path)
                trace.append({
                    "step": len(explored) - 1,
                    "expanded": _code(state),
                    "expanded_full": state,
                    "g": _fmt_num(problem.path_cost(path)),
                    "h": "—",
                    "f": "—",
                    "is_goal": False,
                    "frontier": f"Found goal {_code(nxt)} via shortcut (stopped)",
                })
                trace.append({
                    "step": len(explored),
                    "expanded": _code(nxt),
                    "expanded_full": nxt,
                    "g": _fmt_num(cost),
                    "h": "—",
                    "f": "—",
                    "is_goal": True,
                    "frontier": f"Goal reached · Path {' → '.join(_code(s) for s in new_path)} · cost {_fmt_num(cost)}",
                })
                return SearchResult("BFS", new_path, cost, explored, trace)
            queue.append((nxt, new_path))
            added.append(_code(nxt))

        frontier_str = " · ".join(_code(s) for s, _ in queue) or "(empty)"
        trace.append({
            "step": len(explored),
            "expanded": _code(state),
            "expanded_full": state,
            "g": _fmt_num(problem.path_cost(path)),
            "h": "—",
            "f": "—",
            "is_goal": False,
            "frontier": frontier_str,
        })

    return SearchResult("BFS", [], float("inf"), explored, trace)


def dfs(problem) -> SearchResult:
    """STAND-IN (Member 1): Depth-First Search using LIFO stack."""
    start = problem.initial_state
    stack = [(start, [start])]
    explored = []
    explored_set = set()
    trace = []

    while stack:
        state, path = stack.pop()
        if state in explored_set:
            continue
        explored.append(state)
        explored_set.add(state)

        if problem.goal_test(state):
            cost = problem.path_cost(path)
            trace.append({
                "step": len(explored),
                "expanded": _code(state),
                "expanded_full": state,
                "g": _fmt_num(cost),
                "h": "—",
                "f": "—",
                "is_goal": True,
                "frontier": f"Goal reached · Path {' → '.join(_code(s) for s in path)} · cost {_fmt_num(cost)}",
            })
            return SearchResult("DFS", path, cost, explored, trace)

        # Push in reverse order so the first listed neighbor sits on top of the stack
        for nxt, _ in reversed(problem.actions(state)):
            if nxt not in explored_set:
                stack.append((nxt, path + [nxt]))

        frontier_str = " · ".join(_code(s) for s, _ in stack) or "(empty)"
        trace.append({
            "step": len(explored),
            "expanded": _code(state),
            "expanded_full": state,
            "g": _fmt_num(problem.path_cost(path)),
            "h": "—",
            "f": "—",
            "is_goal": False,
            "frontier": frontier_str,
        })

    return SearchResult("DFS", [], float("inf"), explored, trace)


def ucs(problem) -> SearchResult:
    """STAND-IN (Member 2): Uniform Cost Search ordered by lowest g(n)."""
    start = problem.initial_state
    counter = 0
    frontier = [(0.0, counter, start, [start])]
    best_g = {start: 0.0}
    explored = []
    explored_set = set()
    trace = []

    while frontier:
        g_val, _, state, path = heapq.heappop(frontier)
        if state in explored_set:
            continue

        explored.append(state)
        explored_set.add(state)

        if problem.goal_test(state):
            trace.append({
                "step": len(explored),
                "expanded": _code(state),
                "expanded_full": state,
                "g": _fmt_num(g_val),
                "h": "—",
                "f": "—",
                "is_goal": True,
                "frontier": f"Goal reached · Path {' → '.join(_code(s) for s in path)} · cost {_fmt_num(g_val)}",
            })
            return SearchResult("UCS", path, round(g_val, 2), explored, trace)

        for nxt, step_cost in problem.actions(state):
            if nxt in explored_set:
                continue
            new_g = round(g_val + step_cost, 2)
            if nxt not in best_g or new_g < best_g[nxt]:
                best_g[nxt] = new_g
                counter += 1
                heapq.heappush(frontier, (new_g, counter, nxt, path + [nxt]))

        best_frontier = {}
        for g_item, c_item, st_item, _ in sorted(frontier):
            if st_item not in explored_set and st_item not in best_frontier:
                best_frontier[st_item] = (g_item, c_item)
        frontier_str = " · ".join(
            f"{_code(st)} {_fmt_num(vals[0])}"
            for st, vals in sorted(best_frontier.items(), key=lambda kv: kv[1])
        ) or "(empty)"

        trace.append({
            "step": len(explored),
            "expanded": _code(state),
            "expanded_full": state,
            "g": _fmt_num(g_val),
            "h": "—",
            "f": "—",
            "is_goal": False,
            "frontier": frontier_str,
        })

    return SearchResult("UCS", [], float("inf"), explored, trace)


def greedy(problem) -> SearchResult:
    """STAND-IN (Member 2): Greedy Best-First Search ordered by lowest h(n)."""
    start = problem.initial_state
    counter = 0
    frontier = [(problem.heuristic(start), counter, start, [start])]
    seen = {start}
    explored = []
    trace = []

    while frontier:
        h_val, _, state, path = heapq.heappop(frontier)
        explored.append(state)
        g_val = problem.path_cost(path)

        if problem.goal_test(state):
            trace.append({
                "step": len(explored),
                "expanded": _code(state),
                "expanded_full": state,
                "g": _fmt_num(g_val),
                "h": _fmt_num(h_val),
                "f": "—",
                "is_goal": True,
                "frontier": f"Goal reached · Path {' → '.join(_code(s) for s in path)} · cost {_fmt_num(g_val)}",
            })
            return SearchResult("Greedy", path, g_val, explored, trace)

        for nxt, _ in problem.actions(state):
            if nxt not in seen:
                seen.add(nxt)
                counter += 1
                heapq.heappush(frontier, (problem.heuristic(nxt), counter, nxt, path + [nxt]))

        frontier_str = " · ".join(
            f"{_code(st)} {_fmt_num(hv)}"
            for hv, _, st, _ in sorted(frontier)
        ) or "(empty)"

        trace.append({
            "step": len(explored),
            "expanded": _code(state),
            "expanded_full": state,
            "g": _fmt_num(g_val),
            "h": _fmt_num(h_val),
            "f": "—",
            "is_goal": False,
            "frontier": frontier_str,
        })

    return SearchResult("Greedy", [], float("inf"), explored, trace)


# =====================================================================
# MEMBER 3 — RUN ALL ALGORITHMS (REAL IMPLEMENTATION)
# =====================================================================
def run_all(problem) -> list:
    """Run all five AI search algorithms on the same problem and return SearchResults."""
    return [
        bfs(problem),
        dfs(problem),
        ucs(problem),
        greedy(problem),
        astar(problem),
    ]

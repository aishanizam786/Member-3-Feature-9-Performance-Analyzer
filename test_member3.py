"""Automated verification for Member 3's AI & Performance Analyzer modules."""
import py_compile
from ai_problem import TradingImprovementProblem, path_codes
from analyzer import assess_areas, calculate_statistics
from sample_data import get_sample_trades
from search_algorithms import check_heuristic, run_all


def run_tests():
    # 1. Verify Feature 9 statistics & area ratings against Implementation Guide p. 17
    trades = get_sample_trades()
    assert len(trades) == 12
    stats = calculate_statistics(trades)
    levels = assess_areas(stats)

    assert stats.wins == 4 and stats.losses == 8
    assert stats.win_rate == 33.33, stats.win_rate
    assert stats.total_pnl == -130.0, stats.total_pnl
    assert stats.avg_profit == 127.5, stats.avg_profit
    assert stats.avg_loss == 80.0, stats.avg_loss
    assert stats.risk_reward == 1.59, stats.risk_reward
    assert stats.sl_respected_pct == 75.0, stats.sl_respected_pct
    assert stats.largest_loss_ratio == 3.12, stats.largest_loss_ratio
    assert stats.max_consecutive_losses == 5, stats.max_consecutive_losses

    assert levels == {
        "win_rate": "WEAK",
        "risk_reward": "AVERAGE",
        "stop_loss": "WEAK",
        "risk_management": "WEAK",
        "discipline": "WEAK",
    }, levels

    # 2. Verify all 5 search algorithms match Implementation Guide p. 19
    problem = TradingImprovementProblem(levels)
    results = {r.name: r for r in run_all(problem)}

    expected = {
        "BFS":    (3, "S → WR → G",       11.0),
        "DFS":    (4, "S → WR → EQ → G",  5.5),
        "UCS":    (8, "S → WR → EQ → G",  5.5),
        "Greedy": (3, "S → WR → G",       11.0),
        "A*":     (6, "S → WR → EQ → G",  5.5),
    }

    for name, (exp_nodes, exp_path, exp_cost) in expected.items():
        r = results[name]
        assert len(r.explored) == exp_nodes, f"{name}: got {len(r.explored)} explored, expected {exp_nodes}"
        assert path_codes(r.path) == exp_path, f"{name}: got {path_codes(r.path)}, expected {exp_path}"
        assert r.cost == exp_cost, f"{name}: got cost {r.cost}, expected {exp_cost}"

    # 3. Verify Heuristic Admissibility Check across all 9 states (AI Guide p. 9)
    ok, rows = check_heuristic(problem)
    assert ok is True
    assert len(rows) == 9
    by_code = {row["code"]: row for row in rows}
    assert by_code["S"]["h"] == "5.5" and by_code["S"]["real_cost"] == "5.5"
    assert by_code["RR"]["h"] == "3.5" and by_code["RR"]["real_cost"] == "4"
    assert by_code["G"]["h"] == "0" and by_code["G"]["real_cost"] == "0"

    # 4. Syntax-check app.py and test Flask routes if Flask is installed
    py_compile.compile("app.py", doraise=True)
    try:
        from app import app
        client = app.test_client()
        for url in ("/analyzer", "/ai/results", "/ai/results?algo=BFS", "/ai/results?algo=UCS", "/ai/results?algo=A*"):
            resp = client.get(url)
            assert resp.status_code == 200, f"{url} returned {resp.status_code}"
        flask_status = "passed (HTTP 200 on all routes)"
    except ModuleNotFoundError:
        flask_status = "skipped (Flask not installed in this environment; app.py syntax verified)"

    print("ALL MEMBER 3 TESTS PASSED!")
    print("Ratings:", levels)
    for name in ("BFS", "DFS", "UCS", "Greedy", "A*"):
        r = results[name]
        print(f"  {name:6s} | explored={len(r.explored)} | path={path_codes(r.path):16s} | cost={r.cost}")
    print(f"Heuristic admissible: {ok} ({len(rows)} states verified)")
    print(f"Flask route tests: {flask_status}")


if __name__ == "__main__":
    run_tests()

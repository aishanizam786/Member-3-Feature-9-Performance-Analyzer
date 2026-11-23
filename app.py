"""
Flask Application — Member 3 Standalone Dev Entrypoint (app.py)

MEMBER 3 REAL ROUTES:
  - /analyzer      (Feature 9: Performance Analyzer)
  - /ai/results    (Feature 11: AI Results + Heuristic Admissibility Check)

STAND-IN WRAPPER:
  Uses get_sample_trades() instead of Member 2's SQLite database and provides
  friendly placeholder redirects for teammates' sidebar pages. When merging into
  the team's final app.py, copy the /analyzer and /ai/results route functions
  and swap get_sample_trades() for analyse_user() with @login_required.
"""
from flask import Flask, flash, redirect, render_template, request, url_for

from ai_problem import TradingImprovementProblem, path_codes
from analyzer import assess_areas, calculate_statistics
from knowledge_base import AREAS, STATE_CODE
from sample_data import get_sample_trades
from search_algorithms import check_heuristic, run_all

app = Flask(__name__)
app.secret_key = "member3-dev-secret-key"


def analyse_user():
    """
    STAND-IN helper matching Implementation Guide section 3.4.
    In the merged app, this loads the logged-in user's trades from SQLite.
    """
    trades = get_sample_trades()
    stats = calculate_statistics(trades)
    levels = assess_areas(stats)
    return trades, stats, levels


def _result_badge(result, best_cost):
    """Map each algorithm result to a clean badge label and CSS class."""
    if result.name == "A*":
        return "Optimal · recommended", "badge-blue"
    if result.name == "UCS":
        return "Optimal", "badge-green"
    if result.name == "DFS" and result.cost == best_cost:
        return "Optimal by chance", "badge-muted"
    if result.name == "BFS":
        return "Fewest steps", "badge-muted"
    return "Not optimal", "badge-red"


def _plain_recommendation(path: list) -> str:
    """Turn the optimal A* path into a plain-English one-line focus tip."""
    middle = [s for s in path if s not in ("Analyze Trading History", "Generate Performance Improvement Report")]
    if len(middle) >= 2:
        first = middle[0].replace("Analyze ", "").replace("Review ", "")
        second = middle[1].replace("Analyze ", "").replace("Review ", "")
        return f"Focus first on {first}, then {second}."
    if middle:
        return f"Focus first on {middle[0]}."
    return "Maintain your current trading approach."


@app.route("/")
def home():
    return redirect(url_for("analyzer"))


# =====================================================================
# MEMBER 3 — FEATURE 9: PERFORMANCE ANALYZER
# =====================================================================
@app.route("/analyzer")
def analyzer():
    trades, stats, levels = analyse_user()

    area_rows = [
        {
            "key": "win_rate",
            "label": "Win Rate",
            "value": f"{stats.win_rate:.1f}%",
            "rule": AREAS[0]["rule"],
            "level": levels["win_rate"],
        },
        {
            "key": "risk_reward",
            "label": "Risk-to-Reward",
            "value": f"{stats.risk_reward:.2f}",
            "rule": AREAS[1]["rule"],
            "level": levels["risk_reward"],
        },
        {
            "key": "stop_loss",
            "label": "Stop Loss Management",
            "value": f"{stats.sl_respected_pct:.1f}% respected",
            "rule": AREAS[2]["rule"],
            "level": levels["stop_loss"],
        },
        {
            "key": "risk_management",
            "label": "Risk Management",
            "value": f"Largest loss {stats.largest_loss_ratio:.2f}× avg loss",
            "rule": AREAS[3]["rule"],
            "level": levels["risk_management"],
        },
        {
            "key": "discipline",
            "label": "Trading Discipline",
            "value": f"{stats.max_consecutive_losses} losses in a row",
            "rule": AREAS[4]["rule"],
            "level": levels["discipline"],
        },
    ]

    return render_template(
        "analyzer.html",
        active_page="analyzer",
        stats=stats,
        levels=levels,
        area_rows=area_rows,
    )


# =====================================================================
# MEMBER 3 — FEATURE 11: AI RESULTS (+ HEURISTIC ADMISSIBILITY CHECK)
# =====================================================================
@app.route("/ai/results")
def ai_results():
    trades, stats, levels = analyse_user()
    if not trades:
        flash("No trades found. Add trades first to run AI analysis.")
        return redirect(url_for("analyzer"))

    problem = TradingImprovementProblem(levels)
    results = run_all(problem)
    selected = request.args.get("algo", "A*")
    chosen = next((r for r in results if r.name == selected), results[-1])

    best_cost = min(r.cost for r in results)
    heuristic_ok, heuristic_rows = check_heuristic(problem)

    astar_result = next(r for r in results if r.name == "A*")
    ucs_result = next(r for r in results if r.name == "UCS")

    # Build comparison table rows with badges
    comparison_rows = []
    for r in results:
        badge_text, badge_class = _result_badge(r, best_cost)
        comparison_rows.append({
            "name": r.name,
            "explored_count": len(r.explored),
            "path_str": path_codes(r.path),
            "cost": r.cost,
            "is_best": r.name == "A*",
            "badge_text": badge_text,
            "badge_class": badge_class,
        })

    # Precompute highlighted nodes and edges for the Chosen Path SVG (always shows chosen algo or A*)
    astar_codes = [STATE_CODE[s] for s in astar_result.path]
    astar_edges = {
        (astar_codes[i], astar_codes[i + 1]) for i in range(len(astar_codes) - 1)
    }

    # Map edge costs by short code pair for SVG labels
    edge_costs = {}
    for src, links in problem.graph.items():
        for dst, cost in links:
            val = int(cost) if cost == int(cost) else cost
            edge_costs[(STATE_CODE[src], STATE_CODE[dst])] = str(val)

    return render_template(
        "ai_results.html",
        active_page="ai_results",
        results=results,
        comparison_rows=comparison_rows,
        chosen=chosen,
        astar_result=astar_result,
        ucs_result=ucs_result,
        astar_path_str=path_codes(astar_result.path),
        recommendation=_plain_recommendation(astar_result.path),
        best_cost=best_cost,
        heuristic_ok=heuristic_ok,
        heuristic_rows=heuristic_rows,
        astar_nodes=set(astar_codes),
        astar_edges=astar_edges,
        edge_costs=edge_costs,
    )


# =====================================================================
# STAND-IN PLACEHOLDER ROUTES FOR TEAMMATES' SIDEBAR LINKS
# =====================================================================
@app.route("/placeholder/<feature>")
def placeholder(feature):
    owners = {
        "dashboard": "Member 1 (Dashboard)",
        "add_trade": "Member 2 (Add Trade)",
        "history": "Member 2 (Trade History)",
        "manage": "Search & Sort / Undo (Features 6–8)",
        "ai_search": "Member 4 (AI Search Module)",
        "suggestions": "Member 4 (AI Suggestions)",
        "queue": "Member 1 (Analysis Queue)",
        "reports": "Member 4 (Reports & Logout)",
    }
    label = owners.get(feature, feature)
    flash(f"'{label}' is built in another teammate's repo and will connect during GitHub merge.")
    return redirect(url_for("analyzer"))


if __name__ == "__main__":
    app.run(debug=True)

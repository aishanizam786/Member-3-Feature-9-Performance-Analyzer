"""
Knowledge Base for Trading Journal & Performance Analyzer.

MEMBER 3 OWNERSHIP:
  - HEURISTIC: optimistic lower-bound h(n) for every state (used by A* & Greedy)
  - THRESHOLDS / AREAS: used by analyzer.py (Feature 9)

STAND-IN (Member 4 owns the full knowledge_base.py in the final merged repo):
  - START, GOAL, STATE_CODE, STATE_AREA, BASE_GRAPH, AREA_FACTOR
  Keep these exact constant names so merging with Member 4 is drop-in.
"""

START = "Analyze Trading History"
GOAL = "Generate Performance Improvement Report"

STATE_CODE = {
    "Analyze Trading History": "S",
    "Analyze Win Rate": "WR",
    "Analyze Risk-to-Reward Ratio": "RR",
    "Analyze Stop Loss Management": "SL",
    "Review Entry Quality": "EQ",
    "Review Trade Targets": "TG",
    "Review Risk Management": "RM",
    "Review Trading Discipline": "DS",
    "Generate Performance Improvement Report": "G",
}

# Maps each analysis state to the performance area that adjusts incoming edge costs.
# Start (S) and Goal (G) have no area (factor = 1.0).
STATE_AREA = {
    "Analyze Trading History": None,
    "Analyze Win Rate": "win_rate",
    "Analyze Risk-to-Reward Ratio": "risk_reward",
    "Analyze Stop Loss Management": "stop_loss",
    "Review Entry Quality": "win_rate",
    "Review Trade Targets": "risk_reward",
    "Review Risk Management": "risk_management",
    "Review Trading Discipline": "discipline",
    "Generate Performance Improvement Report": None,
}

# Performance area metadata (used by Feature 9: Performance Analyzer)
AREAS = [
    {
        "key": "win_rate",
        "label": "Win Rate",
        "rule": "Strong ≥ 55% · Average 40–55% · Weak < 40%",
    },
    {
        "key": "risk_reward",
        "label": "Risk-to-Reward",
        "rule": "Strong ≥ 2.0 · Average 1.0–2.0 · Weak < 1.0",
    },
    {
        "key": "stop_loss",
        "label": "Stop Loss Management",
        "rule": "Strong ≥ 95% · Average 80–95% · Weak < 80%",
    },
    {
        "key": "risk_management",
        "label": "Risk Management",
        "rule": "Strong ≤ 1.5× · Average 1.5–2.5× · Weak > 2.5×",
    },
    {
        "key": "discipline",
        "label": "Trading Discipline",
        "rule": "Strong ≤ 2 · Average 3 · Weak ≥ 4 losses",
    },
]

# Dynamic edge-cost multipliers based on area rating
AREA_FACTOR = {
    "WEAK": 0.5,
    "AVERAGE": 1.0,
    "STRONG": 1.5,
}

# State-space graph (9 states, 13 directed transitions with base costs).
# Neighbor order is preserved intentionally to match the AI Explanation Guide traces.
BASE_GRAPH = {
    "Analyze Trading History": [
        ("Analyze Win Rate", 4),
        ("Analyze Risk-to-Reward Ratio", 4),
        ("Analyze Stop Loss Management", 4),
    ],
    "Analyze Win Rate": [
        ("Review Entry Quality", 3),
        ("Review Trading Discipline", 4),
        ("Generate Performance Improvement Report", 9),  # expensive shortcut
    ],
    "Analyze Risk-to-Reward Ratio": [
        ("Review Trade Targets", 3),
        ("Review Risk Management", 4),
    ],
    "Analyze Stop Loss Management": [
        ("Review Risk Management", 3),
        ("Review Trading Discipline", 4),
    ],
    "Review Entry Quality": [
        ("Generate Performance Improvement Report", 2),
    ],
    "Review Trade Targets": [
        ("Generate Performance Improvement Report", 2),
    ],
    "Review Risk Management": [
        ("Generate Performance Improvement Report", 2),
    ],
    "Review Trading Discipline": [
        ("Generate Performance Improvement Report", 2),
    ],
    "Generate Performance Improvement Report": [],
}

# =====================================================================
# MEMBER 3 — HEURISTIC FUNCTION h(n)
# =====================================================================
# Calculated assuming the cheapest possible case: every remaining area is
# WEAK (factor 0.5):
#   - EQ, TG, RM, DS -> G always costs 2        => h = 2.0
#   - WR, RR, SL -> min base-3 edge * 0.5 + 2   => h = 1.5 + 2.0 = 3.5
#   - S -> base-4 edge * 0.5 + 3.5              => h = 2.0 + 3.5 = 5.5
#   - G (goal)                                  => h = 0.0
# Because real costs can only be >= this optimistic lower bound, h(n) is
# admissible (and consistent), guaranteeing A* finds the optimal path.
HEURISTIC = {
    "Analyze Trading History": 5.5,
    "Analyze Win Rate": 3.5,
    "Analyze Risk-to-Reward Ratio": 3.5,
    "Analyze Stop Loss Management": 3.5,
    "Review Entry Quality": 2.0,
    "Review Trade Targets": 2.0,
    "Review Risk Management": 2.0,
    "Review Trading Discipline": 2.0,
    "Generate Performance Improvement Report": 0.0,
}

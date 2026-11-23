# Trading Journal & Performance Analyzer — Member 3 (AI & Analytics)

Standalone, runnable Flask project for **Member 3's AI & Analytics deliverables** (excluding Search/Sort Features 6 & 7). Built on the 12 calibrated sample trades and clean stand-ins so it can be run, demoed, and tested independently before merging with teammates' GitHub repos.

## Member 3 Deliverables vs. Temporary Stand-Ins

| File | Status | Notes |
| :--- | :--- | :--- |
| `analyzer.py` | **Member 3 (Final)** | Feature 9: `calculate_statistics()` & `assess_areas()` using Implementation Guide thresholds. |
| `search_algorithms.py` | **Member 3 (Final + Stand-ins)** | Final `SearchResult`, `astar()`, `check_heuristic()`, and `run_all()`. Stand-in `bfs()`, `dfs()` (Member 1) and `ucs()`, `greedy()` (Member 2) are clearly marked for replacement. |
| `knowledge_base.py` | **Member 3 `HEURISTIC` + Stand-in Graph** | Final `HEURISTIC` table and `AREAS`; graph constants match Member 4's interface. |
| `templates/analyzer.html` | **Member 3 (Final)** | Feature 9 dark-theme UI matching the prototype. |
| `templates/ai_results.html` | **Member 3 (Final)** | Feature 11 dark-theme UI: comparison table, step-by-step trace switcher, chosen-path SVG, and Heuristic Admissibility Check table. |
| `app.py` | **Member 3 Routes + Dev Wrapper** | Final `/analyzer` and `/ai/results` routes wrapped in a standalone dev app. |
| `models.py`, `sample_data.py`, `ai_problem.py`, `templates/base.html`, `static/style.css` | **Temporary Stand-Ins** | Replace with Member 1 (`base.html`, `style.css`), Member 2 (`models.py`, `database.py`), and Member 4 (`ai_problem.py`, `knowledge_base.py`) during final merge. |

## Quick Start

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

pip install -r requirements.txt
flask --app app run --debug
```

Open `http://127.0.0.1:5000` in your browser:
- `/analyzer` — Feature 9: Performance Analyzer
- `/ai/results` — Feature 11: AI Results & Heuristic Admissibility Check

## Run Automated Verification

```bash
python test_member3.py
```

Verifies every number against the Implementation Guide & AI Explanation Guide (Win Rate 33.33% WEAK, R:R 1.59 AVERAGE, SL 75% WEAK, Largest Loss 3.12× WEAK, 5 losses in a row WEAK; A* explores 6 states vs. UCS 8 states with optimal cost 5.5; all 9 states admissible).

## How to Merge with Teammates' GitHub Repos Later

1. Copy your `analyzer.py`, `templates/analyzer.html`, and `templates/ai_results.html` directly into the combined repo.
2. In `search_algorithms.py`, replace the 4 stand-in functions (`bfs`, `dfs`, `ucs`, `greedy`) with Member 1's and Member 2's functions (keeping `SearchResult`, `astar`, `check_heuristic`, and `run_all`).
3. Ensure `knowledge_base.py` includes your `HEURISTIC` dict and `AREAS` list.
4. Copy the `/analyzer` and `/ai/results` routes from `app.py` into the combined `app.py` (adding `@login_required` and using the shared `analyse_user()` helper).

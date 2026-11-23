"""
MEMBER 3 — FEATURE 9: PERFORMANCE ANALYZER (analyzer.py)

Calculates trading statistics from a list of Trade objects and rates the
five performance areas as WEAK, AVERAGE, or STRONG using the thresholds
in the Implementation Guide (pages 16–17).

These ratings feed directly into Member 4's TradingImprovementProblem(levels)
and expert_advice.py, as well as Member 3's A* search & AI Results page.
"""
from dataclasses import dataclass


@dataclass
class PerformanceStats:
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    total_pnl: float = 0.0
    avg_profit: float = 0.0
    avg_loss: float = 0.0
    risk_reward: float = 0.0
    sl_respected_count: int = 0
    sl_respected_pct: float = 0.0
    largest_loss: float = 0.0
    largest_loss_label: str = ""
    largest_loss_ratio: float = 0.0
    max_consecutive_losses: int = 0
    streak_range: str = ""


def _sl_was_respected(trade) -> bool:
    """
    A losing BUY respects its stop loss if exit_price >= stop_loss.
    A losing SELL respects its stop loss if exit_price <= stop_loss.
    """
    direction = trade.direction.upper()
    if direction == "BUY":
        return trade.exit_price >= trade.stop_loss
    return trade.exit_price <= trade.stop_loss


def calculate_statistics(trades: list) -> PerformanceStats:
    """Compute all 7 performance analyzer metrics from a list of Trade records."""
    if not trades:
        return PerformanceStats()

    total = len(trades)
    winning = [t for t in trades if t.profit_loss > 0]
    losing = [t for t in trades if t.profit_loss < 0]

    wins = len(winning)
    losses = len(losing)
    win_rate = round((wins / total) * 100, 2)
    total_pnl = round(sum(t.profit_loss for t in trades), 2)

    avg_profit = round(sum(t.profit_loss for t in winning) / wins, 2) if wins else 0.0
    avg_loss = round(sum(abs(t.profit_loss) for t in losing) / losses, 2) if losses else 0.0
    risk_reward = round(avg_profit / avg_loss, 2) if avg_loss > 0 else 0.0

    # Stop loss respected = losing trades closed at or before SL / all losing trades * 100
    if losses:
        sl_ok = sum(1 for t in losing if _sl_was_respected(t))
        sl_respected_pct = round((sl_ok / losses) * 100, 2)
    else:
        sl_ok = 0
        sl_respected_pct = 100.0

    # Largest loss and ratio to average loss
    if losing:
        worst = min(losing, key=lambda t: t.profit_loss)
        largest_loss = round(abs(worst.profit_loss), 2)
        largest_loss_label = f"#{worst.trade_id} {worst.pair}"
        largest_loss_ratio = round(largest_loss / avg_loss, 2) if avg_loss > 0 else 0.0
    else:
        largest_loss = 0.0
        largest_loss_label = "None"
        largest_loss_ratio = 0.0

    # Longest run of consecutive losing trades in chronological date order
    ordered = sorted(trades, key=lambda t: (t.trade_date, t.trade_id))
    max_streak = 0
    cur_streak = 0
    cur_start = None
    best_start = None
    best_end = None

    for t in ordered:
        if t.profit_loss < 0:
            if cur_streak == 0:
                cur_start = t.trade_date
            cur_streak += 1
            if cur_streak > max_streak:
                max_streak = cur_streak
                best_start = cur_start
                best_end = t.trade_date
        else:
            cur_streak = 0
            cur_start = None

    streak_range = f"{best_start} – {best_end}" if best_start and best_end else ""

    return PerformanceStats(
        total_trades=total,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        total_pnl=total_pnl,
        avg_profit=avg_profit,
        avg_loss=avg_loss,
        risk_reward=risk_reward,
        sl_respected_count=sl_ok,
        sl_respected_pct=sl_respected_pct,
        largest_loss=largest_loss,
        largest_loss_label=largest_loss_label,
        largest_loss_ratio=largest_loss_ratio,
        max_consecutive_losses=max_streak,
        streak_range=streak_range,
    )


def assess_areas(stats: PerformanceStats) -> dict:
    """
    Rate each of the 5 performance areas as 'WEAK', 'AVERAGE', or 'STRONG'
    according to the Implementation Guide (page 17):
      - Win Rate:       Weak < 40, Average 40..55, Strong >= 55
      - Risk-to-Reward: Weak < 1.0, Average 1.0..2.0, Strong >= 2.0
      - Stop Loss:      Weak < 80, Average 80..95, Strong >= 95
      - Risk Mgmt:      Weak > 2.5, Average 1.5..2.5, Strong <= 1.5
      - Discipline:     Weak >= 4, Average == 3, Strong <= 2
    """
    # 1. Win Rate
    if stats.win_rate < 40:
        wr = "WEAK"
    elif stats.win_rate < 55:
        wr = "AVERAGE"
    else:
        wr = "STRONG"

    # 2. Risk-to-Reward
    if stats.risk_reward < 1.0:
        rr = "WEAK"
    elif stats.risk_reward < 2.0:
        rr = "AVERAGE"
    else:
        rr = "STRONG"

    # 3. Stop Loss Management
    if stats.sl_respected_pct < 80:
        sl = "WEAK"
    elif stats.sl_respected_pct < 95:
        sl = "AVERAGE"
    else:
        sl = "STRONG"

    # 4. Risk Management (largest loss ratio)
    if stats.largest_loss_ratio > 2.5:
        rm = "WEAK"
    elif stats.largest_loss_ratio > 1.5:
        rm = "AVERAGE"
    else:
        rm = "STRONG"

    # 5. Trading Discipline (max consecutive losses)
    if stats.max_consecutive_losses >= 4:
        ds = "WEAK"
    elif stats.max_consecutive_losses == 3:
        ds = "AVERAGE"
    else:
        ds = "STRONG"

    return {
        "win_rate": wr,
        "risk_reward": rr,
        "stop_loss": sl,
        "risk_management": rm,
        "discipline": ds,
    }

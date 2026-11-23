"""
STAND-IN FILE (Member 2 owns models.py in the final merged repo).
Matches the Trade record fields defined in the Implementation Guide.
"""
from dataclasses import dataclass


@dataclass
class Trade:
    trade_id: int
    pair: str
    direction: str      # "BUY" or "SELL"
    entry: float
    stop_loss: float
    take_profit: float
    exit_price: float
    profit_loss: float
    trade_date: str     # "YYYY-MM-DD"

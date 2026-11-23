"""
STAND-IN FILE (Member 2 owns database.py / trade storage in the final merged repo).

Provides the 12 sample trades calibrated to produce the exact Performance Analyzer
and AI Search numbers documented in the Implementation Guide & AI Explanation Guide:
  - Total trades: 12 (4 wins, 8 losses)
  - Win rate: 33.33% (WEAK)
  - Average profit: 127.50, Average loss: 80.00, Net P/L: -130.00
  - Risk-to-Reward: 1.59 (AVERAGE)
  - Stop loss respected: 75.0% (6 of 8 losing trades -> WEAK)
  - Largest loss: -250.00 (#5 XAUUSD), ratio 3.12x avg loss (WEAK)
  - Max consecutive losses: 5 (Oct 06 - Oct 12 -> WEAK)
"""
from models import Trade


def get_sample_trades() -> list:
    return [
        Trade(1,  "XAUUSD", "BUY",  2650.00, 2640.00, 2665.00, 2665.00, +150.00, "2026-10-01"),
        Trade(2,  "EURUSD", "SELL", 1.0850,  1.0875,  1.0800,  1.0875,  -55.00,  "2026-10-02"),
        Trade(3,  "GBPUSD", "BUY",  1.2710,  1.2680,  1.2760,  1.2750,  +120.00, "2026-10-05"),
        Trade(4,  "USDJPY", "SELL", 149.80,  150.20,  149.00,  150.20,  -55.00,  "2026-10-06"),
        Trade(5,  "XAUUSD", "SELL", 2668.50, 2680.50, 2645.00, 2680.50, -250.00, "2026-10-07"),
        Trade(6,  "EURUSD", "BUY",  1.0820,  1.0795,  1.0870,  1.0790,  -60.00,  "2026-10-08"),  # SL violated
        Trade(7,  "GBPUSD", "SELL", 1.2765,  1.2785,  1.2720,  1.2785,  -55.00,  "2026-10-09"),
        Trade(8,  "XAUUSD", "BUY",  2672.00, 2664.50, 2690.00, 2664.50, -55.00,  "2026-10-12"),
        Trade(9,  "USDJPY", "BUY",  149.20,  148.80,  150.00,  149.90,  +140.00, "2026-10-13"),
        Trade(10, "EURUSD", "SELL", 1.0790,  1.0810,  1.0750,  1.0815,  -55.00,  "2026-10-14"),  # SL violated
        Trade(11, "GBPUSD", "BUY",  1.2690,  1.2660,  1.2740,  1.2730,  +100.00, "2026-10-15"),
        Trade(12, "XAUUSD", "SELL", 2685.00, 2693.40, 2670.00, 2693.40, -55.00,  "2026-10-16"),
    ]

"""
Trading Strategies Package

Contains various trading strategy implementations for the backtester.
"""

from .Buy_And_Hold_Strat import BuyAndHoldStrat
from .MAC_Strat import MovingAverageCrossOverStrat
from .ETF_Forecast import ETFDailyForecastStrategy

__all__ = [
    'BuyAndHoldStrat',
    'MovingAverageCrossOverStrat', 
    'ETFDailyForecastStrategy'
]
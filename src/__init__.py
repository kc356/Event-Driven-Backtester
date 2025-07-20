"""
Event-Driven Backtester Package

A comprehensive backtesting framework for quantitative trading strategies.
"""

__version__ = "1.0.0"
__author__ = "Event-Driven Backtester Team"

from .DataHandler import YahooDataHandler, HistoricCSVDataHandler
from .Events import MarketEvent, SignalEvent, OrderEvent, FillEvent
from .Strategy import Strategy
from .Portfolio import Portfolio
from .Execution import SimpleSimulatedExecutionHandler
from .Performance import create_sharpe_ratio, create_drawdowns
from .BacktesterLoop import Backtest

__all__ = [
    'YahooDataHandler',
    'HistoricCSVDataHandler', 
    'MarketEvent',
    'SignalEvent',
    'OrderEvent',
    'FillEvent',
    'Strategy',
    'Portfolio',
    'SimpleSimulatedExecutionHandler',
    'create_sharpe_ratio',
    'create_drawdowns',
    'Backtest'
] 
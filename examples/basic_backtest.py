#!/usr/bin/env python3
"""
Basic backtest example using the Event-Driven Backtester.

This example demonstrates how to run a simple backtest using the ETF Forecast strategy.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from datetime import datetime
from src.BacktesterLoop import Backtest
from src.DataHandler import YahooDataHandler
from src.Execution import SimpleSimulatedExecutionHandler
from src.Portfolio import Portfolio
from src.Strategies import ETFDailyForecastStrategy


def main():
    """Run a basic backtest example."""
    
    print("Running Basic Backtest Example")
    print("=" * 40)
    
    # Configuration
    symbol_list = ['TQQQ']
    initial_capital = 100000.0
    start_date = datetime(2016, 1, 1, 0, 0, 0)
    end_date = datetime(2021, 1, 1, 0, 0, 0)
    interval = '1d'
    heartbeat = 0.0
    
    print(f"Symbols: {symbol_list}")
    print(f"Period: {start_date.date()} to {end_date.date()}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Strategy: ETF Forecast")
    print("-" * 40)
    
    # Create backtest instance
    backtest = Backtest(
        data_dir='DataDir',
        symbol_list=symbol_list,
        initial_capital=initial_capital,
        heartbeat=heartbeat,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        data_handler=YahooDataHandler,
        execution_handler=SimpleSimulatedExecutionHandler,
        portfolio=Portfolio,
        strategy=ETFDailyForecastStrategy
    )
    
    # Run the backtest
    backtest.simulate_trading()
    
    print("\nBacktest completed successfully!")


if __name__ == "__main__":
    main() 
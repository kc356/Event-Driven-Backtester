#!/usr/bin/env python3
"""
Strategy comparison example using the Event-Driven Backtester.

This example demonstrates how to compare different trading strategies.
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
from src.Strategies import ETFDailyForecastStrategy, MovingAverageCrossOverStrat, BuyAndHoldStrat


def run_strategy_backtest(strategy_class, strategy_name, symbol_list, start_date, end_date, initial_capital):
    """Run a backtest for a specific strategy."""
    
    print(f"\nRunning {strategy_name} Strategy")
    print("-" * 30)
    
    backtest = Backtest(
        data_dir='DataDir',
        symbol_list=symbol_list,
        initial_capital=initial_capital,
        heartbeat=0.0,
        start_date=start_date,
        end_date=end_date,
        interval='1d',
        data_handler=YahooDataHandler,
        execution_handler=SimpleSimulatedExecutionHandler,
        portfolio=Portfolio,
        strategy=strategy_class
    )
    
    backtest.simulate_trading()
    return backtest


def main():
    """Compare different trading strategies."""
    
    print("Strategy Comparison Example")
    print("=" * 50)
    
    # Configuration
    symbol_list = ['TQQQ']
    initial_capital = 100000.0
    start_date = datetime(2016, 1, 1, 0, 0, 0)
    end_date = datetime(2021, 1, 1, 0, 0, 0)
    
    print(f"Symbols: {symbol_list}")
    print(f"Period: {start_date.date()} to {end_date.date()}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    
    # Strategies to compare
    strategies = [
        (BuyAndHoldStrat, "Buy and Hold"),
        (MovingAverageCrossOverStrat, "Moving Average Crossover"),
        (ETFDailyForecastStrategy, "ETF Forecast")
    ]
    
    results = []
    
    for strategy_class, strategy_name in strategies:
        try:
            backtest = run_strategy_backtest(
                strategy_class, strategy_name, symbol_list, 
                start_date, end_date, initial_capital
            )
            results.append((strategy_name, backtest))
        except Exception as e:
            print(f"Error running {strategy_name}: {e}")
    
    print("\n" + "=" * 50)
    print("Strategy Comparison Summary")
    print("=" * 50)
    
    for strategy_name, backtest in results:
        print(f"\n{strategy_name}:")
        print(f"  Signals: {backtest.signals}")
        print(f"  Orders: {backtest.orders}")
        print(f"  Fills: {backtest.fills}")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Entry point for running backtests.

Usage:
    python run_backtest.py --symbol TQQQ --start-date 2016-01-01 --end-date 2021-01-01
    python run_backtest.py --config my_config.json
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config.backtest_config import BacktestConfig, DEFAULT_CONFIG, STRATEGY_CONFIGS
from src.BacktesterLoop import Backtest
from src.DataHandler import YahooDataHandler, HistoricCSVDataHandler
from src.Execution import SimpleSimulatedExecutionHandler
from src.Portfolio import Portfolio
from src.Strategies import ETFDailyForecastStrategy, MovingAverageCrossOverStrat, BuyAndHoldStrat


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def get_strategy_class(strategy_name: str):
    """Get strategy class by name."""
    strategies = {
        'ETF_Forecast': ETFDailyForecastStrategy,
        'MAC_Strat': MovingAverageCrossOverStrat,
        'Buy_And_Hold': BuyAndHoldStrat
    }
    
    if strategy_name not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(strategies.keys())}")
    
    return strategies[strategy_name]


def run_backtest(config: BacktestConfig) -> None:
    """Run a backtest with the given configuration."""
    
    print(f"Starting backtest for symbols: {config.symbol_list}")
    print(f"Period: {config.start_date.date()} to {config.end_date.date()}")
    print(f"Strategy: {config.strategy_name}")
    print(f"Initial Capital: ${config.initial_capital:,.2f}")
    print("-" * 50)
    
    # Get strategy class
    strategy_class = get_strategy_class(config.strategy_name)
    
    # Choose data handler
    if config.use_yahoo_data:
        data_handler_class = YahooDataHandler
    else:
        data_handler_class = HistoricCSVDataHandler
    
    # Create backtest instance
    backtest = Backtest(
        data_dir=config.data_dir,
        symbol_list=config.symbol_list,
        initial_capital=config.initial_capital,
        heartbeat=config.heartbeat,
        start_date=config.start_date,
        end_date=config.end_date,
        interval=config.interval,
        data_handler=data_handler_class,
        execution_handler=SimpleSimulatedExecutionHandler,
        portfolio=Portfolio,
        strategy=strategy_class
    )
    
    # Run the backtest
    backtest.simulate_trading()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run a backtest')
    
    # Basic arguments
    parser.add_argument('--symbol', '-s', type=str, nargs='+', 
                       help='Trading symbols (e.g., TQQQ SPY)')
    parser.add_argument('--start-date', type=parse_date,
                       help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=parse_date,
                       help='End date (YYYY-MM-DD)')
    parser.add_argument('--strategy', type=str, default='ETF_Forecast',
                       choices=['ETF_Forecast', 'MAC_Strat', 'Buy_And_Hold'],
                       help='Trading strategy to use')
    parser.add_argument('--capital', type=float, default=100000.0,
                       help='Initial capital')
    parser.add_argument('--interval', type=str, default='1d',
                       choices=['1d', '1wk', '1mo'],
                       help='Data interval')
    parser.add_argument('--use-csv', action='store_true',
                       help='Use CSV data instead of Yahoo Finance')
    parser.add_argument('--data-dir', type=str, default='DataDir',
                       help='Data directory for CSV files')
    
    args = parser.parse_args()
    
    # Create configuration
    config = BacktestConfig(
        symbol_list=args.symbol or DEFAULT_CONFIG.symbol_list,
        start_date=args.start_date or DEFAULT_CONFIG.start_date,
        end_date=args.end_date or DEFAULT_CONFIG.end_date,
        interval=args.interval,
        initial_capital=args.capital,
        use_yahoo_data=not args.use_csv,
        data_dir=args.data_dir,
        strategy_name=args.strategy
    )
    
    try:
        run_backtest(config)
    except Exception as e:
        print(f"Error running backtest: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
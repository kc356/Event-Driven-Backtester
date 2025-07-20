# Event-Driven Backtester

A personal backtesting engine for quantitative trading strategies, built with an event-driven architecture.

## Features

- **Event-driven architecture** for realistic backtesting
- **Multiple data sources**: Yahoo Finance API and CSV files
- **Trading strategies**: ETF Forecast, Moving Average Crossover, Buy & Hold
- **Portfolio management** with position tracking
- **Performance analysis** with Sharpe ratio and drawdowns

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run a Backtest
```bash
# Basic backtest with SPY
python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01

# Different strategies
python run_backtest.py --symbol SPY --strategy ETF_Forecast
python run_backtest.py --symbol SPY --strategy MAC_Strat
python run_backtest.py --symbol SPY --strategy Buy_And_Hold

# Multiple symbols
python run_backtest.py --symbol SPY QQQ AAPL

# Custom parameters
python run_backtest.py --symbol SPY --capital 50000 --start-date 2018-01-01 --end-date 2023-01-01
```

### Using Makefile Commands
```bash
make run-example    # ETF Forecast strategy
make run-mac        # Moving Average Crossover
make run-buyhold    # Buy and Hold
```

## Project Structure

```
src/
├── BacktesterLoop.py      # Main backtesting engine
├── DataHandler.py         # Data handling (Yahoo Finance, CSV)
├── Events.py             # Event system (Market, Signal, Order, Fill)
├── Strategy.py           # Base strategy class
├── Portfolio.py          # Portfolio management
├── Execution.py          # Order execution simulation
├── Performance.py        # Performance metrics
└── Strategies/           # Trading strategies
    ├── ETF_Forecast.py   # ML-based ETF prediction
    ├── MAC_Strat.py      # Moving average crossover
    └── Buy_And_Hold_Strat.py
```

## Available Strategies

1. **ETF Forecast** (`ETF_Forecast`)
   - Machine learning-based using Quadratic Discriminant Analysis
   - Predicts next day's price movement

2. **Moving Average Crossover** (`MAC_Strat`)
   - Simple moving average crossover strategy
   - Uses short and long moving averages

3. **Buy and Hold** (`Buy_And_Hold`)
   - Basic buy and hold strategy for comparison

## Data Sources

### Yahoo Finance (Default)
```bash
python run_backtest.py --symbol SPY
```

### CSV Files
Place CSV files in `DataDir/` with format: `SYMBOL.csv`
Required columns: `Date, Open, High, Low, Close, Volume, Adj Close`

```bash
python run_backtest.py --symbol SPY --use-csv
```

## Development

### Run Tests
```bash
make test
```

### Code Formatting
```bash
make format
make lint
```

### Clean Up
```bash
make clean
```

## Example Usage

```python
from datetime import datetime
from src.BacktesterLoop import Backtest
from src.DataHandler import YahooDataHandler
from src.Strategies import ETFDailyForecastStrategy

# Create and run backtest
backtest = Backtest(
    data_dir='DataDir',
    symbol_list=['SPY'],
    initial_capital=100000.0,
    start_date=datetime(2016, 1, 1),
    end_date=datetime(2021, 1, 1),
    data_handler=YahooDataHandler,
    strategy=ETFDailyForecastStrategy
)
backtest.simulate_trading()
```

## Future Plans

- Scale to live trading engine
- Add more sophisticated strategies
- Implement risk management features
- Add real-time data feeds

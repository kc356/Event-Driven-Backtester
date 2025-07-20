Quick Start Guide
=================

This guide will help you get started with the Event-Driven Backtester quickly.

Basic Usage
-----------

Running a Simple Backtest
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Using the command line interface:**

   .. code-block:: bash

      python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01

2. **Using Python code:**

   .. code-block:: python

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

Available Strategies
--------------------

The framework includes several pre-built strategies:

* **ETF Forecast**: Machine learning-based strategy using Quadratic Discriminant Analysis
* **Moving Average Crossover**: Simple moving average crossover strategy
* **Buy and Hold**: Basic buy and hold strategy for comparison

Example: Strategy Comparison
----------------------------

.. code-block:: python

   from src.Strategies import ETFDailyForecastStrategy, MovingAverageCrossOverStrat, BuyAndHoldStrat

   # Compare different strategies
   strategies = [
       ('Buy and Hold', BuyAndHoldStrat),
       ('Moving Average Crossover', MovingAverageCrossOverStrat),
       ('ETF Forecast', ETFDailyForecastStrategy)
   ]

   for name, strategy_class in strategies:
       backtest = Backtest(
           data_dir='DataDir',
           symbol_list=['SPY'],
           initial_capital=100000.0,
           start_date=datetime(2016, 1, 1),
           end_date=datetime(2021, 1, 1),
           data_handler=YahooDataHandler,
           strategy=strategy_class
       )
       backtest.simulate_trading()

Data Sources
------------

Yahoo Finance
~~~~~~~~~~~~

Default data source for real-time market data:

.. code-block:: python

   from src.DataHandler import YahooDataHandler

   handler = YahooDataHandler(
       events=events,
       symbol_list=['SPY', 'QQQ'],
       interval='1d',
       start_date=datetime(2016, 1, 1),
       end_date=datetime(2021, 1, 1)
   )

CSV Files
~~~~~~~~~

For historical data stored locally:

.. code-block:: python

   from src.DataHandler import HistoricCSVDataHandler

   handler = HistoricCSVDataHandler(
       events=events,
       csv_dir='DataDir',
       symbol_list=['SPY']
   )

Configuration
-------------

The framework uses a configuration system for easy parameter management:

.. code-block:: python

   from config.backtest_config import BacktestConfig

   config = BacktestConfig(
       symbol_list=['SPY', 'QQQ'],
       start_date=datetime(2016, 1, 1),
       end_date=datetime(2021, 1, 1),
       initial_capital=100000.0,
       strategy_name='ETF_Forecast'
   )

Performance Analysis
--------------------

After running a backtest, you can analyze the results:

.. code-block:: python

   from src.Performance import create_sharpe_ratio, create_drawdowns

   # Calculate Sharpe ratio
   sharpe_ratio = create_sharpe_ratio(backtest.equity_curve['returns'])

   # Calculate drawdowns
   drawdowns = create_drawdowns(backtest.equity_curve['equity_curve'])

   print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
   print(f"Max Drawdown: {drawdowns['drawdown'].min():.2%}")

Next Steps
----------

* Read the :doc:`api/index` for detailed API documentation
* Check out :doc:`examples/index` for more examples
* Learn about :doc:`contributing` to contribute to the project 
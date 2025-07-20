Event-Driven Backtester Documentation
====================================

Welcome to the Event-Driven Backtester documentation!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   examples/index
   contributing

Overview
--------

The Event-Driven Backtester is a comprehensive backtesting framework for quantitative trading strategies. It provides:

* Event-driven architecture for realistic backtesting
* Multiple data sources (Yahoo Finance, CSV files)
* Various trading strategies (Buy & Hold, Moving Average Crossover, ETF Forecast)
* Portfolio management and risk controls
* Performance analysis and visualization

Key Features
------------

* **Event-Driven Architecture**: Simulates real trading environments with events
* **Multiple Data Sources**: Support for Yahoo Finance API and CSV files
* **Strategy Framework**: Easy to implement and test new trading strategies
* **Portfolio Management**: Comprehensive portfolio tracking and management
* **Performance Analysis**: Built-in performance metrics and visualization
* **Type Safety**: Full type hints throughout the codebase

Quick Start
-----------

.. code-block:: python

   from src.BacktesterLoop import Backtest
   from src.DataHandler import YahooDataHandler
   from src.Strategies import ETFDailyForecastStrategy

   # Run a backtest
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

Command Line Usage
-----------------

.. code-block:: bash

   # Run a backtest with command line interface
   python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01

   # Use different strategies
   python run_backtest.py --symbol SPY --strategy MAC_Strat
   python run_backtest.py --symbol SPY --strategy Buy_And_Hold

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 
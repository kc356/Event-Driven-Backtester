from __future__ import print_function

import numpy as np
import os
import pandas as pd
import yfinance as yf
from typing import Dict, List, Tuple, Optional, Iterator, Any, Union
from datetime import datetime
from abc import ABCMeta, abstractmethod
from .Events import MarketEvent


class DataManagement(object):
    """
    Data management class implemented in an abstract manner to handle different
    types of datafeed (coming from database, webscraping, direct datafeed, csv, etc..)
    this generates a Market event in the back test loop
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bar(self, symbol: str) -> Tuple[datetime, pd.Series]:
        """
        Returns the last bar updated.
        """
        raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol: str, N: int = 1) -> List[Tuple[datetime, pd.Series]]:
        """
        Returns the last N bars updated.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol: str) -> datetime:
        """
        Returns a Python datetime object for the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol: str, val_type: str) -> float:
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        from the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def get_latest_bars_values(self, symbol: str, val_type: str, N: int = 1) -> np.ndarray:
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self) -> None:
        """
        Pushes the latest bars to the bars_queue for each symbol
        in a tuple OHLCVI format: (datetime, open, high, low,
        close, volume, adj closing price).
        """
        raise NotImplementedError("Should implement update_bars()")


class YahooDataHandler(DataManagement):
    """
    Get data directly from Yahoo Finance website, and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.
    """

    def __init__(self, events: Any, symbol_list: List[str], interval: str, 
                 start_date: datetime, end_date: datetime) -> None:
        """
        Initialize Queries from yahoo finance api to
        receive historical data transformed to dataframe

        Parameters:
        events - The Event Queue.
        symbol_list - A list of symbol strings.
        interval - 1d, 1wk, 1mo - daily, weekly monthly data
        start_date - starting date for the historical data (format: datetime)
        end_date - final date of the data (format: datetime)

        """

        self.events = events
        self.symbol_list = symbol_list
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.symbol_data: Dict[str, Iterator[Tuple[datetime, pd.Series]]] = {}
        self.latest_symbol_data: Dict[str, List[Tuple[datetime, pd.Series]]] = {}
        self.continue_backtest = True
        self._load_data_from_Yahoo_finance()

    def _load_data_from_Yahoo_finance(self) -> None:
        """
        Queries yfinance api to receive historical data in csv file format
        """

        combined_index: Optional[pd.DatetimeIndex] = None
        for symbol in self.symbol_list:

            # download data from yfinance for symbol. This could be improved as yfinance can download several
            # symbols at the same time
            self.symbol_data[symbol] = yf.download(tickers=[symbol], start=self.start_date,
                                                   end=self.end_date, interval=self.interval, auto_adjust=False)

            # Handle multi-level columns (when downloading multiple symbols)
            if isinstance(self.symbol_data[symbol].columns, pd.MultiIndex):
                # Flatten the column names to use only the first level
                self.symbol_data[symbol].columns = self.symbol_data[symbol].columns.get_level_values(0)

            # rename columns for consistency
            self.symbol_data[symbol].rename(columns={'Open': 'open',
                                                     'High': 'high',
                                                     'Low': 'low',
                                                     'Close': 'close',
                                                     'Adj Close': 'adj_close',
                                                     'Volume': 'volume'}, inplace=True)

            # rename index as well from 'Date' to 'datetime'
            self.symbol_data[symbol].index.name = 'datetime'

            # create returns column (used for some strategies)
            # Use adj_close if available, otherwise use close (which is already adjusted when auto_adjust=True)
            if 'adj_close' in self.symbol_data[symbol].columns:
                self.symbol_data[symbol]['returns'] = self.symbol_data[symbol]["adj_close"].pct_change() * 100.0
            else:
                self.symbol_data[symbol]['returns'] = self.symbol_data[symbol]["close"].pct_change() * 100.0

            # Combine the index to pad forward values
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol] = []

        # Reindex the dataframes
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()

    def _get_new_bar(self, symbol: str) -> Iterator[Tuple[datetime, pd.Series]]:
        """
        Returns the latest bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume, adj_close, etc).
        """
        for bar in self.symbol_data[symbol]:
            yield bar

    def get_latest_bar(self, symbol: str) -> Tuple[datetime, pd.Series]:
        """
        Returns the last bar from the latest_symbol list.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol: str, N: int = 1) -> List[Tuple[datetime, pd.Series]]:
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol: str) -> datetime:
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol: str, value_type: str) -> float:
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], value_type)

    def get_latest_bars_values(self, symbol: str, value_type: str, N: int = 1) -> np.ndarray:
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)  # bars_list = bars_list[-N:]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(bar[1], value_type) for bar in bars_list])

    def update_bars(self) -> None:
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())


class HistoricCSVDataHandler(DataManagement):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.
    """

    def __init__(self, events: Any, csv_dir: str, symbol_list: List[str]) -> None:

        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.
        It will be assumed that all files are of the form
        'symbol.csv', where symbol is a string in the list.
        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.
        """

        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data: Dict[str, Iterator[Tuple[datetime, pd.Series]]] = {}
        self.latest_symbol_data: Dict[str, List[Tuple[datetime, pd.Series]]] = {}
        self.continue_backtest = True
        self._data_conversion_from_csv_files()

    def _data_conversion_from_csv_files(self) -> None:
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """

        combined_index: Optional[pd.DatetimeIndex] = None
        for symbol in self.symbol_list:
            # Load the CSV file with no header information, indexed on date
            self.symbol_data[symbol] = pd.io.parsers.read_csv(
                os.path.join(self.csv_dir, "%s.csv" % symbol),
                header=0, index_col=0,
                names=["datetime", "open", "high", "low", "close", "adj_close", "volume"]
            )

            # rename index as well from 'Date' to 'datetime'
            self.symbol_data[symbol].index.name = 'datetime'

            # create returns column (used for some strategies)
            # Use adj_close if available, otherwise use close
            if 'adj_close' in self.symbol_data[symbol].columns:
                self.symbol_data[symbol]['returns'] = self.symbol_data[symbol]["adj_close"].pct_change() * 100.0
            else:
                self.symbol_data[symbol]['returns'] = self.symbol_data[symbol]["close"].pct_change() * 100.0

            # Combine the index to pad forward values
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol] = []

        # Reindex the dataframes
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()

    def _get_new_bar(self, symbol: str) -> Iterator[Tuple[datetime, pd.Series]]:
        """
        Returns the latest bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume, adj_close).
        """
        for bar in self.symbol_data[symbol]:
            yield bar

    def get_latest_bar(self, symbol: str) -> Tuple[datetime, pd.Series]:
        """
        Returns the last bar from the latest_symbol list.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol: str, N: int = 1) -> List[Tuple[datetime, pd.Series]]:
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol: str) -> datetime:
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol: str, value_type: str) -> float:
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], value_type)

    def get_latest_bars_values(self, symbol: str, value_type: str, N: int = 1) -> np.ndarray:
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)  # bars_list = bars_list[-N:]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(bar[1], value_type) for bar in bars_list])

    def update_bars(self) -> None:
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())


'''
class HistoricMySQLDataHandler(DataManagement):
    """
    HistoricMySQLDataHandler is designed to read a MySQL database for each requested symbol from disk and 
    provide an interface to obtain the "latest" bar in a manner identical to a live trading interface.
    """

    def __init__(self, events, db_host, db_user, db_pass, db_name, symbol_list):

        """
        Initialises the historic data handler by requesting
        the location of the database and a list of symbols.
        It will be assumed that all price data is in a table called 
        'symbols', where the field 'symbol' is a string in the list.
        Parameters:
        events - The Event Queue.
        db_host - host of the database
        db_user - database user
        db_pass - password to access database
        db_name - database's name
        symbol_list - A list of symbol stringss
        """

        self.events = events
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name  

        self.symbol_list = symbol_list
        self.symbol_data = {}
        self.latest_symbol_data = {}

        self.continue_backtest = True
        self._data_conversion_from_database()


    def _get_data_from_database(self, symbol, columns):
        try:
            connection = MySQLdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, db=self.db_name)
        except MySQLdb.Error as e:  
            print("Error:%d:%s" % (e.args[0], e.args[1]))

        sql = SELECT {},{},{},{},{},{},{}
                FROM {}.format(columns[0],
                                    columns[1],
                                        columns[2],
                                            columns[3],
                                              columns[4],
                                                columns[5],
                                                    columns[6],
                                                        symbol)

        return pd.read_sql_query(sql, con=connection, index_col="datetime")

    def _data_conversion_from_database(self):
        """
        Opens the database files, converting them into 
        pandas DataFrames within a symbol dictionary.
        For this handler it will be assumed that the data is
        assumed to be stored in a database with similar columns 
        as the pandas dataframes. Thus, the format will be respected.
        """

        combined_index = None
        columns = ["datetime","open","high","low","close","volume","adj_close"]

        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self._get_data_from_database(symbol, columns)


            # Combine the index to pad forward values
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol] = []

        # Reindex the dataframes
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple of 
        (symbol, datetime, open, low, high, close, volume, adj_close).
        """
        for bar in self.symbol_data[symbol]:
            yield bar


    def get_latest_bar(self, symbol):
        """
        Returns the last bar from the latest_symbol list.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol, value_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
                print("That symbol is not available in the historical data set.")
                raise
        else:
            return getattr(bars_list[-1][1], value_type)


    def get_latest_bars_values(self, symbol, value_type, N=1):
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N) # bars_list = bars_list[-N:]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(bar[1], value_type) for bar in bars_list])

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())
'''
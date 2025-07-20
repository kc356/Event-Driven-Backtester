import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from Strategy import Strategy
from Events import SignalEvent, MarketEvent
from Strategies.Helper.CreateLaggedSeries import create_lagged_series
from typing import Any, Optional
from datetime import datetime


class ETFDailyForecastStrategy(Strategy):
    """
    S&P100 forecast strategy. It uses a Quadratic Discriminant
    Analyser to predict the returns for a subsequent time
    period and then generated long/exit signals based on the
    prediction.
    """

    def __init__(self, bars: Any, events: Any) -> None:
        """
        Initialises the buy and hold strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars: Any = bars
        self.symbol_list: list = self.bars.symbol_list
        self.events: Any = events

        # FIXME --> Here the models are fit on the training dataset only, especially here with the
        # regime change in 1st quarter 2020
        self.datetime_now: datetime = datetime.utcnow()
        self.model_start_date: datetime = datetime(2016, 1, 1, 0, 0, 0)
        self.model_end_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        self.model_start_test_date: datetime = datetime(2020, 1, 1, 0, 0, 0)
        self.model_interval: str = '1d'

        self.long_market: bool = False
        self.short_market: bool = False
        self.bar_index: int = 0

        self.model: QDA = self.create_symbol_forecast_model()

    """
    The model here is directly chosen, as for calculating inside the trading signals. For model choice,
    it's better to run a script outside of the backtest strategy. 
    """

    def create_symbol_forecast_model(self) -> QDA:
        # Create a lagged series of the S&P500 US stock market index
        df_ret: pd.DataFrame = create_lagged_series(self.symbol_list[0], self.model_start_date,
                                      self.model_end_date, self.model_interval, lags=5)

        # Use the prior two days of returns as predictor
        # values, with direction as the response
        X: pd.DataFrame = df_ret[["Lag1", "Lag2"]]
        Y: pd.Series = df_ret["Direction"]

        # Create training and test sets
        start_test: datetime = self.model_start_test_date
        X_train: pd.DataFrame = X[X.index < start_test]
        X_train = X[X.index > X.index[2]]  # avoid 2 nan values TODO --> filter one is timestamp other datetime index
        X_test: pd.DataFrame = X[X.index >= start_test]
        Y_train: pd.Series = Y[Y.index < start_test]
        Y_train = Y[Y.index > Y.index[2]]
        Y_test: pd.Series = Y[Y.index >= start_test]

        """
        Here we choose QDA, but the strategy would be dependent on different parameters.
        There is requirements to test the strategy with different models, k-fold cross validation,
        and also grid searching for parameters optimization
        """
        model: QDA = QDA()
        model.fit(X_train, Y_train)  # TODO --> The model could be fit on the whole dataset, this is on model validation
        return model

    def calculate_signals(self, event: MarketEvent) -> None:
        """
        Calculate the SignalEvents based on market data.
        """
        symbol: str = self.symbol_list[0]
        dt: datetime = self.datetime_now

        if isinstance(event, MarketEvent):
            self.bar_index += 1

            # make sure we wait 5 days to get the latest "bar" values
            if self.bar_index > 5:
                lags: np.ndarray = self.bars.get_latest_bars_values(self.symbol_list[0], "returns", N=3)

                # series of lags for 2 days prior
                pred_series: pd.Series = pd.Series(
                    {
                        "Lag1": lags[1] * 100.0,
                        "Lag2": lags[2] * 100.0
                    }
                )

                # reshape the array as it needs to be 2d
                pred_values: np.ndarray = pred_series.values.reshape(1, -1)
                pred: np.ndarray = self.model.predict(pred_values)

                # if price prediction is up and not LONG then BUY
                if pred > 0 and not self.long_market:
                    self.long_market = True
                    signal: SignalEvent = SignalEvent(symbol, dt, "LONG", 1.0)
                    self.events.put(signal)

                # if price prediction down and LONG then SELL
                if pred < 0 and self.long_market:
                    self.long_market = False
                    signal: SignalEvent = SignalEvent(symbol, dt, "EXIT", 1.0)
                    self.events.put(signal)

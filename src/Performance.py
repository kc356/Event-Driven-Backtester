from __future__ import print_function
import numpy as np
import pandas as pd
from typing import Tuple, Union


def create_sharpe_ratio(returns: pd.Series, periods: int = 252) -> float:
    """
    Create the Sharpe ratio for the strategy, based on a
    benchmark of zero (i.e. no risk-free rate information).
    Parameters:
    returns - A pandas Series representing period percentage returns.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """

    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_drawdowns(equity_curve: pd.Series) -> Tuple[pd.Series, float, float]:
    """
    Calculate the largest peak-to-trough drawdown of the equity curve
    as well as the duration of the drawdown. Requires that the
    equity_returns is a pandas Series.

    Parameters:
    equity_curve - A pandas Series representing period percentage returns.
    Returns:
    drawdown, duration - Highest peak-to-trough drawdown and duration.
    """

    # Calculate the cumulative returns curve and set up the High Water Mark
    high_water_mark: list = [0]
    # Create the drawdown and duration series
    idx = equity_curve.index
    drawdown: pd.Series = pd.Series(index=idx)
    duration: pd.Series = pd.Series(index=idx)
    # Loop over the index range
    for i in range(1, len(idx)):
        high_water_mark.append(max(high_water_mark[i - 1], equity_curve.iloc[i]))
        drawdown.iloc[i] = high_water_mark[i] - equity_curve.iloc[i]
        duration.iloc[i] = 0 if drawdown.iloc[i] == 0 else duration.iloc[i - 1] + 1
    return drawdown, drawdown.max(), duration.max()

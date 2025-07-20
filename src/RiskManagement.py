from __future__ import print_function
from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd


class RiskManagement(object):
    """
    RiskManagement class would be necessary for different things:
    - Risk calculation on position (such as VaR)
    - Calculation/Update of correlation matrix for the different positions
    This would require different methods if the Universe is to big (NxN) matrix
        --> Be careful if data is sparse
        --> Find factors such as calculating NxF with F < N and F particular factors

    - Position sizing, for better capital management (leverage, weight between portfolios)
        --> Kelly Criterion?
        --> Markowitz theory?
    """
    
    def __init__(self, portfolio_value: float = 100000.0, max_position_size: float = 0.1) -> None:
        """
        Initialize risk management parameters.
        
        Parameters:
        portfolio_value - Total portfolio value
        max_position_size - Maximum position size as fraction of portfolio (0.1 = 10%)
        """
        self.portfolio_value: float = portfolio_value
        self.max_position_size: float = max_position_size

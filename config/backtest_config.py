"""
Configuration settings for backtesting.
"""

from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class BacktestConfig:
    """Configuration class for backtest parameters."""
    
    # Data settings
    symbol_list: List[str]
    start_date: datetime
    end_date: datetime
    interval: str = '1d'
    
    # Capital and execution settings
    initial_capital: float = 100000.0
    heartbeat: float = 0.0
    
    # Data source settings
    data_dir: str = 'DataDir'
    use_yahoo_data: bool = True
    
    # Strategy settings
    strategy_name: str = 'ETF_Forecast'
    
    # Risk management settings
    max_position_size: float = 0.1  # 10% of portfolio
    stop_loss: float = 0.05  # 5% stop loss
    take_profit: float = 0.15  # 15% take profit


# Default configurations
DEFAULT_CONFIG = BacktestConfig(
    symbol_list=['TQQQ'],
    start_date=datetime(2016, 1, 1, 0, 0, 0),
    end_date=datetime(2021, 1, 1, 0, 0, 0),
    interval='1d',
    initial_capital=100000.0,
    heartbeat=0.0,
    data_dir='DataDir',
    use_yahoo_data=True,
    strategy_name='ETF_Forecast'
)

# Strategy configurations
STRATEGY_CONFIGS = {
    'ETF_Forecast': {
        'model_start_date': datetime(2016, 1, 1, 0, 0, 0),
        'model_end_date': datetime(2021, 1, 1, 0, 0, 0),
        'model_start_test_date': datetime(2020, 1, 1, 0, 0, 0),
        'lags': 5
    },
    'MAC_Strat': {
        'short_window': 100,
        'long_window': 400
    },
    'Buy_And_Hold': {
        # No specific parameters needed
    }
} 
from Strategy import Strategy
from Events import MarketEvent, SignalEvent
from typing import Dict, Any
import datetime


class BuyAndHoldStrat(Strategy):
    """
    This is an extremely simple strategy that goes LONG all of the 
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.
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

        # Once buy & hold signal is given, these are set to True
        self.bought: Dict[str, bool] = self._calculate_initial_bought()

    def _calculate_initial_bought(self) -> Dict[str, bool]:
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to False.
        """
        bought: Dict[str, bool] = {symbol: False for symbol in self.symbol_list}
        return bought

    def calculate_signals(self, event: MarketEvent) -> None:
        """
        For "Buy and Hold" we generate a single signal per symbol
        and then no additional signals. This means we are 
        constantly long the market from the date of strategy
        initialisation.

        Parameters
        event - A MarketEvent object. 
        """
        strength: float = 1.0
        if isinstance(event, MarketEvent):
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bar(symbol)
                if bars is not None and bars != []:

                    dt: datetime.datetime = datetime.datetime.utcnow()

                    if not self.bought[symbol]:
                        # (Symbol, Datetime, Type = LONG, SHORT or EXIT, Signal strength)
                        signal: SignalEvent = SignalEvent(symbol, dt, "LONG", strength)
                        self.events.put(signal)
                        self.bought[symbol] = True

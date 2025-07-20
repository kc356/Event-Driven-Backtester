from typing import Optional, Union
from datetime import datetime


class Event(object):
    """
    Event is base class providing an interface for all subsequent 
    (inherited) events, that will trigger further events in the 
    trading infrastructure.   
    """
    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """

    def __init__(self) -> None:
        """
        Initialises the MarketEvent.
        """
        self.type: str = "MARKET"


class SignalEvent(Event):
    """
    Signal event generated from a particular strategy, if signal met strategy conditions

    Parameters:
    symbol - The symbol for current asset.
    datetime - A datetime at which the signal is generated.
    signal_type - The signal type ('LONG', 'SHORT', 'EXIT')
    strength - strength of the signal --> TODO: this should be given from a risk class when applying multiple strats
    """

    def __init__(self, symbol: str, datetime: datetime, signal_type: str, strength: float) -> None:
        self.type: str = "SIGNAL"
        self.symbol: str = symbol
        self.datetime: datetime = datetime
        self.signal_type: str = signal_type
        self.strength: float = strength


class OrderEvent(Event):
    """
    Order event to be sent to a broker api. It takes into account the quantity,
    type of ordering, and direction (long, short, exit...)

    Parameters:
    symbol - The symbol for current asset.
    order_type - Whether is it a 'MARKET' or 'LIMIT' order
    quantity --> TODO: this should be implemented in a risk class (Kelly Criterion, etc)
    direction - 1 or -1 based on the type
    """

    def __init__(self, symbol: str, order_type: str, quantity: int, direction: int) -> None:
        self.type: str = "ORDER"
        self.symbol: str = symbol
        self.order_type: str = order_type
        self.quantity: int = quantity
        self.direction: int = direction

    def print_order(self) -> None:
        """
        Outputs the values within the Order.
        """
        print("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s") % \
        (self.symbol, self.order_type, self.quantity, self.direction)


class FillEvent(Event):
    """
    Fill event once an order based on the response from the broker

    Parameters:
    datetime - A datetime at which the signal is created.
    symbol - The symbol for current asset.
    exchange - The exchange, broker where the order is filled
    quantity - quantity filled
    direction
    fill_cost - can contain commission already
    commission - Defaulted to None if non specified
    """

    def __init__(self, datetime: datetime, symbol: str, exchange: str, 
                 quantity: int, direction: int, fill_cost: float, 
                 commission: Optional[float] = None) -> None:

        self.type: str = "FILL"
        self.datetime: datetime = datetime
        self.symbol: str = symbol
        self.exchange: str = exchange
        self.quantity: int = quantity
        self.direction: int = direction
        self.fill_cost: float = fill_cost

        # Calculate commission
        if commission is None:
            self.commission: float = self._calculate_commission()
        else:
            self.commission: float = commission

    def _calculate_commission(self) -> float:
        """
        TODO: Commission fees to be implemented
        """
        # between 1 and 2%
        return max(1.5, 0.015 * self.quantity)

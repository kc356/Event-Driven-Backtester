from abc import ABCMeta, abstractmethod
from typing import Any, Optional
from .Events import FillEvent, OrderEvent
from datetime import datetime


class ExecutionHandler(object):
    """
    Execution handler class to handle Order and Fill events
    for different types of APIs (brokers, exchanges), or protocols such as FIX
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event: OrderEvent) -> None:
        """
        Takes an Order event and executes it, producing
        a Fill event that gets placed onto the Events queue.

        Parameters:
        event - Contains an Event object with order information.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimpleSimulatedExecutionHandler(ExecutionHandler):
    """
    Simple handler with no latency or slippage modelling
    """

    def __init__(self, events: Any) -> None:
        """
        Initialises the handler, setting the event queues
        up internally.

        Parameters:
        events - The Queue of Event objects.
        """
        self.events: Any = events

    def execute_order(self, event: OrderEvent) -> None:
        """
        Order event converted to Fill event to
        execute the order on "live" broker. The event is
        then added to the queue

        Parameters:
        event - Contains an Event object with order information.
        """

        if isinstance(event, OrderEvent):
            fill_event: FillEvent = FillEvent(datetime.utcnow(), event.symbol, "FAKE_EXCHANGE", event.quantity, event.direction, float("nan"))
            self.events.put(fill_event)

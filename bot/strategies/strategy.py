from abc import ABC, abstractmethod

from bot.orderbook import OrderBook

class Strategy(ABC):
    @abstractmethod
    def run(self, asset_id: str, orderbook: OrderBook):
        ...


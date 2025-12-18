from abc import ABC, abstractmethod

from bot.orderbook import OrderBook

class Strategy(ABC):
    @abstractmethod
    def run(self, asset_id: str, orderbook: OrderBook):
        ...

    @abstractmethod
    def get_asset_ids(self) -> list[str]:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

from abc import ABC, abstractmethod

from bot.common.types.common import AssetIdentifier
from bot.orderbook import OrderBook

class Strategy(ABC):
    @abstractmethod
    def run(self, asset_id: str, order_book: OrderBook):
        ...

    @abstractmethod
    def get_asset_ids(self) -> list[AssetIdentifier]:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

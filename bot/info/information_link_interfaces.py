from typing import Protocol

from bot.common.messages.websocket import (
    OrderBookSummary,
    PriceChange,
    TickSizeChange,
    LastTradePrice,
)


class DataConsumer(Protocol):
    def on_order_book_summary_event(self, asset_id: str, event: OrderBookSummary):
        ...

    def on_price_change_event(self, asset_id: str, event: PriceChange, timestamp: int):
        ...

    def on_tick_size_change_event(self, asset_id: str, event: TickSizeChange):
        ...

    def on_last_trade_price_event(self, asset_id: str, event: LastTradePrice):
        ...


class DataProvider(Protocol):
    def subscribe_to_data(self, asset_id: int, consumer: DataConsumer):
        ...


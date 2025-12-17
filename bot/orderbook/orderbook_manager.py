from .orderbook import OrderBook
from .orderbook_fanout_interface import OrderBookConsumer, OrderBookFanoutInterface

from bot.info.information_link_interfaces import DataConsumer, DataProvider
from bot.common.messages.websocket import (
    OrderBookSummary,
    PriceChange,
    TickSizeChange,
    LastTradePrice,
)

from collections import defaultdict

class OrderManager(OrderBookFanoutInterface, DataConsumer):
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
    
        self.order_books: dict[str, OrderBook] = {} # Asset id -> Order Book

        # Asset id -> List of consumers
        self.order_book_subscribers: dict[str, list[OrderBookConsumer]] = defaultdict(list)

    def create_order_book(self, asset_id: str):
        self.order_books[asset_id] = OrderBook()

        self.data_provider.subscribe_to_data(asset_id, self)

    def get_order_book(self, asset_id: str) -> OrderBook:
        return self.order_books[asset_id]


    def on_order_book_summary_event(self, asset_id: str, event: OrderBookSummary):
        if asset_id not in self.order_books:
            return
        
        order_book = self.get_order_book(asset_id)
        order_book.apply_book_snapshot(
            bids=[(bid.price, bid.size) for bid in event.bids],
            asks=[(ask.price, ask.size) for ask in event.asks],
            ts=event.timestamp,
            book_hash=event.hash,
        )

        self._push_order_book_update(asset_id)


    def on_price_change_event(self, asset_id: str, event: PriceChange):
        if asset_id not in self.order_books:
            return
        
        order_book = self.get_order_book(asset_id)
        order_book.apply_price_change(event.best_ask, event.best_bid, event.timestamp)

        self._push_order_book_update(asset_id)


    def on_tick_size_change_event(self, asset_id: str, event: TickSizeChange):
        if asset_id not in self.order_books:
            return

        order_book = self.get_order_book(asset_id)
        order_book.update_tick_size(event.new_tick_size)

        self._push_order_book_update(asset_id)

    def on_last_trade_price_event(self, asset_id: str, event: LastTradePrice):
        if asset_id not in self.order_books:
            return

        order_book = self.get_order_book(asset_id)
        order_book.update_last_trade_price(event.price)

        self._push_order_book_update(asset_id)

    def _push_order_book_update(self, asset_id: str):
        order_book = self.get_order_book(asset_id)
        for consumer in self.order_book_subscribers[asset_id]:
            consumer.on_order_book_update(asset_id, order_book)

    def subscribe_to_order_book(self, asset_id: str, consumer: OrderBookConsumer):
        if asset_id not in self.order_books:
            self.create_order_book(asset_id)
        
        self.order_book_subscribers[asset_id].append(consumer)



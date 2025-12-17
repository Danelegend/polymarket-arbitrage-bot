from typing import Protocol

from .orderbook import OrderBook

class OrderBookConsumer(Protocol):
  def on_order_book_update(self, asset_id: str, order_book: OrderBook):
    ...


class OrderBookFanoutInterface(Protocol):
  def subscribe_to_order_book(self, asset_id: str, consumer: OrderBookConsumer):
    ...
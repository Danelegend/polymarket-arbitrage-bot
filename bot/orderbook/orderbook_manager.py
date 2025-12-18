from typing import Optional

from .orderbook import OrderBook

class OrderManager():
    def __init__(self):
        self.order_books: dict[str, OrderBook] = {} # Asset id -> Order Book

    def create_order_book(self, asset_id: str):
        self.order_books[asset_id] = OrderBook()

    def get_order_book(self, asset_id: str) -> Optional[OrderBook]:
        if asset_id not in self.order_books:
            return None

        return self.order_books[asset_id]


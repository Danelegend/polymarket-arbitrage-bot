from decimal import Decimal
from bot.orderbook import (
    OrderBookConsumer,
    OrderBookFanoutInterface,
    OrderBook
)

from enum import Enum

import logging

logger = logging.getLogger(__name__)

class Side(Enum):
    BUY = "buy"
    SELL = "sell"


class ArbitrageStrategy(OrderBookConsumer):
    def __init__(
        self, 
        asset_ids: list[str],
        orderbook_fanout: OrderBookFanoutInterface,    
    ):
        self.assets = asset_id
        self.asset_order_books: dict[str, OrderBook] = {}

        for asset_id in asset_ids:
            orderbook_fanout.subscribe_to_order_book(asset_id, self)


    def on_order_book_update(
        self,
        asset_id: str,
        order_book: OrderBook,
    ):
        self.asset_order_books[asset_id] = order_book

        if not self._can_run_strategy():
            return


    def _can_run_strategy(self) -> bool:
        # Check that we have an order book for each asset
        return len(self.assets) == len(self.asset_order_books)

    def _run_strategy(self):
        order_books = self.asset_order_books.values()

        if check_for_arb(Side.BUY, order_books):
            logger.info(f"BUY ARBITRAGE for {self.assets}")

        if check_for_arb(Side.SELL, order_books):
            logger.info(f"SELL ARBITRAGE for {self.assets}")


def check_for_arb(side: Side, order_books: list[OrderBook]):
    best_top_levels = [order_book.get_best_bid() if side == Side.BUY else order_book.get_best_ask() for order_book in order_books]

    return get_top_level_sum(best_top_levels) - 1 != 0


def get_top_level_sum(best_top_levels: list[Decimal]) -> Decimal:
    return sum(best_top_levels)


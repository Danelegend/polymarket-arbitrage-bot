"""
The channel is the central orchestrator

What it does:
 -> It handles the inbound message pipeline
 -> It handles the outbound message pipeline
 -> Handles the overall state
"""

from bot.orderbook import OrderManager

from bot.info.information_link_interfaces import DataConsumer, DataProvider
from bot.strategies.strategy import Strategy
from bot.common.messages.websocket import (
    OrderBookSummary,
    PriceChange,
    TickSizeChange,
    LastTradePrice,
)
from bot.orderbook import OrderBook

from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

class Channel(DataConsumer):
    def __init__(
        self,
        data_provider: DataProvider
    ):
        self.data_provider = data_provider

        self.orderbook_manager = OrderManager()
        self.strategies: dict[int, Strategy] = {}

        self.asset_strategy_map: dict[str, list[int]] = defaultdict(list)

    def add_strategy(self, strategy: Strategy):
        strategy_id = len(self.strategies) + 1
        self.strategies[strategy_id] = strategy

        for asset in strategy.get_asset_ids():
            asset_id = asset.asset_id
            self.asset_strategy_map[asset_id].append(strategy_id)
            self.add_asset(asset_id)

    def add_asset(self, asset_id: str):
        self.orderbook_manager.create_order_book(asset_id)
        self.subscribe_to_instrument_updates(asset_id)

    def subscribe_to_instrument_updates(self, asset_id: str):
        self.data_provider.subscribe_to_data(asset_id, self)

    def on_order_book_summary_event(self, asset_id: str, event: OrderBookSummary):
        orderbook = self.orderbook_manager.get_order_book(asset_id)

        if orderbook is None:
            return

        orderbook.apply_book_snapshot(
            bids=[(bid.price, bid.size) for bid in event.bids],
            asks=[(ask.price, ask.size) for ask in event.asks],
            ts=event.timestamp,
            book_hash=event.book_hash,
        )

        self._on_orderbook_update(asset_id, orderbook)

    def on_price_change_event(self, asset_id: str, event: PriceChange, timestamp: int):
        orderbook = self.orderbook_manager.get_order_book(asset_id)

        if orderbook is None:
            logger.info("No order book found")
            return

        orderbook.apply_price_change(event.best_bid, event.best_ask, timestamp)

        self._on_orderbook_update(asset_id, orderbook)


    def on_tick_size_change_event(self, asset_id: str, event: TickSizeChange):
        orderbook = self.orderbook_manager.get_order_book(asset_id)

        if orderbook is None:
            return

        orderbook.update_tick_size(event.new_tick_size)


    def on_last_trade_price_event(self, asset_id: str, event: LastTradePrice):
        orderbook = self.orderbook_manager.get_order_book(asset_id)

        if orderbook is None:
            return

        orderbook.update_last_trade_price(event.price)

    def _on_orderbook_update(self, asset_id: str, orderbook: OrderBook):
        for strategy in self.strategies:
            strategy.run(asset_id, orderbook)

        logger.info(f"Orderbook updated for asset_id={asset_id}, best_bid={orderbook.get_best_bid()}, best_ask={orderbook.get_best_ask()}")

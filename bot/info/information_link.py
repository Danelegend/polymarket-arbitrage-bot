from bot.polymarket.ws_connection import PolyMarketWebSocketConnection
from collections import defaultdict

from bot.polymarket.market_data_interface import MarketDataHandlerInterface
from bot.common.messages.websocket import (
    OrderBookSummaryEvent,
    PriceChangeEvent,
    TickSizeChangeEvent,
    LastTradePriceEvent,
)
from bot.ids.ids_interface import IdsInterface

from .information_link_interfaces import DataConsumer, DataProvider

import logging

logger = logging.getLogger(__name__)

class InfoLink(DataProvider, MarketDataHandlerInterface):
    def __init__(self):
        # asset_id -> list of subscribers
        self.subscribers: dict[int, list[DataConsumer]] = defaultdict(list)
        self.polymarket_connection = PolyMarketWebSocketConnection(self)

        self.subscribed_markets: set[int] = set()

    def start(self):
        self.polymarket_connection.run()

    def subscribe_to_data(self, asset_id: int, consumer: DataConsumer):
        logger.info(f"Subscription request for asset={asset_id}")
        
        self.subscribers[asset_id].append(consumer)

        self._subscribe_to_market(
            asset_id
        )
        
    def _subscribe_to_market(self, market_id: int):
        if market_id in self.subscribed_markets:
            return

        logger.info(f"Subscribing to data for asset={market_id}")

        self.subscribed_markets.add(market_id)
        self.polymarket_connection.subscribe_to_market(market_id)

    def handle_order_book_summary_event(self, event: OrderBookSummaryEvent):
        token_id = event.token_id

        logger.debug(f"{token_id}")

        if token_id not in self.subscribers:
            return

        for consumer in self.subscribers[token_id]:
            consumer.on_order_book_summary_event(token_id, event)


    def handle_price_change_event(self, event: PriceChangeEvent):
        for pc in event.price_changes:
            token_id = pc.token_id

            logger.debug(f"{token_id}")

            if token_id not in self.subscribers:
                continue

            for consumer in self.subscribers[token_id]:
                consumer.on_price_change_event(token_id, pc, event.timestamp)

    def handle_tick_size_change_event(self, event: TickSizeChangeEvent):
        token_id = event.token_id

        if token_id not in self.subscribers:
            return

        for consumer in self.subscribers[token_id]:
            consumer.on_tick_size_change_event(token_id, event)


    def handle_last_trade_price_event(self, event: LastTradePriceEvent):
        token_id = event.token_id

        if token_id not in self.subscribers:
            return

        for consumer in self.subscribers[token_id]:
            consumer.on_last_trade_price_event(token_id, event)
    

from decimal import Decimal

from bot.common.types.common import AssetIdentifier
from bot.strategies.strategy import Strategy
from bot.orderbook import OrderBook

from enum import Enum

import logging

logger = logging.getLogger(__name__)

class Side(Enum):
    BUY = "buy"
    SELL = "sell"


class ArbitrageStrategy(Strategy):
    def __init__(
        self, 
        asset_ids: list[AssetIdentifier],  
    ):
        self.assets: dict[str, AssetIdentifier] = {
            str(asset.asset_id): asset
            for asset in asset_ids
        }
        self.asset_order_books: dict[str, OrderBook] = {}

    def run(self, asset_id: str, order_book: OrderBook):
        self.asset_order_books[asset_id] = order_book

        if not self._can_run_strategy():
            return

        self._run_strategy()

    def get_asset_ids(self) -> list[AssetIdentifier]:
        return list(self.assets.values())

    def _can_run_strategy(self) -> bool:
        # Check that we have an order book for each asset
        return len(self.assets) == len(self.asset_order_books)

    def _run_strategy(self):
        order_books = list(self.asset_order_books.values())

        if check_for_arb(Side.BUY, order_books):
            logger.info(f"BUY ARBITRAGE for {self.assets.keys()}")

        if check_for_arb(Side.SELL, order_books):
            logger.info(f"SELL ARBITRAGE for {self.assets.keys()}")

        string_builder1 = f"Market={next(iter(self.assets.values())).market_name}"
        string_builder2 = string_builder1

        for asset_id, orderbook in self.asset_order_books.items():
            asset_identifier = self.assets[asset_id]
            string_builder1 += f"{asset_identifier.market_outcome}={orderbook.get_best_bid()}, "
            string_builder2 += f"{asset_identifier.market_outcome}={orderbook.get_best_ask()}, "

        logger.info(string_builder1)
        logger.info(string_builder2)

    def __str__(self) -> str:
        return f"ArbitrageStrategy({self.assets})"


def check_for_arb(side: Side, order_books: list[OrderBook]):
    best_top_levels: list[Decimal] = []

    for orderbook in order_books:
        match side:
            case Side.BUY:
                best_bid = orderbook.get_best_bid()

                if best_bid is None:
                    return False

                best_top_levels.append(Decimal(best_bid))
            case Side.SELL:
                best_ask = orderbook.get_best_ask()

                if best_ask is None:
                    return False

                best_top_levels.append(Decimal(best_ask))

    total = get_top_level_sum(best_top_levels)

    return total - 1 < 0 if side == Side.BUY else total - 1 > 0


def get_top_level_sum(best_top_levels: list[Decimal]) -> Decimal:
    return Decimal(sum(best_top_levels))


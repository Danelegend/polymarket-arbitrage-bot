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
            logger.info(
                f"BUY ARBITRAGE for Market={get_market_name(self.assets)}, assets={list(self.assets.keys())}"
            )

        if check_for_arb(Side.SELL, order_books):
            logger.info(f"SELL ARBITRAGE for Market={get_market_name(self.assets)}, assets={list(self.assets.keys())}")

        string_builder1 = f"Market={get_market_name(self.assets)}, assets={list(self.assets.keys())}"
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
    return (
        should_hit_bids([to_decimal(ob.get_best_bid()) for ob in order_books]) 
        if side == Side.BUY else
        should_hit_asks([to_decimal(ob.get_best_ask()) for ob in order_books])
    )



def get_market_name(assets: dict[str, AssetIdentifier]) -> str:
    return next(iter(assets.values())).market_name


def should_hit_bids(best_bids: list[Decimal], fee: float = 0.0) -> bool:
    """
    Returns True if selling 1 unit of each outcome at the given bids
    yields risk-free profit.

    best_bids: list of best bid prices (e.g. [yes_bid, no_bid])
    fee: total fee per unit round-trip (optional)
    """
    return sum(best_bids) > 1 + fee

def should_hit_asks(best_asks: list[Decimal], fee: float = 0.0) -> bool:
    """
    Returns True if selling 1 unit of each outcome at the given bids
    yields risk-free profit.

    best_bids: list of best bid prices (e.g. [yes_bid, no_bid])
    fee: total fee per unit round-trip (optional)
    """
    return sum(best_asks) < 1 + fee

def to_decimal(num: float | None) -> Decimal:
    return Decimal(num) if num is not None else Decimal('Infinity')
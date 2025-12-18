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

FEE_PER_LEG = Decimal("0.0015")     # 0.15% per trade
SLIPPAGE_BUFFER = Decimal("0.002")  # execution risk
MIN_EDGE = Decimal("0.001")         # required profit (0.1%)


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
        should_hit_bids([to_decimal(ob.get_best_bid(), negative_infinity=True) for ob in order_books]) 
        if side == Side.BUY else
        should_hit_asks([to_decimal(ob.get_best_ask()) for ob in order_books])
    )



def get_market_name(assets: dict[str, AssetIdentifier]) -> str:
    return next(iter(assets.values())).market_name


def should_hit_bids(
    best_bids: list[Decimal],
    fee_per_leg: Decimal = FEE_PER_LEG,
    slippage_buffer: Decimal = SLIPPAGE_BUFFER,
    min_edge: Decimal = MIN_EDGE,
) -> bool:
    """
    Returns True if selling 1 unit of each outcome at the given bids
    yields guaranteed profit after fees and buffers.
    """
    if not best_bids:
        return False

    gross_credit = sum(best_bids)

    # Fees paid on both legs
    fee_cost = gross_credit * fee_per_leg * Decimal(len(best_bids))

    effective_credit = gross_credit - fee_cost - slippage_buffer

    net_pnl = effective_credit - Decimal("1")

    return net_pnl >= min_edge


def should_hit_asks(
    best_asks: list[Decimal],
    fee_per_leg: Decimal = FEE_PER_LEG,
    slippage_buffer: Decimal = SLIPPAGE_BUFFER,
    min_edge: Decimal = MIN_EDGE,
) -> bool:
    """
    Returns True if buying 1 unit of each outcome at the given asks
    yields guaranteed profit after fees and buffers.
    """
    if not best_asks:
        return False

    raw_cost = sum(best_asks)

    # Fees paid on both legs
    fee_cost = raw_cost * fee_per_leg * Decimal(len(best_asks))

    effective_cost = raw_cost + fee_cost + slippage_buffer

    net_pnl = Decimal("1") - effective_cost

    return net_pnl >= min_edge


def to_decimal(num: float | None, negative_infinity: bool = False) -> Decimal:
    return Decimal(num) if num is not None else Decimal('-Infinity' if negative_infinity else 'Infinity')
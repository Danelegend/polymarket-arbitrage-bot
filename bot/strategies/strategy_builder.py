import json

from typing import Generator

from .arbitrage.arbitrage_strategy import ArbitrageStrategy

from bot.common.types.ids import MarketInformation


def build_arbitrage_strategy(market: MarketInformation):
    return ArbitrageStrategy(
        [str(asset_id) for asset_id in market.asset_ids], 
    )


def build_strategies(tradable_markets: list[MarketInformation]) -> Generator[ArbitrageStrategy, None, None]:
    for market in tradable_markets:
        yield build_arbitrage_strategy(market)


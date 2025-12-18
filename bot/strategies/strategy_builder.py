import json

from typing import Generator

from .arbitrage.arbitrage_strategy import ArbitrageStrategy

from bot.common.types.common import AssetIdentifier
from bot.common.types.ids import MarketInformation


def build_arbitrage_strategy(market: MarketInformation):
    asset_identifiers = []
    
    for i in range(0, len(market.outcomes)):
        asset_id = market.token_ids[i]
        outcome = market.outcomes[i]

        asset_identifiers.append(
            AssetIdentifier(
                market_name=market.name,
                market_outcome=outcome,
                asset_id=asset_id
            )
        )
    
    return ArbitrageStrategy(
        asset_identifiers,
    )


def build_strategies(tradable_markets: list[MarketInformation]) -> Generator[ArbitrageStrategy, None, None]:
    for market in tradable_markets:
        yield build_arbitrage_strategy(market)


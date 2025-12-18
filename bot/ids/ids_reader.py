from typing import Generator

from bot.common.types.ids import MarketInformation, TradeableMarket
from .constants import MARKET_OUTPUT_FILE, TRADABLE_MARKETS_OUTPUT_FILE

def read_markets() -> Generator[MarketInformation, None, None]:
    with open(MARKET_OUTPUT_FILE, 'r') as f:
        for line in f:
            yield MarketInformation(**line) 

def read_tradeable_markets() -> list[TradeableMarket]:
    with open(TRADABLE_MARKETS_OUTPUT_FILE, 'r') as f:
        return [TradeableMarket(**line) for line in f]

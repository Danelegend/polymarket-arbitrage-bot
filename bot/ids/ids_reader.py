from bot.common.types.ids import MarketInformation, TradeableMarket
from .constants import MARKET_OUTPUT_FILE, TRADABLE_MARKETS_OUTPUT_FILE

def read_markets() -> list[MarketInformation]:
    with open(MARKET_OUTPUT_FILE, 'r') as f:
        return [MarketInformation(**line) for line in f]

def read_tradeable_markets() -> list[TradeableMarket]:
    with open(TRADABLE_MARKETS_OUTPUT_FILE, 'r') as f:
        return [TradeableMarket(**line) for line in f]

from .ids_interface import IdsInterface
from .ids_reader import read_markets, read_tradeable_markets

from bot.common.types.ids import MarketInformation

class IdsClient(IdsInterface):
    def __init__(self):
        return

    def get_market_for_event(self, event_id: int) -> MarketInformation:
        tradable_markets = read_tradeable_markets()

        for market in tradable_markets:
            if event_id in market.tradeable_events:
                return self.get_market(market.tradeable_market_id)


    def get_market(self, market_id: int) -> MarketInformation:
        for market in read_markets():
            if market.id == market_id:
                return market


    def get_tradable_markets(self) -> list[MarketInformation]:
        tradable_markets = read_tradeable_markets()

        return [self.get_market(market.tradeable_market_id) for market in tradable_markets]


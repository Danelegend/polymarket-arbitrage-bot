from typing import Protocol

from bot.common.types.ids import MarketInformation

class IdsInterface(Protocol):
    def get_market_for_event(self, event_id: int) -> MarketInformation:
        ...

    def get_market(self, market_id: int) -> MarketInformation:
        ...

    
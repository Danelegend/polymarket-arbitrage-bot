from bot.common.types.ids import MarketInformation, EventInformation, TradeableMarket

def serialise_market(market: MarketInformation) -> str:
    return market.json()

def serialise_event_information(event: EventInformation) -> str:
    return event.json()

def serialise_tradeable_market(tradeable_market: TradeableMarket) -> str:
    return tradeable_market.json()
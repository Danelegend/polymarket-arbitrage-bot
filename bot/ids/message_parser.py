from bot.common.types.ids import MarketInformation, EventInformation, TradeableMarket
from bot.common.messages.gamma import GammaMarket, Event

def parse_market(market: GammaMarket) -> MarketInformation:
    return MarketInformation(
        id=market.id,
        question_id=market.question_id,
        slug=market.slug,
        question=market.question,
        category=market.category,
        start_date=market.start_date,
        end_date=market.end_date,
        creation_date=market.created_at,
        active=market.active,
        new=market.new or False,
        volume=market.volume,
        events=[parse_event(e) for e in market.events],
    )

def parse_event(event: Event) -> EventInformation:
    return EventInformation(
        id=event.id,
        ticker=event.ticker,
        slug=event.slug,
        title=event.title,
        description=event.description,
        start_date=event.start_date,
        end_date=event.end_date,
        creation_date=event.created_at,
        active=event.active,
        new=event.new or False,
        volume_1mo=event.volume_1mo,
        volume_1wk=event.volume_1wk,
        volume_24hr=event.volume_24hr,
    )

def to_tradeable_market(market: MarketInformation) -> TradeableMarket:
    return to_tradeable_market(market, market.events)

def to_tradeable_market(market: MarketInformation, tradeable_events: list[EventInformation]) -> TradeableMarket:
    return TradeableMarket(
        tradeable_market_id=market.id,
        tradeable_events=[e.id for e in tradeable_events],
    )

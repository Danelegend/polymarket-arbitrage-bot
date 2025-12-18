from datetime import datetime

from pydantic import BaseModel


class EventInformation(BaseModel):
    """
    An Event is a tradeable asset
    """
    id: int
    ticker: str
    slug: str
    title: str
    description: str

    start_date: datetime
    end_date: datetime
    creation_date: datetime

    active: bool
    new: bool

    volume_1mo: float
    volume_1wk: float
    volume_24hr: float


class MarketInformation(BaseModel):
    """
    A Market is composed of one or multiple events
    """
    id: str
    question_id: str
    slug: str
    question: str

    category: str

    start_date: datetime
    end_date: datetime
    creation_date: datetime

    active: bool
    new: bool

    volume: float

    outcomes: list[str]
    token_ids: list[str]

    events: list[EventInformation]


class TradeableMarket(BaseModel):
    tradeable_market_id: str
    tradeable_events: list[int]

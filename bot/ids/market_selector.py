from bot.common.types.ids import MarketInformation, EventInformation

from dataclasses import dataclass
from typing import Callable, Any, Generic, TypeVar

L = TypeVar("L")  # left-hand side (attribute type)
R = TypeVar("R")  # right-hand side (comparison value type)


@dataclass(frozen=True)
class Condition(Generic[L]):
    attribute: str
    predicate: Callable[[L], bool]


def is_valid(obj: Any, conditions: list[Condition[Any]]) -> bool:
    return all(
        condition.predicate(
            getattr(obj, condition.attribute)
        )
        for condition in conditions
    )

def market_valid(market: MarketInformation, conditions: list[Condition[Any]]) -> bool:
    return is_valid(market, conditions)

def event_valid(event: EventInformation, conditions: list[Condition[Any]]) -> bool:
    return is_valid(event, conditions)

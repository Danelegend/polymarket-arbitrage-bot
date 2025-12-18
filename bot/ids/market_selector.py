from bot.common.messages.gamma import Event
from bot.common.messages.gamma import GammaMarket
from dataclasses import dataclass
from typing import Callable, Any, Generic, TypeVar

L = TypeVar("L")  # left-hand side (attribute type)
R = TypeVar("R")  # right-hand side (comparison value type)


@dataclass(frozen=True)
class Condition(Generic[L, R]):
    attribute: str
    operator: Callable[[L, R], bool]
    value: R


def is_valid(obj: Any, conditions: list[Condition[Any, Any]]) -> bool:
    return all(
        condition.operator(
            getattr(obj, condition.attribute),
            condition.value
        )
        for condition in conditions
    )

def market_valid(market: GammaMarket, conditions: list[Condition[Any, Any]]) -> bool:
    return is_valid(market, conditions)

def event_valid(event: Event, conditions: list[Condition[Any, Any]]) -> bool:
    return is_valid(event, conditions)

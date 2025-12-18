from bot.common.messages.gamma import GammaMarket, Event

from dataclasses import dataclass
from typing import TypeVar, FunctionType

T = TypeVar('T')

@dataclass
class Condition[T]:
    artibute: str
    operator: FunctionType[T, T, bool]
    value: T


def market_valid(market: GammaMarket, conditions: list[Condition[T]]) -> bool:
    return all(
        condition.operator(
            getattr(
                market, 
                condition.artibute
            ), 
            condition.value
        ) for condition in conditions
    )

def event_valid(event: Event, conditions: list[Condition[T]]) -> bool:
    return all(
        condition.operator(
            getattr(
                event, 
                condition.artibute
            ), 
            condition.value
        ) for condition in conditions
    )

    
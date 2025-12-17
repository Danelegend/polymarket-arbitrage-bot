import json

from typing import Generator

from .arbitrage.arbitrage_strategy import ArbitrageStrategy

from bot.orderbook import OrderBookFanoutInterface
from pydantic import BaseModel

ARBITRAGE_STRATEGY_FILE = "arbitrage_strategies.json"

class ArbitrageStrategyConfig(BaseModel):
    name: str
    market_id: str
    asset_ids: list[int]


def load_arbitrage_strategies() -> Generator[ArbitrageStrategyConfig, None, None]:
    with open(ARBITRAGE_STRATEGY_FILE, "r") as f:
        for config in json.load(f):
            yield ArbitrageStrategyConfig(**config)


def build_strategies(order_book_fanout_interface: OrderBookFanoutInterface) -> Generator[ArbitrageStrategy, None, None]:
    for config in load_arbitrage_strategies():
        yield ArbitrageStrategy(
            [str(asset_id) for asset_id in config.asset_ids], 
            order_book_fanout_interface
        )

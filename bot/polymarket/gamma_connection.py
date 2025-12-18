"""
Gamma connection makes use of REST API endpoints to fetch market data
"""

import requests

from typing import Generator

from bot.common.messages.gamma import GammaMarket

GAMMA_API = "https://gamma-api.polymarket.com"

def _build_markets_endpoint(limit: int, offset: int, **kwargs) -> str:
    """Builds the markets endpoint URL with the given parameters."""
    base_url = f"{GAMMA_API}/markets"

    return f"{base_url}?limit={limit}&offset={offset}&closed=false"

def build_markets_endpoint(limit: int, offset: int) -> str:
    return _build_markets_endpoint(limit, offset)

def get_raw_markets_from_url(url: str) -> list[dict]:
    response = requests.get(url)
    response = response.json()

    return response

def _get_markets(limit: int, offset: int) -> list[GammaMarket]:
    url = build_markets_endpoint(limit, offset)
    markets = get_raw_markets_from_url(url)

    for market in markets:
        events = market.get("events", [])

        if len(events) >= 2:
            print(events)

    return [GammaMarket(**market) for market in markets]

def get_markets() -> Generator[GammaMarket, None, None]:
    limit = 100
    offset = 0

    while True:
        markets = _get_markets(limit, offset)

        yield from markets

        if len(markets) != limit:
            break
        
        offset += limit

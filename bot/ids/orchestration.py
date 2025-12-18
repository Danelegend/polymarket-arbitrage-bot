from bot.common.messages.gamma import GammaMarket
from bot.common.types.ids import MarketInformation

from .market_selector import market_valid, event_valid 
from .ids_writer import write_market, write_tradable_market
from .message_parser import parse_market, parse_event, to_tradeable_market

import logging

logger = logging.getLogger(__name__)

def save_market(gamma_market: GammaMarket):
    # Save the market to a file
    try:
        write_market(parse_market(gamma_market))
    except Exception as e:
        logger.info(f"Failed to parse market, title={gamma_market.question} e={e}")
        return

def save_market_as_tradable(market: MarketInformation):
    tradeable_market = to_tradeable_market(market)

    # Save the tradeable market to a file
    write_tradable_market(tradeable_market)

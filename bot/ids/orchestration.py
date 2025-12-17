from bot.common.messages.gamma import GammaMarket

from .market_selector import market_valid, event_valid 
from .ids_writer import write_market, write_tradable_market
from .message_parser import parse_market, parse_event, to_tradeable_market

import logging

logger = logging.getLogger(__name__)

def handle_market(gamma_market: GammaMarket):
    # Save the market to a file
    try:
        write_market(parse_market(gamma_market))
    except Exception as e:
        logger.info(f"Failed to parse market, title={gamma_market.question} e={e}")
        return

    # Check what markets and events are valid
    market_valid = market_valid(gamma_market)
    
    # If the market is not valid, we do not trade any events
    if not market_valid:
        return

    valid_events = [
        event for event in gamma_market.events if event_valid(event)
    ]

    # Convert to tradeable market
    tradeable_market = to_tradeable_market(
        gamma_market, 
        [parse_event(e) for e in valid_events]
    )

    # Save the tradeable market to a file
    write_tradable_market(tradeable_market)

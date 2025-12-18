from bot.polymarket.gamma_connection import get_markets
from bot.ids.orchestration import save_market

import logging

from dataclasses import dataclass

logging.basicConfig(
    filename="ids_runner.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

def run():
    # Goal of this script is to populate what markets are tradable
    
    # We want to find arb markets that:
    # -> End by Feb 1st 2026
    # -> Have a yes and no market
    # -> 

    for market in get_markets():
        save_market(market)


if __name__ == '__main__':
    run()


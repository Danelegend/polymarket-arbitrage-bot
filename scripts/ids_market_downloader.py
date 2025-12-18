from bot.polymarket.gamma_connection import get_markets
from bot.ids.orchestration import save_market

import logging

logging.basicConfig(
    filename="ids_runner.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

def run():
    for market in get_markets():
        if market.events is not None and len(market.events) >= 2:
            print("More than 2 events")
        save_market(market)


if __name__ == '__main__':
    run()


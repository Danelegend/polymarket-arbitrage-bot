from bot.polymarket.gamma_connection import get_markets
from bot.ids.orchestration import save_market
from bot.ids.ids_writer import create_market_file

import logging

logging.basicConfig(
    filename="ids_runner.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

def run():
    create_market_file()
    for market in get_markets():
        save_market(market)


if __name__ == '__main__':
    run()


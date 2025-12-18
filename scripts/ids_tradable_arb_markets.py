from datetime import datetime

from bot.ids.ids_reader import read_markets
from bot.ids.orchestration import save_market_as_tradable
from bot.ids.market_selector import market_valid, Condition
from bot.ids.ids_writer import create_tradable_markets_file

import logging


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
    # -> Have a volume of at least 1M

    create_tradable_markets_file()

    count = 0
    for market in read_markets():
        if market_valid(
            market,
            [
                Condition(
                    attribute="end_date",
                    predicate=lambda x: x < datetime(2026, 2, 1),
                ),
                Condition(
                    attribute="outcomes",
                    predicate=lambda x: len(x) == 2 and "Yes" in x and "No" in x,
                ),
                Condition(
                    attribute="volume",
                    predicate=lambda x: x > 1000000,
                )
            ]
        ):
            save_market_as_tradable(market)
            count += 1

    print(f"Found {count} tradable markets")


if __name__ == '__main__':
    run()


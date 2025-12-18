from bot.ids.ids_client import IdsClient
from bot.info.information_link import InfoLink
from bot.channel import Channel

from bot.strategies.strategy_builder import build_strategies

import logging

logging.basicConfig(
    filename="arb_runner.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.ids_client = IdsClient()
        self.info_link = InfoLink()
        self.channel = Channel(self.info_link)

        _build_strategies(
            self.ids_client,
            self.channel
        )

    def run(self):
        logger.info("Starting Channel")
        
        self.info_link.start()

        logger.info("Channel started")


def _build_strategies(ids_client: IdsClient, channel: Channel):
    tradable_markets = ids_client.get_tradable_markets()
    
    for strategy in build_strategies(tradable_markets):
        logger.info(f"Adding strategy {str(strategy)}")
        channel.add_strategy(strategy)
    

if __name__ == '__main__':
    app = App()
    app.run()
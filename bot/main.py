from bot.ids.ids_client import IdsClient
from bot.info.information_link import InfoLink
from bot.orderbook import OrderManager

from bot.strategies.strategy_builder import build_strategies

class App:
    def __init__(self):
        self.ids_client = IdsClient()
        self.info_link = InfoLink(self.ids_client)
        self.order_manager = OrderManager(self.info_link)

        self.strategies = []

    def build_strategies(self):
        for strategy in build_strategies(self.order_manager):
            self.strategies.append(strategy)

    def run(self):
        self.info_link.start()
from bot.polymarket.gamma_connection import get_markets
from bot.ids.orchestration import handle_market

def run():
    markets = get_markets()
    for market in markets:
        handle_market(market)


if __name__ == '__main__':
    run()


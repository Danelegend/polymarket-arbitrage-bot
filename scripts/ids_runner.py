from bot.polymarket.gamma_connection import get_markets
from bot.ids.orchestration import handle_market

def run():
    for market in get_markets():
        print(market)
        handle_market(market)


if __name__ == '__main__':
    run()


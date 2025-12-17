from bot.common.types.ids import MarketInformation, TradeableMarket
from .constants import MARKET_OUTPUT_FILE, TRADABLE_MARKETS_OUTPUT_FILE
from .serialiser import serialise_market, serialise_tradeable_market


class FileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None

        open(self.file_path, "w").close()

    def __enter__(self):
        self.file = open(self.file_path, "a")
        return self

    def write(self, data: str):
        self.file.write(data + "\n")

    def __exit__(self, exc_type, exc, tb):
        self.file.close()

MARKET_FILE_WRITER = FileWriter(MARKET_OUTPUT_FILE)
TRADABLE_MARKETS_FILE_WRITER = FileWriter(TRADABLE_MARKETS_OUTPUT_FILE)

def write_market(market: MarketInformation):
    with MARKET_FILE_WRITER as writer:
        writer.write(
            serialise_market(market)
        )

def write_tradable_market(tradeable_market: TradeableMarket):
    with TRADABLE_MARKETS_FILE_WRITER as writer:
        writer.write(
            serialise_tradeable_market(tradeable_market)
        )


from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Optional, Tuple

@dataclass
class PriceLevel:
  price: Decimal
  size: Decimal

IncomingPriceLevel = Tuple[float, float]

class OrderBook:
  def __init__(self):
    self.bids: Dict[Decimal, Decimal] = {}
    self.asks: Dict[Decimal, Decimal] = {}

    self._bid_prices = []
    self._ask_prices = []

    self.best_bid: Optional[Decimal] = None
    self.best_ask: Optional[Decimal] = None

    self.last_update_ts: Optional[int] = None
    self.last_hash: Optional[str] = None
    
    self.tick_size: Optional[Decimal] = None
    self.last_trade_price: Optional[Decimal] = None

  def _rebuild_price_lists(self):
    self._bid_prices = sorted(self.bids.keys(), reverse=True)
    self._ask_prices = sorted(self.asks.keys())

    self.best_bid = self._bid_prices[0] if self._bid_prices else None
    self.best_ask = self._ask_prices[0] if self._ask_prices else None

  def apply_book_snapshot(self, bids: list[IncomingPriceLevel], asks: list[IncomingPriceLevel], ts: int, book_hash: str):
    self.bids.clear()
    self.asks.clear()

    for lvl in bids:
      p = Decimal(lvl[0])
      s = Decimal(lvl[1])
      if s > 0:
        self.bids[p] = s
        
    for lvl in asks:
      p =  Decimal(lvl[0])
      s = Decimal(lvl[1])
      if s > 0:
        self.asks[p] = s

    self._rebuild_price_lists()
    self.last_update_ts = ts
    self.last_hash = book_hash

  def apply_price_change(self, best_bid: Optional[float], best_ask: Optional[float], ts: int):
    """
    price_change does NOT mutate depth.
    Only updates top-of-book hints.
    """
  
    if best_bid is not None:
        self.best_bid = Decimal(best_bid)
  
    if best_ask is not None:
        self.best_ask = Decimal(best_ask)
  
    self.last_update_ts = ts

  def update_tick_size(self, tick_size: str):
    self.tick_size = Decimal(tick_size)

  def update_last_trade_price(self, price: float):
    self.last_trade_price = Decimal(price)

  def get_best_bid(self) -> Optional[float]:
    if self.best_bid is None:
       return None
    return float(self.best_bid)

  def get_best_ask(self) -> Optional[float]:
    if self.best_ask is None:
      return None

    return float(self.best_ask)


  def __str__(self) -> str:
    return f"OrderBook(bids={self.bids}, asks={self.asks})"
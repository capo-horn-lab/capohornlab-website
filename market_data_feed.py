"""Real-time market-data primitives with no hard dependency on a WebSocket client."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict


@dataclass
class OrderBook:
    """Price-level order book for one market symbol."""

    bids: dict[float, float] = field(default_factory=dict)
    asks: dict[float, float] = field(default_factory=dict)

    @property
    def best_bid(self) -> tuple[float, float] | None:
        """Return the highest bid price and its quantity, if available."""
        return max(self.bids.items()) if self.bids else None

    @property
    def best_ask(self) -> tuple[float, float] | None:
        """Return the lowest ask price and its quantity, if available."""
        return min(self.asks.items()) if self.asks else None


class MarketDataFeedHandler:
    """Accumulate trade metrics received from a market-data WebSocket feed."""

    def __init__(self, websocket_url: str) -> None:
        """Create a handler for the supplied WebSocket endpoint."""
        self.websocket_url = websocket_url
        self._trade_volume: DefaultDict[str, float] = defaultdict(float)
        self._trade_notional: DefaultDict[str, float] = defaultdict(float)
        self._volume_profile: DefaultDict[str, DefaultDict[float, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self._order_books: DefaultDict[str, OrderBook] = defaultdict(OrderBook)

    def process_message(self, raw_message: str) -> None:
        """Parse and apply one JSON trade message."""
        message = json.loads(raw_message)
        if message.get("type") == "book_snapshot":
            self._apply_book_snapshot(message)
            return
        if message.get("type") != "trade":
            return

        symbol = str(message["symbol"])
        price = float(message["price"])
        size = float(message["size"])
        self._trade_notional[symbol] += price * size
        self._trade_volume[symbol] += size
        self._volume_profile[symbol][price] += size

    def vwap(self, symbol: str) -> float | None:
        """Return the volume-weighted average price for ``symbol``."""
        volume = self._trade_volume[symbol]
        return self._trade_notional[symbol] / volume if volume else None

    def volume_profile(self, symbol: str) -> dict[float, float]:
        """Return traded volume by exact price for ``symbol``."""
        return dict(self._volume_profile[symbol])

    def order_book(self, symbol: str) -> OrderBook:
        """Return the live order book for ``symbol``."""
        return self._order_books[symbol]

    def _apply_book_snapshot(self, message: dict[str, object]) -> None:
        """Replace a symbol's book with a complete bid/ask snapshot."""
        symbol = str(message["symbol"])
        self._order_books[symbol] = OrderBook(
            bids=self._parse_levels(message["bids"]),
            asks=self._parse_levels(message["asks"]),
        )

    @staticmethod
    def _parse_levels(raw_levels: object) -> dict[float, float]:
        """Convert wire-format ``[price, size]`` entries to price levels."""
        return {float(price): float(size) for price, size in raw_levels}  # type: ignore[misc]

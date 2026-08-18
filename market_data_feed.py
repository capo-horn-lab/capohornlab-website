"""Real-time market-data primitives with an injectable WebSocket transport."""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, DefaultDict


class MarketDataMessageError(ValueError):
    """Raised when a market-data message is malformed or unsupported."""


@dataclass
class OrderBook:
    bids: dict[float, float] = field(default_factory=dict)
    asks: dict[float, float] = field(default_factory=dict)

    @property
    def best_bid(self) -> tuple[float, float] | None:
        return max(self.bids.items()) if self.bids else None

    @property
    def best_ask(self) -> tuple[float, float] | None:
        return min(self.asks.items()) if self.asks else None


class MarketDataFeedHandler:
    """Accumulate trade/order-book state without imposing a WebSocket package."""

    def __init__(self, websocket_url: str, websocket_factory: Callable[[str], Any] | None = None,
                 significant_price_change_pct: float | None = None) -> None:
        self.websocket_url = websocket_url
        self._websocket_factory = websocket_factory
        self._socket: Any | None = None
        self._threshold = significant_price_change_pct
        self._callbacks: DefaultDict[str, list[Callable[[dict[str, object]], None]]] = defaultdict(list)
        self._last_price: dict[str, float] = {}
        self._trade_volume: DefaultDict[str, float] = defaultdict(float)
        self._trade_notional: DefaultDict[str, float] = defaultdict(float)
        self._volume_profile: DefaultDict[str, DefaultDict[float, float]] = defaultdict(lambda: defaultdict(float))
        self._order_books: DefaultDict[str, OrderBook] = defaultdict(OrderBook)

    @property
    def is_connected(self) -> bool:
        return self._socket is not None

    def connect(self) -> None:
        if self._socket is not None:
            return
        if self._websocket_factory is None:
            raise RuntimeError("a websocket_factory is required for this standalone handler")
        self._socket = self._websocket_factory(self.websocket_url)

    def disconnect(self) -> None:
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def receive_once(self) -> None:
        if self._socket is None:
            raise RuntimeError("feed is not connected")
        self.process_message(self._socket.recv())

    def on(self, event_name: str, callback: Callable[[dict[str, object]], None]) -> None:
        self._callbacks[event_name].append(callback)

    def process_message(self, raw_message: str) -> None:
        try:
            message = json.loads(raw_message)
            if not isinstance(message, dict):
                raise ValueError("message must be an object")
            kind = message.get("type")
            if kind == "book_snapshot": self._apply_book_snapshot(message); return
            if kind == "book_update": self._apply_book_update(message); return
            if kind != "trade": return
            symbol, price, size = str(message["symbol"]), float(message["price"]), float(message["size"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise MarketDataMessageError("invalid market-data message") from exc
        previous = self._last_price.get(symbol)
        self._trade_notional[symbol] += price * size; self._trade_volume[symbol] += size; self._volume_profile[symbol][price] += size; self._last_price[symbol] = price
        if previous and self._threshold is not None:
            change = round(((price - previous) / previous) * 100, 10)
            if abs(change) >= self._threshold:
                event: dict[str, object] = {"symbol": symbol, "previous_price": previous, "price": price, "change_pct": change}
                for callback in self._callbacks["significant_price_change"]: callback(event)

    def vwap(self, symbol: str) -> float | None:
        volume = self._trade_volume[symbol]
        return self._trade_notional[symbol] / volume if volume else None

    def volume_profile(self, symbol: str) -> dict[float, float]: return dict(self._volume_profile[symbol])
    def order_book(self, symbol: str) -> OrderBook: return self._order_books[symbol]

    def _apply_book_snapshot(self, message: dict[str, object]) -> None:
        try: self._order_books[str(message["symbol"])] = OrderBook(self._parse_levels(message["bids"]), self._parse_levels(message["asks"]))
        except (KeyError, TypeError, ValueError) as exc: raise MarketDataMessageError("invalid book snapshot") from exc

    def _apply_book_update(self, message: dict[str, object]) -> None:
        try:
            book=self._order_books[str(message["symbol"])]
            for side, levels in ((book.bids, message["bids"]), (book.asks, message["asks"])):
                for price, size in levels:  # type: ignore[misc]
                    p,q=float(price),float(size)
                    side.pop(p, None) if q == 0 else side.__setitem__(p,q)
        except (KeyError, TypeError, ValueError) as exc: raise MarketDataMessageError("invalid book update") from exc

    @staticmethod
    def _parse_levels(raw_levels: object) -> dict[float, float]: return {float(price): float(size) for price, size in raw_levels}  # type: ignore[misc]

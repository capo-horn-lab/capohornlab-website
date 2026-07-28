"""Behavioral tests for the standalone market-data feed handler."""

from __future__ import annotations

import unittest

from market_data_feed import MarketDataFeedHandler


class MarketDataFeedHandlerTests(unittest.TestCase):
    def test_process_trade_updates_vwap_and_volume_profile(self) -> None:
        handler = MarketDataFeedHandler("wss://feed.example.test")

        handler.process_message(
            '{"type":"trade","symbol":"BTC-USD","price":"100.00","size":"2"}'
        )
        handler.process_message(
            '{"type":"trade","symbol":"BTC-USD","price":"110.00","size":"3"}'
        )

        self.assertAlmostEqual(handler.vwap("BTC-USD"), 106.0)
        self.assertEqual(handler.volume_profile("BTC-USD"), {100.0: 2.0, 110.0: 3.0})

    def test_book_snapshot_exposes_best_bid_and_ask(self) -> None:
        handler = MarketDataFeedHandler("wss://feed.example.test")

        handler.process_message(
            '{"type":"book_snapshot","symbol":"BTC-USD",'
            '"bids":[["100.00","1.5"],["99.50","2"]],'
            '"asks":[["101.00","1"],["101.50","3"]]}'
        )

        book = handler.order_book("BTC-USD")
        self.assertEqual(book.best_bid, (100.0, 1.5))
        self.assertEqual(book.best_ask, (101.0, 1.0))

    def test_connect_receive_and_disconnect_use_injected_websocket(self) -> None:
        socket = _FakeWebSocket(
            '{"type":"trade","symbol":"ETH-USD","price":"2000","size":"1"}'
        )
        handler = MarketDataFeedHandler(
            "wss://feed.example.test", websocket_factory=lambda _: socket
        )

        handler.connect()
        self.assertTrue(handler.is_connected)
        handler.receive_once()
        handler.disconnect()

        self.assertEqual(handler.vwap("ETH-USD"), 2000.0)
        self.assertTrue(socket.closed)
        self.assertFalse(handler.is_connected)

    def test_significant_price_change_emits_event(self) -> None:
        handler = MarketDataFeedHandler(
            "wss://feed.example.test", significant_price_change_pct=1.0
        )
        events: list[dict[str, object]] = []
        handler.on("significant_price_change", events.append)

        handler.process_message(
            '{"type":"trade","symbol":"BTC-USD","price":"100","size":"1"}'
        )
        handler.process_message(
            '{"type":"trade","symbol":"BTC-USD","price":"102","size":"1"}'
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["symbol"], "BTC-USD")
        self.assertEqual(events[0]["change_pct"], 2.0)

    def test_book_update_removes_zero_quantity_levels(self) -> None:
        handler = MarketDataFeedHandler("wss://feed.example.test")
        handler.process_message(
            '{"type":"book_snapshot","symbol":"BTC-USD",'
            '"bids":[["100","1"]],"asks":[["101","2"]]}'
        )
        handler.process_message(
            '{"type":"book_update","symbol":"BTC-USD",'
            '"bids":[["100","0"],["99","3"]],"asks":[["101","0"]]}'
        )

        book = handler.order_book("BTC-USD")
        self.assertEqual(book.bids, {99.0: 3.0})
        self.assertEqual(book.asks, {})

    def test_malformed_trade_message_raises_domain_error(self) -> None:
        from market_data_feed import MarketDataMessageError

        handler = MarketDataFeedHandler("wss://feed.example.test")

        with self.assertRaises(MarketDataMessageError):
            handler.process_message('{"type":"trade","symbol":"BTC-USD","price":"nope"}')


class _FakeWebSocket:
    def __init__(self, message: str) -> None:
        self.message = message
        self.closed = False

    def recv(self) -> str:
        return self.message

    def close(self) -> None:
        self.closed = True


if __name__ == "__main__":
    unittest.main()

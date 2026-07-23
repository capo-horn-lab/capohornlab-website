#!/usr/bin/env python3
"""
backtest_engine.py — Capo Horn Lab Backtest Engine
===================================================

Motore di backtest Python realistico per Futures (ES, NQ, CL).
Include slippage, commissioni, fill model, regime detector,
statistiche complete, Monte Carlo, e strategie implementate
come sottoclassi.

Compatibile con chart_pipeline.py per la generazione dei grafici.

Usage:
    python backtest_engine.py                          # demo run con smoke test
    python backtest_engine.py --strategy TSMomentum     # run specifica strategia
    python backtest_engine.py --list                    # elenca strategie disponibili

Dipendenze: numpy, pandas, scipy (no dipendenze pesanti)
"""

from __future__ import annotations

import math
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Constants ─────────────────────────────────────────────────────────────
TICK_SIZE: dict[str, float] = {
    "ES": 0.25,
    "NQ": 0.25,
    "CL": 0.01,
}
POINT_VALUE: dict[str, float] = {
    "ES": 50.0,
    "NQ": 20.0,
    "CL": 1000.0,
}
COMMISSION_PER_SIDE: float = 2.50
HIGH_VOLUME_THRESHOLD: int = 10000
DISCOUNTED_COMMISSION: float = 1.80

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1 — Data Types & Structures
# ══════════════════════════════════════════════════════════════════════════


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Order:
    """Un singolo ordine inviato al motore di backtest."""
    id: int = 0
    timestamp: Optional[pd.Timestamp] = None
    symbol: str = ""
    side: Optional[OrderSide] = None
    order_type: OrderType = OrderType.MARKET
    quantity: int = 0
    price: float = 0.0
    stop_price: float = 0.0
    time_in_force: str = "gtc"
    status: str = "pending"
    filled_qty: int = 0
    avg_fill_price: float = 0.0
    commission: float = 0.0
    fill_log: list[dict] = field(default_factory=list)
    tag: str = ""


@dataclass
class Trade:
    """Un trade chiuso (round trip)."""
    id: int = 0
    entry_time: Optional[pd.Timestamp] = None
    exit_time: Optional[pd.Timestamp] = None
    symbol: str = ""
    direction: str = ""
    entry_price: float = 0.0
    exit_price: float = 0.0
    quantity: int = 0
    gross_pnl: float = 0.0
    net_pnl: float = 0.0
    commission: float = 0.0
    slippage: float = 0.0
    bars_held: int = 0
    exit_reason: str = ""


@dataclass
class BarData:
    """Una barra OHLCV."""
    timestamp: Optional[pd.Timestamp] = None
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: int = 0
    symbol: str = ""


@dataclass
class FillResult:
    """Risultato del fill model per un ordine."""
    filled: bool = False
    fill_price: float = 0.0
    fill_qty: int = 0
    slippage: float = 0.0
    partial: bool = False


# ══════════════════════════════════════════════════════════════════════════
# SECTION 2 — Data Loader
# ══════════════════════════════════════════════════════════════════════════


class DataLoader:
    """
    Carica dati OHLCV da parquet in D:\\marketdata\\.
    Supporta ES, NQ, CL. Rileva automaticamente il formato delle colonne.
    """

    MARKET_DATA_DIR = Path(r"D:\marketdata")

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or self.MARKET_DATA_DIR
        self._loaded: dict[str, pd.DataFrame] = {}

    def load(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        timeframe: str = "1m",
        resample_cl: bool = True,
    ) -> pd.DataFrame:
        """Carica dati OHLCV per il simbolo specificato."""
        symbol = symbol.upper()
        cache_key = f"{symbol}_{timeframe}"
        if cache_key in self._loaded:
            df = self._loaded[cache_key].copy()
        else:
            df = self._load_raw(symbol, timeframe, resample_cl)
            self._loaded[cache_key] = df.copy()

        if start:
            df = df[df.index >= pd.Timestamp(start, tz="UTC")]
        if end:
            df = df[df.index <= pd.Timestamp(end, tz="UTC")]
        return df

    def list_available(self) -> list[str]:
        """Elenca i simboli e periodi disponibili."""
        result = []
        es_dir = self.data_dir / "ES"
        if es_dir.exists():
            n = len(list(es_dir.glob("*.parquet")))
            result.append(f"ES: {n} files")
        nq_dir = self.data_dir / "NQ" / "1m"
        if nq_dir.exists():
            n = len(list(nq_dir.glob("*.parquet")))
            result.append(f"NQ: {n} files")
        cl_dir = self.data_dir / "cl_mbp1" / "parquet"
        if cl_dir.exists():
            n = len(list(cl_dir.glob("*.parquet")))
            result.append(f"CL: {n} MBP1 files")
        return result

    def _load_raw(self, symbol: str, timeframe: str, resample_cl: bool) -> pd.DataFrame:
        if symbol == "ES":
            return self._load_es()
        elif symbol == "NQ":
            return self._load_nq()
        elif symbol == "CL":
            return self._load_cl(timeframe) if resample_cl else self._load_cl_mbp1()
        else:
            raise ValueError(f"Simbolo non supportato: {symbol}")

    def _load_es(self) -> pd.DataFrame:
        es_dir = self.data_dir / "ES"
        files = sorted(es_dir.glob("ES_ohlcv_1m_*.parquet"))
        if not files:
            files = sorted(es_dir.glob("*smoke*.parquet"))
        if not files:
            raise FileNotFoundError(f"Nessun file ES in {es_dir}")
        dfs = []
        for f in files:
            df = pd.read_parquet(f)
            if "ts_event" in df.columns:
                df = df.set_index("ts_event")
            dfs.append(df)
        df = pd.concat(dfs).sort_index()
        cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        return df[cols].astype({c: float for c in cols if c != "volume"})

    def _load_nq(self) -> pd.DataFrame:
        nq_dir = self.data_dir / "NQ" / "1m"
        files = sorted(nq_dir.glob("*.parquet"))
        if not files:
            raise FileNotFoundError(f"Nessun file NQ in {nq_dir}")
        dfs = []
        for f in files:
            df = pd.read_parquet(f)
            if "ts_event" in df.columns:
                df = df.set_index("ts_event")
            dfs.append(df)
        df = pd.concat(dfs).sort_index()
        cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        return df[cols].astype({c: float for c in cols if c != "volume"})

    def _load_cl_mbp1(self) -> pd.DataFrame:
        cl_dir = self.data_dir / "cl_mbp1" / "parquet"
        files = sorted(cl_dir.glob("*.parquet"))
        if not files:
            raise FileNotFoundError(f"Nessun file CL in {cl_dir}")
        dfs = []
        for f in files:
            df = pd.read_parquet(f)
            if df.index.name == "ts_recv" and "ts_event" in df.columns:
                df = df.reset_index(drop=True).set_index("ts_event")
            elif "ts_event" in df.columns:
                df = df.set_index("ts_event")
            dfs.append(df)
        df = pd.concat(dfs).sort_index()
        return df

    def _load_cl(self, timeframe: str = "1m") -> pd.DataFrame:
        df = self._load_cl_mbp1()
        if "bid_px_00" in df.columns and "ask_px_00" in df.columns:
            df["mid"] = (df["bid_px_00"] + df["ask_px_00"]) / 2
        elif "price" in df.columns:
            df["mid"] = df["price"]
        else:
            raise ValueError("CL: no price column found")
        ohlc = df["mid"].resample(timeframe).agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        vol = df["size"].resample(timeframe).sum() if "size" in df.columns else pd.Series(0, index=ohlc.index)
        result = ohlc.copy()
        result["volume"] = vol
        result = result.dropna(subset=["open"])
        return result[["open", "high", "low", "close", "volume"]].astype(float)


# ══════════════════════════════════════════════════════════════════════════
# SECTION 3 — Slippage, Commission & Fill Models
# ══════════════════════════════════════════════════════════════════════════


class SlippageModel:
    """Modello di slippage realistico. Base = 1 tick, variabile per volume/volatilità."""
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.tick = TICK_SIZE.get(self.symbol, 0.25)
        self.pv = POINT_VALUE.get(self.symbol, 50.0)

    def compute(self, bar: BarData, order_qty: int, avg_volume: float = 1000.0) -> float:
        base = self.tick
        vol_ratio = bar.volume / max(avg_volume, 1)
        if vol_ratio < 0.3:
            vol_factor = 1.5
        elif vol_ratio < 0.7:
            vol_factor = 1.2
        elif vol_ratio < 1.5:
            vol_factor = 1.0
        elif vol_ratio < 3.0:
            vol_factor = 0.8
        else:
            vol_factor = 0.6
        bar_range = bar.high - bar.low
        avg_range = bar.close * 0.002
        vola_factor = max(0.5, min(3.0, bar_range / max(avg_range, 0.01)))
        size_factor = 1.0 + (order_qty - 1) * 0.05
        size_factor = min(size_factor, 3.0)
        slippage = base * vol_factor * vola_factor * size_factor
        return round(slippage / self.tick) * self.tick


class CommissionModel:
    @staticmethod
    def compute_per_contract(daily_volume: int = 0) -> float:
        return DISCOUNTED_COMMISSION if daily_volume > HIGH_VOLUME_THRESHOLD else COMMISSION_PER_SIDE

    @staticmethod
    def compute(qty: int, price: float = 0.0, daily_volume: int = 0) -> float:
        return round(qty * CommissionModel.compute_per_contract(daily_volume), 2)


class FillModel:
    """Modello di esecuzione: MARKET always fills, LIMIT 80%, STOP su violazione."""
    def __init__(self, symbol: str, slippage_model: Optional[SlippageModel] = None):
        self.symbol = symbol.upper()
        self.slippage = slippage_model or SlippageModel(symbol)
        self.tick = TICK_SIZE.get(self.symbol, 0.25)
        self.rng = np.random.default_rng(42)

    def try_fill(self, order: Order, bar: BarData, avg_volume: float = 1000.0, daily_volume: int = 0) -> FillResult:
        remaining = order.quantity - order.filled_qty
        if remaining <= 0:
            return FillResult(filled=False)
        if order.order_type == OrderType.MARKET:
            return self._fill_market(order, bar, remaining, avg_volume, daily_volume)
        elif order.order_type == OrderType.LIMIT:
            return self._fill_limit(order, bar, remaining, avg_volume, daily_volume)
        elif order.order_type == OrderType.STOP:
            return self._fill_stop(order, bar, remaining, avg_volume, daily_volume)
        return FillResult(filled=False)

    def _fill_market(self, order, bar, remaining, avg_volume, daily_volume):
        slippage_pts = self.slippage.compute(bar, remaining, avg_volume)
        if order.side == OrderSide.BUY:
            fill_price = max(bar.open, bar.low) + slippage_pts
        else:
            fill_price = min(bar.open, bar.high) - slippage_pts
        fill_price = max(fill_price, bar.low * 0.99)
        fill_price = min(fill_price, bar.high * 1.01)
        fill_qty = remaining
        partial = False
        if bar.volume < avg_volume * 0.2 and remaining > 5:
            fill_ratio = min(1.0, bar.volume / max(avg_volume * 0.1, 1))
            fill_qty = max(1, int(remaining * fill_ratio))
            partial = fill_qty < remaining
        fill_price = round(fill_price / self.tick) * self.tick
        return FillResult(filled=True, fill_price=fill_price, fill_qty=fill_qty, slippage=slippage_pts, partial=partial)

    def _fill_limit(self, order, bar, remaining, avg_volume, daily_volume):
        hit = (order.side == OrderSide.BUY and bar.low <= order.price) or (order.side == OrderSide.SELL and bar.high >= order.price)
        if not hit or self.rng.random() > 0.8:
            return FillResult(filled=False)
        fill_qty = remaining
        partial = False
        if bar.volume < avg_volume * 0.15 and remaining > 3:
            fill_qty = max(1, remaining // 2)
            partial = True
        return FillResult(filled=True, fill_price=order.price, fill_qty=fill_qty, partial=partial)

    def _fill_stop(self, order, bar, remaining, avg_volume, daily_volume):
        triggered = (order.side == OrderSide.BUY and bar.high >= order.stop_price) or (order.side == OrderSide.SELL and bar.low <= order.stop_price)
        if not triggered:
            return FillResult(filled=False)
        slippage_pts = self.slippage.compute(bar, remaining, avg_volume)
        if order.side == OrderSide.BUY:
            fill_price = max(order.stop_price, bar.open) + slippage_pts
        else:
            fill_price = min(order.stop_price, bar.open) - slippage_pts
        fill_price = round(fill_price / self.tick) * self.tick
        return FillResult(filled=True, fill_price=fill_price, fill_qty=remaining, slippage=slippage_pts)


# ══════════════════════════════════════════════════════════════════════════
# SECTION 4 — Position Manager (SIGNED quantity: positive=long, negative=short)
# ══════════════════════════════════════════════════════════════════════════


class Position:
    """
    Gestisce una posizione aperta usando signed quantity.
    quantity > 0  = LONG
    quantity < 0  = SHORT
    quantity == 0 = FLAT
    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.quantity: int = 0
        self.avg_entry: float = 0.0
        self.entry_time: Optional[pd.Timestamp] = None
        self.realized_pnl: float = 0.0
        self.unrealized_pnl: float = 0.0
        self.trade_id_counter: int = 0
        self.bars_held: int = 0

        # Stop / Target / Trailing
        self.stop_loss: Optional[float] = None
        self.take_profit: Optional[float] = None
        self.trailing_activated: bool = False
        self.trailing_stop_price: Optional[float] = None
        self.trailing_dist_pts: Optional[float] = None
        self.max_bars_held: Optional[int] = None

    @property
    def is_long(self) -> bool:
        return self.quantity > 0

    @property
    def is_short(self) -> bool:
        return self.quantity < 0

    @property
    def is_flat(self) -> bool:
        return self.quantity == 0

    @property
    def abs_qty(self) -> int:
        return abs(self.quantity)

    def open_long(self, qty: int, price: float, timestamp: pd.Timestamp) -> None:
        """Aumenta posizione long (qty > 0)."""
        qty = int(qty)
        price = float(price)
        if self.quantity >= 0:
            total_qty = self.quantity + qty
            self.avg_entry = (float(self.avg_entry) * float(self.quantity) + price * float(qty)) / float(total_qty)
        else:
            # Currently short — this should be handled by reduce + open
            self.quantity = qty
            self.avg_entry = price
        self.quantity += qty
        if self.entry_time is None:
            self.entry_time = timestamp

    def open_short(self, qty: int, price: float, timestamp: pd.Timestamp) -> None:
        """Aumenta posizione short (qty > 0)."""
        qty = int(qty)
        price = float(price)
        if self.quantity <= 0:
            total_qty = abs(self.quantity) + qty
            self.avg_entry = (float(self.avg_entry) * float(abs(self.quantity)) + price * float(qty)) / float(total_qty)
        else:
            self.quantity = -qty
            self.avg_entry = price
        self.quantity -= qty
        if self.entry_time is None:
            self.entry_time = timestamp

    def close_position(self, price: float, timestamp: pd.Timestamp) -> Trade:
        """Chiude completamente la posizione."""
        if self.quantity == 0:
            raise ValueError("Posizione già flat")
        direction = "long" if self.quantity > 0 else "short"
        price = float(price)
        qty = abs(self.quantity)
        if self.quantity > 0:
            gross_pnl = (price - self.avg_entry) * qty * POINT_VALUE.get(self.symbol, 50.0)
        else:
            gross_pnl = (self.avg_entry - price) * qty * POINT_VALUE.get(self.symbol, 50.0)
        trade = Trade(
            id=self.trade_id_counter, entry_time=self.entry_time, exit_time=timestamp,
            symbol=self.symbol, direction=direction, entry_price=self.avg_entry, exit_price=price,
            quantity=qty, gross_pnl=gross_pnl, net_pnl=gross_pnl, commission=0.0, slippage=0.0,
            bars_held=self.bars_held,
        )
        self.trade_id_counter += 1
        self.realized_pnl += gross_pnl
        self._reset()
        return trade

    def reduce_position(self, qty: int, price: float, timestamp: pd.Timestamp) -> Optional[Trade]:
        """
        Riduce la posizione di 'qty' contratti.
        Se la posizione viene completamente chiusa, restituisce un Trade.
        Se la posizione si inverte, NON gestisce reversal — il chiamante deve farlo.
        """
        qty = min(qty, abs(self.quantity))
        if qty <= 0:
            return None
        price = float(price)
        direction = "long" if self.quantity > 0 else "short"
        if self.quantity > 0:
            gross_pnl = (price - self.avg_entry) * qty * POINT_VALUE.get(self.symbol, 50.0)
            self.quantity -= qty
        else:
            gross_pnl = (self.avg_entry - price) * qty * POINT_VALUE.get(self.symbol, 50.0)
            self.quantity += qty
        self.realized_pnl += gross_pnl
        trade = Trade(
            id=self.trade_id_counter, entry_time=self.entry_time, exit_time=timestamp,
            symbol=self.symbol, direction=direction, entry_price=self.avg_entry, exit_price=price,
            quantity=qty, gross_pnl=gross_pnl, net_pnl=gross_pnl, commission=0.0, slippage=0.0,
            bars_held=self.bars_held,
        )
        self.trade_id_counter += 1
        if self.quantity == 0:
            self._reset()
        return trade

    def update_unrealized(self, current_price: float) -> float:
        if self.quantity == 0:
            self.unrealized_pnl = 0.0
        elif self.quantity > 0:
            self.unrealized_pnl = (current_price - self.avg_entry) * self.quantity * POINT_VALUE.get(self.symbol, 50.0)
        else:
            self.unrealized_pnl = (self.avg_entry - current_price) * abs(self.quantity) * POINT_VALUE.get(self.symbol, 50.0)
        return self.unrealized_pnl

    def set_stop_loss(self, price: float) -> None:
        self.stop_loss = price

    def set_take_profit(self, price: float) -> None:
        self.take_profit = price

    def set_trailing_stop(self, activate_price: float, distance_pts: float) -> None:
        self.trailing_activated = False
        self.trailing_stop_price = None
        self.trailing_dist_pts = distance_pts

    def set_time_exit(self, max_bars: int) -> None:
        self.max_bars_held = max_bars

    def on_bar(self, bar: BarData) -> Optional[str]:
        """Controlla stop/target/trailing/time. Restituisce motivo exit o None."""
        if self.quantity == 0:
            return None
        self.bars_held += 1
        # Stop loss
        if self.stop_loss is not None:
            if self.quantity > 0 and bar.low <= self.stop_loss:
                return "stop_loss"
            if self.quantity < 0 and bar.high >= self.stop_loss:
                return "stop_loss"
        # Take profit
        if self.take_profit is not None:
            if self.quantity > 0 and bar.high >= self.take_profit:
                return "take_profit"
            if self.quantity < 0 and bar.low <= self.take_profit:
                return "take_profit"
        # Trailing stop
        if self.trailing_dist_pts is not None:
            if self.quantity > 0:
                if not self.trailing_activated:
                    self.trailing_activated = True
                    self.trailing_stop_price = bar.high - self.trailing_dist_pts
                else:
                    new_stop = bar.high - self.trailing_dist_pts
                    self.trailing_stop_price = max(self.trailing_stop_price, new_stop)
                if bar.low <= self.trailing_stop_price:
                    return "trailing_stop"
            else:
                if not self.trailing_activated:
                    self.trailing_activated = True
                    self.trailing_stop_price = bar.low + self.trailing_dist_pts
                else:
                    new_stop = bar.low + self.trailing_dist_pts
                    self.trailing_stop_price = min(self.trailing_stop_price, new_stop)
                if bar.high >= self.trailing_stop_price:
                    return "trailing_stop"
        # Time exit
        if self.max_bars_held is not None and self.bars_held >= self.max_bars_held:
            return "time_exit"
        return None

    def _reset(self) -> None:
        self.quantity = 0
        self.avg_entry = 0.0
        self.bars_held = 0
        self.entry_time = None
        self.stop_loss = None
        self.take_profit = None
        self.trailing_activated = False
        self.trailing_stop_price = None
        self.trailing_dist_pts = None


# ══════════════════════════════════════════════════════════════════════════
# SECTION 5 — Market Regime Detector
# ══════════════════════════════════════════════════════════════════════════


@dataclass
class RegimeState:
    trend_strength: float = 0.0
    trend_direction: int = 0
    volatility_regime: str = "normal"
    volatility_percentile: float = 0.5
    atr_percent: float = 0.0
    vix_proxy: float = 0.0
    mean_reversion_prob: float = 0.0
    regime_label: str = "neutral"
    regime_code: int = 0


class RegimeDetector:
    """Market Regime Detector: trend, volatilità, VIX proxy, mean reversion."""
    def __init__(self, atr_period: int = 14, trend_period: int = 20, lookback: int = 50):
        self.atr_period = atr_period
        self.trend_period = trend_period
        self.lookback = lookback

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        n = len(df)

        # ATR
        tr = np.full(n, np.nan)
        for i in range(1, n):
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
        atr = pd.Series(tr).rolling(self.atr_period, min_periods=1).mean().values
        atr_pct = np.where(close > 0, atr / close * 100, 0)

        # Trend
        up = np.maximum(0, np.diff(close, prepend=close[0]))
        down = np.maximum(0, -np.diff(close, prepend=close[0]))
        sup = pd.Series(up).rolling(self.trend_period, min_periods=1).mean().values
        sdown = pd.Series(down).rolling(self.trend_period, min_periods=1).mean().values
        di_plus = sup / np.maximum(close, 1e-10) * 100
        di_minus = sdown / np.maximum(close, 1e-10) * 100
        dx = np.where(di_plus + di_minus > 0, abs(di_plus - di_minus) / (di_plus + di_minus) * 100, 0)
        adx = pd.Series(dx).rolling(self.trend_period, min_periods=1).mean().values
        trend_dir = np.sign(di_plus - di_minus)

        # Volatility percentile
        vola_pct = pd.Series(atr_pct).rolling(self.lookback, min_periods=1).rank(pct=True).values
        vola_regime = np.full(n, "normal", dtype=object)
        vola_regime[vola_pct > 0.8] = "high"
        vola_regime[vola_pct < 0.2] = "low"

        # VIX proxy (range expansion)
        hl_range = high - low
        avg_range = pd.Series(hl_range).rolling(self.atr_period, min_periods=1).mean().values
        vix_proxy = np.where(avg_range > 0, hl_range / avg_range, 1.0)

        # Mean reversion prob
        sma = pd.Series(close).rolling(self.trend_period, min_periods=1).mean().values
        std = pd.Series(close).rolling(self.trend_period, min_periods=1).std().values
        z_score = np.where(std > 0, (close - sma) / std, 0)
        mr_prob = np.where(adx < 25, np.clip(np.abs(z_score) / 3.0, 0, 1), np.clip(np.abs(z_score) / 5.0, 0, 0.5))

        # Regime labels
        rc = np.zeros(n, dtype=int)
        rl = np.full(n, "neutral", dtype=object)
        for i in range(n):
            if adx[i] > 25:
                if trend_dir[i] > 0:
                    rc[i] = 1 if adx[i] < 45 else 2
                    rl[i] = "up" if adx[i] < 45 else "strong_up"
                elif trend_dir[i] < 0:
                    rc[i] = -1 if adx[i] < 45 else -2
                    rl[i] = "down" if adx[i] < 45 else "strong_down"

        df["atr"] = atr
        df["atr_pct"] = atr_pct
        df["adx"] = adx
        df["trend_direction"] = trend_dir
        df["trend_strength"] = adx
        df["volatility_regime"] = vola_regime
        df["volatility_percentile"] = vola_pct
        df["vix_proxy"] = vix_proxy
        df["mr_prob"] = mr_prob
        df["z_score"] = z_score
        df["regime_code"] = rc
        df["regime_label"] = rl
        return df

    def get_current(self, df: pd.DataFrame) -> RegimeState:
        if len(df) == 0:
            return RegimeState()
        last = df.iloc[-1]
        return RegimeState(
            trend_strength=float(last.get("trend_strength", 0)),
            trend_direction=int(last.get("trend_direction", 0)),
            volatility_regime=str(last.get("volatility_regime", "normal")),
            volatility_percentile=float(last.get("volatility_percentile", 0.5)),
            atr_percent=float(last.get("atr_pct", 0)),
            vix_proxy=float(last.get("vix_proxy", 1.0)),
            mean_reversion_prob=float(last.get("mr_prob", 0)),
            regime_label=str(last.get("regime_label", "neutral")),
            regime_code=int(last.get("regime_code", 0)),
        )


# ══════════════════════════════════════════════════════════════════════════
# SECTION 6 — Statistics Engine
# ══════════════════════════════════════════════════════════════════════════


@dataclass
class BacktestStats:
    n_bars: int = 0
    total_days: float = 0.0
    total_trades: int = 0
    total_long: int = 0
    total_short: int = 0
    total_gross_pnl: float = 0.0
    total_net_pnl: float = 0.0
    total_commission: float = 0.0
    total_slippage: float = 0.0
    avg_trade_pnl: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    med_trade_pnl: float = 0.0
    win_rate: float = 0.0
    loss_rate: float = 0.0
    profit_factor: float = 0.0
    expectancy: float = 0.0
    avg_bars_held: float = 0.0
    avg_win_bars: float = 0.0
    avg_loss_bars: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0
    cagr: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    max_drawdown_duration: int = 0
    ulcer_index: float = 0.0
    max_consec_wins: int = 0
    max_consec_losses: int = 0
    avg_consec_wins: float = 0.0
    avg_consec_losses: float = 0.0
    skewness: float = 0.0
    kurtosis: float = 0.0
    pct_positive: float = 0.0
    mc_sharpe_5pct: float = 0.0
    mc_sharpe_95pct: float = 0.0
    mc_sharpe_mean: float = 0.0
    mc_prob_positive: float = 0.0
    mc_max_dd_95pct: float = 0.0
    monthly_returns: Optional[pd.Series] = None
    annual_returns: Optional[pd.Series] = None
    best_month: float = 0.0
    worst_month: float = 0.0
    pct_positive_months: float = 0.0
    trade_pnls: np.ndarray = field(default_factory=lambda: np.array([]))
    trade_directions: list[str] = field(default_factory=list)
    equity_curve: Optional[np.ndarray] = None
    drawdown_curve: Optional[np.ndarray] = None
    drawdown_pct_curve: Optional[np.ndarray] = None


class StatisticsEngine:
    """Calcola statistiche complete: Sharpe, Sortino, Calmar, Monte Carlo, drawdown."""
    def __init__(self, risk_free_rate: float = 0.05, trading_days: int = 252):
        self.risk_free_rate = risk_free_rate
        self.trading_days = trading_days

    def compute(self, trades: list[Trade], initial_capital: float = 100_000.0,
                dates: Optional[pd.DatetimeIndex] = None,
                equity_curve: Optional[np.ndarray] = None) -> BacktestStats:
        stats = BacktestStats()
        if len(trades) == 0:
            return stats

        pnls = np.array([t.net_pnl for t in trades])
        stats.trade_pnls = pnls
        stats.trade_directions = [t.direction for t in trades]
        stats.total_trades = len(trades)
        stats.total_long = sum(1 for t in trades if t.direction == "long")
        stats.total_short = sum(1 for t in trades if t.direction == "short")
        stats.total_gross_pnl = sum(t.gross_pnl for t in trades)
        stats.total_net_pnl = sum(t.net_pnl for t in trades)
        stats.total_commission = sum(t.commission for t in trades)
        stats.total_slippage = sum(t.slippage for t in trades)
        stats.avg_trade_pnl = float(np.mean(pnls))
        stats.med_trade_pnl = float(np.median(pnls))

        wins = pnls[pnls > 0]
        losses = pnls[pnls < 0]
        stats.win_rate = len(wins) / len(pnls) * 100
        stats.loss_rate = len(losses) / len(pnls) * 100
        stats.pct_positive = stats.win_rate
        stats.avg_win = float(np.mean(wins)) if len(wins) > 0 else 0.0
        stats.avg_loss = float(np.mean(losses)) if len(losses) > 0 else 0.0
        total_wins = wins.sum() if len(wins) > 0 else 0
        total_losses = abs(losses.sum()) if len(losses) > 0 else 0
        stats.profit_factor = total_wins / total_losses if total_losses > 0 else (999.0 if total_wins > 0 else 0.0)
        stats.expectancy = (stats.win_rate / 100 * stats.avg_win) + (stats.loss_rate / 100 * stats.avg_loss)

        bh = np.array([t.bars_held for t in trades])
        stats.avg_bars_held = float(np.mean(bh))
        if len(wins) > 0:
            stats.avg_win_bars = float(np.mean([t.bars_held for t in trades if t.net_pnl > 0]))
        if len(losses) > 0:
            stats.avg_loss_bars = float(np.mean([t.bars_held for t in trades if t.net_pnl < 0]))

        # Consecutive streaks
        signs = np.sign(pnls)
        streaks = []
        cur_s, cur_n = signs[0], 1
        for s in signs[1:]:
            if s == cur_s and s != 0:
                cur_n += 1
            else:
                if cur_s != 0:
                    streaks.append((cur_s, cur_n))
                cur_s, cur_n = s, 1
        if cur_s != 0:
            streaks.append((cur_s, cur_n))
        win_streaks = [s[1] for s in streaks if s[0] > 0]
        loss_streaks = [s[1] for s in streaks if s[0] < 0]
        stats.max_consec_wins = max(win_streaks) if win_streaks else 0
        stats.max_consec_losses = max(loss_streaks) if loss_streaks else 0
        stats.avg_consec_wins = float(np.mean(win_streaks)) if win_streaks else 0.0
        stats.avg_consec_losses = float(np.mean(loss_streaks)) if loss_streaks else 0.0
        stats.skewness = float(scipy_stats.skew(pnls))
        stats.kurtosis = float(scipy_stats.kurtosis(pnls, fisher=True))

        # Equity curve
        if equity_curve is not None:
            eq = np.asarray(equity_curve, dtype=float)
        else:
            eq = np.concatenate([[initial_capital], initial_capital + np.cumsum(pnls)])
        stats.equity_curve = eq
        stats.n_bars = len(eq)

        # Drawdown
        peak = np.maximum.accumulate(eq)
        dd = eq - peak
        dd_pct = np.where(peak > 0, dd / peak * 100, 0)
        stats.drawdown_curve = dd
        stats.drawdown_pct_curve = dd_pct
        stats.max_drawdown = float(dd.min())
        stats.max_drawdown_pct = float(dd_pct.min())
        dur = 0
        max_dur = 0
        for v in dd_pct:
            if v < 0:
                dur += 1
                max_dur = max(max_dur, dur)
            else:
                dur = 0
        stats.max_drawdown_duration = max_dur
        stats.ulcer_index = float(np.sqrt(np.mean(dd_pct ** 2)))

        # CAGR
        if dates is not None and len(dates) > 1:
            stats.total_days = (dates[-1] - dates[0]).total_seconds() / 86400.0
        else:
            stats.total_days = stats.n_bars
        years = stats.total_days / self.trading_days
        stats.cagr = ((eq[-1] / eq[0]) ** (1 / years) - 1) * 100 if years > 0 and eq[0] > 0 else 0.0

        # Sharpe / Sortino
        if len(pnls) > 1 and np.std(pnls) > 0:
            scale = np.sqrt(self.trading_days / max(stats.avg_bars_held, 1))
            stats.sharpe_ratio = (np.mean(pnls) / np.std(pnls)) * scale
            downside = pnls[pnls < 0]
            stats.sortino_ratio = (np.mean(pnls) / np.std(downside)) * scale if len(downside) > 1 and np.std(downside) > 0 else 0.0
        stats.calmar_ratio = stats.cagr / abs(stats.max_drawdown_pct) if stats.max_drawdown_pct != 0 else 0.0

        # Monte Carlo
        mc_sharpes, mc_dds = [], []
        for _ in range(1000):
            s = np.random.permutation(pnls)
            mc_sharpes.append(np.mean(s) / np.std(s) if len(s) > 1 and np.std(s) > 0 else 0.0)
            pk = np.maximum.accumulate(np.cumsum(s))
            mc_dds.append((np.cumsum(s) - pk).min())
        stats.mc_sharpe_5pct = float(np.percentile(mc_sharpes, 5))
        stats.mc_sharpe_95pct = float(np.percentile(mc_sharpes, 95))
        stats.mc_sharpe_mean = float(np.mean(mc_sharpes))
        stats.mc_prob_positive = float(np.mean(np.array(mc_sharpes) > 0) * 100)
        stats.mc_max_dd_95pct = float(np.percentile(mc_dds, 95))

        # Monthly / Annual
        if dates is not None and len(dates) == len(pnls):
            df = pd.DataFrame({"date": dates, "pnl": pnls})
            df["year"], df["month"] = df["date"].dt.year, df["date"].dt.month
            monthly = df.groupby(["year", "month"])["pnl"].sum()
            annual = df.groupby("year")["pnl"].sum()
            stats.monthly_returns = monthly
            stats.annual_returns = annual
            if len(monthly) > 0:
                stats.best_month = float(monthly.max())
                stats.worst_month = float(monthly.min())
                stats.pct_positive_months = float((monthly > 0).mean() * 100)
        return stats

    @staticmethod
    def split_is_oos(df: pd.DataFrame, split_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        ts = pd.Timestamp(split_date, tz="UTC") if "TZ" in str(df.index.dtype) else pd.Timestamp(split_date)
        return df[df.index < ts].copy(), df[df.index >= ts].copy()


# ══════════════════════════════════════════════════════════════════════════
# SECTION 7 — Strategy Interface & Implementations
# ══════════════════════════════════════════════════════════════════════════


class Strategy(ABC):
    """Classe base astratta per tutte le strategie."""
    def __init__(self, name: str, symbol: str, params: Optional[dict] = None):
        self.name = name
        self.symbol = symbol
        self.params = params or {}
        self.tick = TICK_SIZE.get(symbol, 0.25)
        self.point_value = POINT_VALUE.get(symbol, 50.0)
        self.signals: list[dict] = []
        self.bar_index: int = 0

    @abstractmethod
    def on_bar(self, bar: BarData, position: Position, regime: Optional[RegimeState] = None) -> list[Order]:
        ...

    def on_trade(self, trade: Trade) -> None:
        pass

    def on_position_change(self, position: Position) -> None:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}' on {self.symbol}>"


class TimeSeriesMomentum(Strategy):
    """
    Time Series Momentum (Trend Following).
    Entra long quando prezzo > SMA_lento, short quando prezzo < SMA_lento.
    Esce quando prezzo incrocia SMA_veloce.
    """
    def __init__(self, symbol: str, params: Optional[dict] = None):
        defaults = {"fast_ma": 20, "slow_ma": 100, "atr_multiplier": 2.0, "use_trailing": True, "quantity": 1, "max_bars_hold": 240}
        merged = {**defaults, **(params or {})}
        super().__init__("TimeSeriesMomentum", symbol, merged)
        self._prices: list[float] = []

    def on_bar(self, bar: BarData, position: Position, regime: Optional[RegimeState] = None) -> list[Order]:
        orders = []
        self._prices.append(bar.close)
        fast_ma = self.params["fast_ma"]
        slow_ma = self.params["slow_ma"]
        qty = self.params["quantity"]
        if len(self._prices) < slow_ma:
            return orders
        prices = np.array(self._prices)
        fast = float(np.mean(prices[-fast_ma:]))
        slow = float(np.mean(prices[-slow_ma:]))

        if position.is_long:
            if bar.close < fast:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=qty, tag="tsmom_exit_long"))
        elif position.is_short:
            if bar.close > fast:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=qty, tag="tsmom_exit_short"))
        else:
            if bar.close > slow:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=qty, tag="tsmom_entry_long"))
            elif bar.close < slow:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=qty, tag="tsmom_entry_short"))
        self.bar_index += 1
        return orders


class OpeningRangeBreakout(Strategy):
    """
    Opening Range Breakout.
    Compra se prezzo rompe sopra massimo del range di apertura (N barre).
    Vende se rompe sotto minimo.
    """
    def __init__(self, symbol: str, params: Optional[dict] = None):
        defaults = {"range_bars": 30, "atr_multiplier": 2.0, "target_multiplier": 1.5, "session_start": "14:30", "session_end": "21:00", "quantity": 1}
        super().__init__("OpeningRangeBreakout", symbol, {**defaults, **(params or {})})
        self._session_high: Optional[float] = None
        self._session_low: Optional[float] = None
        self._range_count: int = 0
        self._current_session: Optional[str] = None
        self._atr: float = 0.0
        self._daily_prices: list[float] = []

    def on_bar(self, bar: BarData, position: Position, regime: Optional[RegimeState] = None) -> list[Order]:
        orders = []
        qty = self.params["quantity"]
        rbars = self.params["range_bars"]
        atr_mult = self.params["atr_multiplier"]
        tgt_mult = self.params["target_multiplier"]
        ss, se = self.params["session_start"], self.params["session_end"]
        sk = bar.timestamp.strftime("%Y-%m-%d")
        if sk != self._current_session:
            self._current_session = sk
            self._session_high = self._session_low = None
            self._range_count = 0
            self._daily_prices = []
        self._daily_prices.append(bar.close)
        if len(self._daily_prices) > 14:
            self._atr = float(np.mean(np.abs(np.diff(np.array(self._daily_prices[-15:])))))

        ts = bar.timestamp.strftime("%H:%M")
        in_sesh = ss <= ts <= se or ss > se
        if in_sesh and self._range_count < rbars:
            self._session_high = max(self._session_high or 0, bar.high)
            self._session_low = min(self._session_low or float('inf'), bar.low)
            self._range_count += 1
            return orders
        if self._session_high is None:
            return orders

        atr = max(self._atr, bar.close * 0.002)
        if position.is_long:
            if bar.low <= (position.stop_loss or 0) or position.bars_held >= 60:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="orb_exit_long"))
        elif position.is_short:
            if bar.high >= (position.stop_loss or float('inf')) or position.bars_held >= 60:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="orb_exit_short"))
        elif in_sesh:
            if bar.close > self._session_high:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=qty, tag="orb_entry_long"))
            elif bar.close < self._session_low:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=qty, tag="orb_entry_short"))
        self.bar_index += 1
        return orders


class VWAPMeanReversion(Strategy):
    """
    VWAP Mean Reversion.
    Entra long quando prezzo è molto sotto VWAP (z-score > entry_z).
    Entra short quando molto sopra. Esce quando z torna verso 0.
    """
    def __init__(self, symbol: str, params: Optional[dict] = None):
        defaults = {"vwap_period": 20, "entry_z": 1.5, "exit_z": 0.5, "quantity": 1, "max_bars_hold": 60}
        super().__init__("VWAPMeanReversion", symbol, {**defaults, **(params or {})})
        self._prices: list[float] = []
        self._volumes: list[int] = []
        self._typ: list[float] = []

    def on_bar(self, bar: BarData, position: Position, regime: Optional[RegimeState] = None) -> list[Order]:
        orders = []
        qty = self.params["quantity"]
        period = self.params["vwap_period"]
        entry_z = self.params["entry_z"]
        exit_z = self.params["exit_z"]
        max_hold = self.params["max_bars_hold"]
        tp = (bar.high + bar.low + bar.close) / 3
        self._prices.append(bar.close)
        self._volumes.append(bar.volume)
        self._typ.append(tp)
        if len(self._prices) < period:
            return orders
        prices = np.array(self._prices[-period:])
        volumes = np.array(self._volumes[-period:], dtype=float)
        typ = np.array(self._typ[-period:])
        vwap = np.sum(typ * volumes) / np.sum(volumes) if np.sum(volumes) > 0 else np.mean(prices)
        z = (prices[-1] - vwap) / np.std(prices - vwap) if np.std(prices - vwap) > 0 else 0

        if position.is_long:
            if abs(z) < exit_z or position.bars_held >= max_hold:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="vwap_exit_long"))
        elif position.is_short:
            if abs(z) < exit_z or position.bars_held >= max_hold:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="vwap_exit_short"))
        else:
            if z < -entry_z:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=qty, tag="vwap_entry_long"))
            elif z > entry_z:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=qty, tag="vwap_entry_short"))
        self.bar_index += 1
        return orders


class IntradayMomentumSPY(Strategy):
    """
    Intraday Momentum (adattata per futures).
    Usa momentum intraday e gap dalla chiusura precedente.
    """
    def __init__(self, symbol: str, params: Optional[dict] = None):
        defaults = {"momentum_period": 10, "entry_threshold": 0.001, "stop_atr_mult": 1.5, "quantity": 1, "session_start": "14:30", "session_end": "21:00", "max_bars_hold": 60, "use_prev_close": True}
        super().__init__("IntradayMomentumSPY", symbol, {**defaults, **(params or {})})
        self._prices: list[float] = []
        self._prev_close: Optional[float] = None
        self._current_session: Optional[str] = None
        self._session_open: Optional[float] = None

    def on_bar(self, bar: BarData, position: Position, regime: Optional[RegimeState] = None) -> list[Order]:
        orders = []
        qty = self.params["quantity"]
        mom_p = self.params["momentum_period"]
        entry_th = self.params["entry_threshold"]
        ss, se = self.params["session_start"], self.params["session_end"]
        max_hold = self.params["max_bars_hold"]
        self._prices.append(bar.close)
        sk = bar.timestamp.strftime("%Y-%m-%d")
        if sk != self._current_session:
            self._current_session = sk
            self._session_open = bar.open
            if self.params["use_prev_close"] and len(self._prices) >= 5:
                self._prev_close = self._prices[-5]
        ts = bar.timestamp.strftime("%H:%M")
        if not (ss <= ts <= se or ss > se):
            return orders
        if len(self._prices) < mom_p + 1:
            return orders
        mom = bar.close / self._prices[-mom_p - 1] - 1
        gap = (bar.open / (self._prev_close or self._prices[0]) - 1)

        if position.is_long:
            if mom < -entry_th or position.bars_held >= max_hold:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="im_exit_long"))
        elif position.is_short:
            if mom > entry_th or position.bars_held >= max_hold:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=position.abs_qty, tag="im_exit_short"))
        else:
            if mom > entry_th and gap > 0:
                orders.append(Order(side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=qty, tag="im_entry_long"))
            elif mom < -entry_th and gap < 0:
                orders.append(Order(side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=qty, tag="im_entry_short"))
        self.bar_index += 1
        return orders


# ══════════════════════════════════════════════════════════════════════════
# SECTION 8 — Main Backtest Engine
# ══════════════════════════════════════════════════════════════════════════


class BacktestEngine:
    """Motore di backtest principale."""
    def __init__(self, symbol: str = "ES", initial_capital: float = 100_000.0, data_loader: Optional[DataLoader] = None):
        self.symbol = symbol.upper()
        self.initial_capital = initial_capital
        self.data_loader = data_loader or DataLoader()
        self.slippage_model = SlippageModel(self.symbol)
        self.fill_model = FillModel(self.symbol, self.slippage_model)
        self.regime_detector = RegimeDetector()
        self.stats_engine = StatisticsEngine()
        self.strategy: Optional[Strategy] = None
        self.data: Optional[pd.DataFrame] = None
        self.regime_data: Optional[pd.DataFrame] = None
        self.position = Position(self.symbol)
        self.trades: list[Trade] = []
        self.equity_curve: list[float] = []
        self.equity_dates: list[pd.Timestamp] = []
        self.daily_volume: int = 0
        self._orders: list[Order] = []
        self._next_order_id: int = 1
        self._avg_volume: float = 1000.0

    def set_data(self, start: Optional[str] = None, end: Optional[str] = None, df: Optional[pd.DataFrame] = None) -> None:
        if df is not None:
            self.data = df
        else:
            self.data = self.data_loader.load(self.symbol, start, end)
        if self.data is None or len(self.data) == 0:
            raise ValueError(f"Nessun dato per {self.symbol}")
        self._avg_volume = float(self.data["volume"].mean())
        print(f"  Dati: {len(self.data):,} bar | {self.data.index[0]:%Y-%m-%d} → {self.data.index[-1]:%Y-%m-%d} | Vol avg: {self._avg_volume:,.0f}")

    def set_strategy(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def run(self, mode: str = "realistico") -> BacktestStats:
        """
        Esegue il backtest in modalità 'ottimale' o 'realistico'.

        mode='ottimale':  nessuno slippage, nessuna commissione, fill al 100% al prezzo esatto
        mode='realistico': slippage variabile, commissioni $2.50/contract, fill model realistico (default)
        """
        if self.data is None:
            raise ValueError("Chiama set_data() prima di run()")
        if self.strategy is None:
            raise ValueError("Chiama set_strategy() prima di run()")
        print(f"\n  === {self.strategy.name} on {self.symbol} [{mode}] ===")
        print(f"  Capital: ${self.initial_capital:,.0f} | Bars: {len(self.data):,}")

        self.regime_data = self.regime_detector.compute(self.data)
        self.position = Position(self.symbol)
        self.trades = []
        self.equity_curve = [float(self.initial_capital)]
        self.equity_dates = [self.regime_data.index[0]]
        self.daily_volume = 0
        current_day = self.regime_data.index[0].date()
        n_bars = len(self.regime_data)
        last_pct = 0

        is_ottimale = (mode == "ottimale")

        for i in range(n_bars):
            row = self.regime_data.iloc[i]
            ts = self.regime_data.index[i]
            if ts.date() != current_day:
                self.daily_volume = 0
                current_day = ts.date()
            self.daily_volume += int(row["volume"])

            bar = BarData(timestamp=ts, open=float(row["open"]), high=float(row["high"]),
                          low=float(row["low"]), close=float(row["close"]),
                          volume=int(row["volume"]), symbol=self.symbol)

            regime = RegimeState(
                trend_strength=float(row["trend_strength"]),
                trend_direction=int(row["trend_direction"]),
                volatility_regime=str(row["volatility_regime"]),
                volatility_percentile=float(row["volatility_percentile"]),
                atr_percent=float(row["atr_pct"]),
                vix_proxy=float(row["vix_proxy"]),
                mean_reversion_prob=float(row["mr_prob"]),
                regime_label=str(row["regime_label"]),
                regime_code=int(row["regime_code"]),
            )

            # 1. Check exit conditions on open position
            exit_reason = self.position.on_bar(bar)
            if exit_reason is not None:
                self._close_position(bar, exit_reason, is_ottimale)

            # 2. Execute pending orders (mode-aware)
            self._process_orders(bar, is_ottimale)

            # 3. Strategy decision
            new_orders = self.strategy.on_bar(bar, self.position, regime)
            for order in new_orders:
                self._submit_order(order)

            # 4. Update unrealized PnL
            self.position.update_unrealized(bar.close)

            # 5. Track equity
            total_eq = self.initial_capital + self.position.realized_pnl + self.position.unrealized_pnl
            self.equity_curve.append(total_eq)
            self.equity_dates.append(ts)

            pct = (i + 1) * 100 // n_bars
            if pct >= last_pct + 10:
                print(f"  Progress: {pct}% ({i + 1:,}/{n_bars:,})")
                last_pct = pct

        # Close final position
        if not self.position.is_flat:
            last_bar = BarData(timestamp=self.regime_data.index[-1],
                               close=float(self.regime_data.iloc[-1]["close"]),
                               high=float(self.regime_data.iloc[-1]["close"]),
                               low=float(self.regime_data.iloc[-1]["close"]),
                               open=float(self.regime_data.iloc[-1]["close"]),
                               volume=0, symbol=self.symbol)
            trade = self.position.close_position(last_bar.close, last_bar.timestamp)
            trade.exit_reason = "end_of_data"
            if is_ottimale:
                trade.commission = 0.0
                trade.slippage = 0.0
            self.trades.append(trade)

        print(f"\n  ✓ Done: {len(self.trades)} trades [{mode}]")
        dates_idx = pd.DatetimeIndex(self.equity_dates) if self.equity_dates else None
        return self.stats_engine.compute(trades=self.trades, initial_capital=self.initial_capital,
                                          dates=dates_idx, equity_curve=np.array(self.equity_curve))

    def run_both(self) -> dict[str, BacktestStats]:
        """Esegue il backtest in entrambe le modalità e restituisce {'ottimale': ..., 'realistico': ...}."""
        print(f"\n  ╔{'═'*60}╗")
        print(f"  ║  Modalità OTTIMALE (no slippage, no commissioni, fill 100%)")
        print(f"  ╚{'═'*60}╝")
        ottimale = self.run(mode="ottimale")
        print(f"\n  ╔{'═'*60}╗")
        print(f"  ║  Modalità REALISTICO (slippage, commissioni, fill realistico)")
        print(f"  ╚{'═'*60}╝")
        realistico = self.run(mode="realistico")
        return {"ottimale": ottimale, "realistico": realistico}

    def _submit_order(self, order: Order) -> None:
        order.id = self._next_order_id
        self._next_order_id += 1
        order.status = "pending"
        order.timestamp = pd.Timestamp.now()
        self._orders.append(order)

    def _process_orders(self, bar: BarData, is_ottimale: bool = False) -> None:
        """Fill all pending orders on this bar. Filled orders are immediately removed."""
        to_remove = []
        for order in self._orders:
            if order.status in ("filled", "cancelled", "rejected"):
                to_remove.append(order)
                continue
            remaining = order.quantity - order.filled_qty
            if remaining <= 0:
                order.status = "filled"
                to_remove.append(order)
                continue

            if is_ottimale:
                # Modalità ottimale: fill al 100% al prezzo esatto, zero slippage, zero commissioni
                fill_price = float(bar.open) if order.order_type == OrderType.MARKET else float(order.price)
                result = FillResult(filled=True, fill_price=fill_price, fill_qty=remaining, slippage=0.0)
                commission = 0.0
                order.filled_qty += result.fill_qty
                order.commission += commission
                order.fill_log.append({"bar": bar.timestamp, "price": result.fill_price,
                                        "qty": result.fill_qty, "commission": commission, "slippage": 0.0})
                prev_cost = order.avg_fill_price * max(0, order.filled_qty - result.fill_qty)
                order.avg_fill_price = (prev_cost + result.fill_price * result.fill_qty) / order.filled_qty
                self._execute_fill(order, result, bar.timestamp, is_ottimale)
                if order.filled_qty >= order.quantity:
                    order.status = "filled"
                    to_remove.append(order)
                else:
                    order.status = "partial"
            else:
                result = self.fill_model.try_fill(order, bar, self._avg_volume, self.daily_volume)
                if result.filled:
                    commission = CommissionModel.compute(result.fill_qty, result.fill_price, self.daily_volume)
                    order.filled_qty += result.fill_qty
                    order.commission += commission
                    order.fill_log.append({"bar": bar.timestamp, "price": result.fill_price,
                                            "qty": result.fill_qty, "commission": commission, "slippage": result.slippage})
                    # Update avg fill price
                    prev_cost = order.avg_fill_price * max(0, order.filled_qty - result.fill_qty)
                    order.avg_fill_price = (prev_cost + result.fill_price * result.fill_qty) / order.filled_qty
                    # Execute on position
                    self._execute_fill(order, result, bar.timestamp)
                    if order.filled_qty >= order.quantity:
                        order.status = "filled"
                        to_remove.append(order)
                    else:
                        order.status = "partial"
                else:
                    to_remove.append(order)
        self._orders = [o for o in self._orders if o not in to_remove]

    def _execute_fill(self, order: Order, result: FillResult, timestamp: pd.Timestamp, is_ottimale: bool = False) -> None:
        """Apply fill to position using signed quantity."""
        qty = int(result.fill_qty)
        price = float(result.fill_price)

        if order.side == OrderSide.BUY:
            if self.position.is_short:
                # Reduce short
                trade = self.position.reduce_position(qty, price, timestamp)
                if trade:
                    self._finalize_trade(trade, order, result)
                remaining = qty - (trade.quantity if trade else 0)
                if remaining > 0 and not self.position.is_short:
                    self.position.open_long(remaining, price, timestamp)
            elif self.position.is_long:
                self.position.open_long(qty, price, timestamp)
            else:  # FLAT
                self.position.open_long(qty, price, timestamp)
        else:  # SELL
            if self.position.is_long:
                # Reduce long
                trade = self.position.reduce_position(qty, price, timestamp)
                if trade:
                    self._finalize_trade(trade, order, result)
                remaining = qty - (trade.quantity if trade else 0)
                if remaining > 0 and not self.position.is_long:
                    self.position.open_short(remaining, price, timestamp)
            elif self.position.is_short:
                self.position.open_short(qty, price, timestamp)
            else:  # FLAT
                self.position.open_short(qty, price, timestamp)

        self.strategy.on_position_change(self.position)

    def _close_position(self, bar: BarData, reason: str, is_ottimale: bool = False) -> None:
        if self.position.is_flat:
            return
        sl = self.position.stop_loss
        tp = self.position.take_profit
        if reason == "stop_loss" and sl is not None:
            exit_price = sl
        elif reason == "take_profit" and tp is not None:
            exit_price = tp
        elif reason == "trailing_stop" and self.position.trailing_stop_price is not None:
            exit_price = self.position.trailing_stop_price
        else:
            exit_price = bar.close
        trade = self.position.close_position(exit_price, bar.timestamp)
        trade.exit_reason = reason
        if is_ottimale:
            trade.commission = 0.0
            trade.slippage = 0.0
            trade.net_pnl = trade.gross_pnl
        else:
            trade.commission = CommissionModel.compute(trade.quantity, exit_price, self.daily_volume)
            trade.net_pnl = trade.gross_pnl - trade.commission
        self.trades.append(trade)
        self.strategy.on_trade(trade)

    def _finalize_trade(self, trade: Trade, order: Order, result: FillResult) -> None:
        trade.commission += order.commission
        trade.slippage += result.slippage * result.fill_qty * POINT_VALUE.get(self.symbol, 50.0)
        trade.net_pnl = trade.gross_pnl - trade.commission
        self.trades.append(trade)
        self.strategy.on_trade(trade)

    def get_report(self, stats: Optional[BacktestStats] = None) -> dict:
        if stats is None:
            stats = self.run() if not hasattr(self, '_last_stats') else self._last_stats
            self._last_stats = stats

        trades_df = pd.DataFrame([{
            "date": t.exit_time, "trade_return": t.net_pnl, "direction": t.direction,
            "regime": "is", "exit_reason": t.exit_reason, "entry_price": t.entry_price,
            "exit_price": t.exit_price, "quantity": t.quantity, "bars_held": t.bars_held,
        } for t in self.trades])

        if stats.equity_curve is not None and len(trades_df) > 0:
            eq_s = pd.Series(stats.equity_curve, index=pd.DatetimeIndex(self.equity_dates))
            trades_df["equity"] = trades_df["date"].apply(lambda d: eq_s.asof(d) if d >= eq_s.index[0] else stats.equity_curve[0])
            peak = trades_df["equity"].expanding().max()
            trades_df["drawdown"] = (trades_df["equity"] - peak) / peak * 100
            split = int(len(trades_df) * 0.7)
            trades_df.iloc[:split, trades_df.columns.get_loc("regime")] = "is"
            trades_df.iloc[split:, trades_df.columns.get_loc("regime")] = "oos"

        return {
            "stats": stats,
            "trades_df": trades_df,
            "summary": {
                "strategy": self.strategy.name if self.strategy else "Unknown",
                "symbol": self.symbol,
                "period": {"start": str(self.equity_dates[0]) if self.equity_dates else None,
                           "end": str(self.equity_dates[-1]) if self.equity_dates else None},
                "initial_capital": self.initial_capital,
                "total_trades": stats.total_trades,
                "total_net_pnl": stats.total_net_pnl,
                "total_commission": stats.total_commission,
                "total_slippage": stats.total_slippage,
                "win_rate": stats.win_rate,
                "profit_factor": stats.profit_factor,
                "sharpe_ratio": stats.sharpe_ratio,
                "sortino_ratio": stats.sortino_ratio,
                "calmar_ratio": stats.calmar_ratio,
                "cagr": stats.cagr,
                "max_drawdown_pct": stats.max_drawdown_pct,
                "avg_trade_pnl": stats.avg_trade_pnl,
                "expectancy": stats.expectancy,
                "mc_prob_positive": stats.mc_prob_positive,
            },
            "regime_distribution": self.regime_data["regime_label"].value_counts().to_dict() if self.regime_data is not None and "regime_label" in self.regime_data.columns else {},
            "trade_distribution": {
                "mean": float(np.mean([t.net_pnl for t in self.trades])),
                "median": float(np.median([t.net_pnl for t in self.trades])),
                "std": float(np.std([t.net_pnl for t in self.trades])),
                "min": float(min(t.net_pnl for t in self.trades)),
                "max": float(max(t.net_pnl for t in self.trades)),
            } if self.trades else {},
            "equity_dates": [str(d) for d in self.equity_dates],
            "equity_values": [float(v) for v in self.equity_curve],
        }

    def print_summary(self, stats: Optional[BacktestStats] = None) -> None:
        if stats is None:
            stats = self._last_stats if hasattr(self, '_last_stats') else self.run()
            self._last_stats = stats
        print(f"\n{'='*65}")
        print(f"  BACKTEST — {self.strategy.name} on {self.symbol}")
        print(f"{'='*65}")
        print(f"  {'Trades':20s} {stats.total_trades:>8d}")
        print(f"  {'Win Rate':20s} {stats.win_rate:>8.1f}%")
        print(f"  {'Profit Factor':20s} {stats.profit_factor:>8.2f}")
        print(f"  {'Total Net PnL':20s} ${stats.total_net_pnl:>+8,.0f}")
        print(f"  {'Avg Trade':20s} ${stats.avg_trade_pnl:>+8,.0f}")
        print(f"  {'Commission':20s} ${stats.total_commission:>8,.0f}")
        print(f"  {'Slippage':20s} ${stats.total_slippage:>8,.0f}")
        print(f"  {'Sharpe Ratio':20s} {stats.sharpe_ratio:>8.2f}")
        print(f"  {'Sortino Ratio':20s} {stats.sortino_ratio:>8.2f}")
        print(f"  {'Calmar Ratio':20s} {stats.calmar_ratio:>8.2f}")
        print(f"  {'CAGR':20s} {stats.cagr:>8.2f}%")
        print(f"  {'Max Drawdown':20s} {stats.max_drawdown_pct:>8.2f}%")
        print(f"  {'Expectancy':20s} ${stats.expectancy:>+8,.0f}")
        print(f"  {'Long/Short':20s} {stats.total_long}/{stats.total_short}")
        print(f"  {'Avg Bars Held':20s} {stats.avg_bars_held:>8.1f}")
        print(f"  {'MC Pos Prob':20s} {stats.mc_prob_positive:>8.1f}%")
        print(f"{'='*65}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 9 — CLI & Demo
# ══════════════════════════════════════════════════════════════════════════

_STRATEGY_REGISTRY = {
    "TSMomentum": TimeSeriesMomentum,
    "OpeningRangeBreakout": OpeningRangeBreakout,
    "VWAPMeanReversion": VWAPMeanReversion,
    "IntradayMomentumSPY": IntradayMomentumSPY,
}


def list_strategies() -> None:
    print("\n  Available strategies:")
    print(f"  {'─'*50}")
    for name, cls in _STRATEGY_REGISTRY.items():
        doc = (cls.__doc__ or "").strip().split("\n")[0]
        print(f"  {name:<25s} {doc}")
    print()


def run_demo() -> None:
    print(f"\n  ╔{'═'*60}╗")
    print(f"  ║  Capo Horn Lab — Backtest Engine Demo")
    print(f"  ╚{'═'*60}╝")
    loader = DataLoader()
    smoke_path = loader.data_dir / "ES" / "ES_1m_smoke_test.parquet"
    if smoke_path.exists():
        df = pd.read_parquet(smoke_path)
        if "ts_event" in df.columns:
            df = df.set_index("ts_event")
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
    else:
        df = loader.load("ES", start="2024-01-02", end="2024-01-05")
    print(f"\n  Data: {len(df)} bars OHLCV")

    for name, strat_cls in _STRATEGY_REGISTRY.items():
        print(f"\n  {'─'*60}")
        strategy = strat_cls("ES")
        engine = BacktestEngine(symbol="ES", data_loader=loader)
        engine.set_data(df=df)
        engine.set_strategy(strategy)
        engine.print_summary(engine.run())
    print(f"\n  ✅ Demo done.\n")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Capo Horn Lab — Backtest Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python backtest_engine.py --demo
  python backtest_engine.py --strategy TSMomentum
  python backtest_engine.py --list
  python backtest_engine.py --symbol NQ --strategy VWAPMeanReversion --start 2023-01-01 --end 2023-06-01
        """,
    )
    parser.add_argument("--symbol", default="ES", help="Symbol (ES, NQ, CL)")
    parser.add_argument("--strategy", type=str, help="Strategy name")
    parser.add_argument("--start", type=str, help="Start date")
    parser.add_argument("--end", type=str, help="End date")
    parser.add_argument("--capital", type=float, default=100_000.0, help="Initial capital")
    parser.add_argument("--list", action="store_true", help="List strategies")
    parser.add_argument("--demo", action="store_true", help="Demo with smoke test")
    args = parser.parse_args()
    if args.demo:
        run_demo()
        return
    if args.list:
        list_strategies()
        return
    if args.strategy:
        strat_cls = _STRATEGY_REGISTRY.get(args.strategy)
        if strat_cls is None:
            print(f"❌ Strategy '{args.strategy}' not found.")
            list_strategies()
            return
        strategy = strat_cls(args.symbol)
        engine = BacktestEngine(symbol=args.symbol, initial_capital=args.capital)
        engine.set_data(start=args.start, end=args.end)
        engine.set_strategy(strategy)
        engine.print_summary(engine.run())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

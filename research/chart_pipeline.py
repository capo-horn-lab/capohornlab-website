#!/usr/bin/env python3
"""
chart_pipeline.py — Capo Horn Lab Research Chart Pipeline (MVP 7 Charts)
=======================================================================

Genera 7 grafici statistici standard per ogni ricerca pubblicata:

  1. Equity Curve          — Line chart cumulativo (plotly + mpl)
  2. Drawdown              — Area chart con linea -20%
  3. Trade Distribution    — Histogram + Kernel density
  4. Monthly Heatmap       — PnL per mese (mesi × anni)
  5. Long vs Short         — Bar chart comparativo per direzione
  6. Performance Table     — Tabella riepilogativa metriche
  7. IS vs OOS             — Bar chart comparativo IS vs OOS

Input:  CSV con colonne: date, equity, drawdown, trade_return,
        direction(long/short), regime(is/oos)
Output: PNG + HTML interattivo in output-dir

Palette Capo Horn: navy #0F172A, teal #14B8A6, rose #E11D48, amber #F59E0B

Usage:
    python chart_pipeline.py --csv trades.csv --output-dir ./charts
    python chart_pipeline.py --demo                     # synthetic data
    python chart_pipeline.py --help
"""

from __future__ import annotations

import argparse
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

# ── Capo Horn Lab Design Tokens ──────────────────────────────────────────
NAVY = "#0F172A"
TEAL = "#14B8A6"
ROSE = "#E11D48"
AMBER = "#F59E0B"
SLATE_100 = "#F1F5F9"
SLATE_300 = "#CBD5E1"
SLATE_500 = "#64748B"
SLATE_700 = "#334155"
WHITE = "#FFFFFF"
PALETTE = [NAVY, TEAL, ROSE, AMBER, "#8B5CF6", "#06B6D4", "#F97316", "#22C55E"]

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "charts"


# ══════════════════════════════════════════════════════════════════════════
# PLOTLY HELPERS
# ══════════════════════════════════════════════════════════════════════════

def _plotly_template(title: str) -> dict:
    return dict(
        paper_bgcolor=NAVY, plot_bgcolor=NAVY,
        font_family="Inter, system-ui, sans-serif", font_color=SLATE_100,
        title=dict(text=title, font_size=20, font_color=WHITE, x=0.5, xanchor="center"),
        hovermode="x unified", margin=dict(l=60, r=30, t=60, b=60),
        xaxis=dict(gridcolor=SLATE_700, zerolinecolor=SLATE_500, tickfont_color=SLATE_300, title_font_color=SLATE_100),
        yaxis=dict(gridcolor=SLATE_700, zerolinecolor=SLATE_500, tickfont_color=SLATE_300, title_font_color=SLATE_100),
        legend=dict(font_color=SLATE_100, bgcolor="rgba(0,0,0,0.3)", bordercolor=SLATE_700, borderwidth=1),
    )


def _plotly_save(fig, stem: str, output_dir: Path):
    html_path = output_dir / f"{stem}.html"
    png_path = output_dir / f"{stem}.png"
    fig.write_html(str(html_path), include_plotlyjs="cdn", full_html=False)
    fig.write_image(str(png_path), width=1200, height=675, scale=1.5)
    print(f"  ✔ {html_path.name} / {png_path.name}")


def _import_plotly():
    import plotly.graph_objects as go
    return go


# ══════════════════════════════════════════════════════════════════════════
# MATPLOTLIB HELPERS
# ══════════════════════════════════════════════════════════════════════════

def _mpl_style():
    import matplotlib.pyplot as plt
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": NAVY, "axes.facecolor": NAVY,
        "axes.edgecolor": SLATE_700, "axes.labelcolor": SLATE_100,
        "axes.titlecolor": WHITE, "text.color": SLATE_100,
        "xtick.color": SLATE_300, "ytick.color": SLATE_300,
        "grid.color": SLATE_700, "grid.alpha": 0.3,
        "legend.facecolor": "black", "legend.edgecolor": SLATE_700,
        "legend.labelcolor": SLATE_100, "font.family": "sans-serif",
    })


def _mpl_save(fig, stem: str, output_dir: Path, dpi: int = 150):
    import matplotlib.pyplot as plt
    path = output_dir / f"{stem}.png"
    fig.savefig(str(path), dpi=dpi, bbox_inches="tight", facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"  ✔ {path.name}")


def _import_mpl():
    import matplotlib.figure
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import matplotlib.colors as mcolors
    import seaborn as sns
    return plt, mticker, mcolors, sns


# ══════════════════════════════════════════════════════════════════════════
# CHART 1: EQUITY CURVE
# ══════════════════════════════════════════════════════════════════════════

def chart_equity_curve(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    dates_raw = df["date"] if "date" in df.columns else df.index
    # Keep original for mpl, string for plotly JSON safety
    dates = dates_raw.astype(str).tolist() if hasattr(dates_raw, 'tolist') else list(dates_raw)
    dates_orig = dates_raw

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=df["equity"], mode="lines", name="Equity", line=dict(color=TEAL, width=2)))
    oos_mask = None
    if "regime" in df.columns:
        oos_mask = df["regime"].str.lower().str.contains("oos|test|out", na=False)
        if oos_mask.any():
            oos_idx = np.where(oos_mask)[0]
            oos_start_str, oos_end_str = dates[oos_idx[0]], dates[oos_idx[-1]]
            fig.add_vrect(x0=oos_start_str, x1=oos_end_str, fillcolor=AMBER, opacity=0.08, layer="below", line_width=0)
            fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="OOS Region", line=dict(color="rgba(0,0,0,0)"), fillcolor=AMBER, opacity=0.08, showlegend=True))
    fig.update_layout(**_plotly_template("Equity Curve"))
    fig.update_yaxes(title_text="Equity ($)")
    fig.update_xaxes(title_text="Date")
    _plotly_save(fig, "01_equity_curve", output_dir)

    plt, _, _, _ = _import_mpl()
    _mpl_style()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.fill_between(dates_orig, df["equity"], 0, alpha=0.08, color=TEAL)
    ax.plot(dates_orig, df["equity"], color=TEAL, linewidth=1.5, label="Equity")
    if oos_mask is not None and oos_mask.any():
        oos_start = dates_orig.iloc[oos_idx[0]]
        oos_end = dates_orig.iloc[oos_idx[-1]]
        ax.axvspan(oos_start, oos_end, alpha=0.06, color=AMBER, label="OOS Region")
    ax.axhline(y=0, color=SLATE_500, linewidth=0.5, linestyle="--")
    ax.set_title("Equity Curve", fontsize=16, fontweight="bold")
    ax.set_ylabel("Equity ($)")
    ax.set_xlabel("Date")
    ax.legend(loc="upper left")
    _mpl_save(fig, "01_equity_curve", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 2: DRAWDOWN
# ══════════════════════════════════════════════════════════════════════════

def chart_drawdown(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    dates_raw = df["date"] if "date" in df.columns else df.index
    dates = dates_raw.astype(str).tolist() if hasattr(dates_raw, 'tolist') else list(dates_raw)
    dates_orig = dates_raw
    dd_col = "drawdown" if "drawdown" in df.columns else "equity"
    dd_vals = df[dd_col].where(df[dd_col] <= 0, 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=dd_vals, mode="lines", name="Drawdown", line=dict(color=ROSE, width=2), fill="tozeroy", fillcolor="rgba(225,29,72,0.15)"))
    fig.add_hline(y=-20, line_dash="dash", line_color=AMBER, line_width=1.5, annotation_text="-20%", annotation_position="right")
    fig.update_layout(**_plotly_template("Drawdown"))
    fig.update_yaxes(title_text="Drawdown (%)", ticksuffix="%")
    fig.update_xaxes(title_text="Date")
    _plotly_save(fig, "02_drawdown", output_dir)

    plt, _, _, _ = _import_mpl()
    _mpl_style()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.fill_between(dates_orig, dd_vals, 0, alpha=0.12, color=ROSE)
    ax.plot(dates_orig, dd_vals, color=ROSE, linewidth=1.5, label="Drawdown")
    ax.axhline(y=-20, color=AMBER, linewidth=1, linestyle="--", alpha=0.7, label="-20% Reference")
    ax.set_title("Drawdown", fontsize=16, fontweight="bold")
    ax.set_ylabel("Drawdown (%)")
    ax.set_xlabel("Date")
    ax.legend(loc="lower left")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    _mpl_save(fig, "02_drawdown", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 3: TRADE DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════

def chart_trade_distribution(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    plt, _, _, sns = _import_mpl()
    _mpl_style()

    trades_col = "trade_return" if "trade_return" in df.columns else "equity"
    trades = df[trades_col].dropna().values
    mean_val, median_val = trades.mean(), np.median(trades)
    skew_val = pd.Series(trades).skew()

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=trades, nbinsx=50, name="Trade PnL", marker_color=TEAL, opacity=0.6))
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(trades)
    x_grid = np.linspace(trades.min(), trades.max(), 200)
    hist_area = len(trades) * (trades.max() - trades.min()) / 50
    fig.add_trace(go.Scatter(x=x_grid, y=kde(x_grid) * hist_area, mode="lines", name="Density", line=dict(color=AMBER, width=2)))
    fig.add_vline(x=mean_val, line_dash="dash", line_color=ROSE, line_width=1.5, annotation_text=f"Mean: {mean_val:.2f}")
    fig.add_vline(x=median_val, line_dash="dot", line_color=AMBER, line_width=1.5, annotation_text=f"Median: {median_val:.2f}")
    fig.update_layout(**_plotly_template(f"Trade Distribution &nbsp;&nbsp;·&nbsp;&nbsp; Skew: {skew_val:.2f}"))
    fig.update_xaxes(title_text="Trade PnL ($)")
    fig.update_yaxes(title_text="Frequency")
    _plotly_save(fig, "03_trade_distribution", output_dir)

    fig, ax = plt.subplots(figsize=(16, 9))
    sns.histplot(trades, bins=50, color=TEAL, alpha=0.5, stat="count", ax=ax)
    ax2 = ax.twinx()
    sns.kdeplot(trades, color=AMBER, linewidth=2, ax=ax2)
    ax2.set_ylabel("Density", color=AMBER)
    ax2.tick_params(colors=AMBER)
    ax.axvline(mean_val, color=ROSE, linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.2f}")
    ax.axvline(median_val, color=AMBER, linestyle=":", linewidth=1.5, label=f"Median: {median_val:.2f}")
    ax.set_title(f"Trade Distribution — Skew: {skew_val:.2f}", fontsize=16, fontweight="bold")
    ax.set_xlabel("Trade PnL ($)")
    ax.set_ylabel("Frequency")
    ax.legend(loc="upper right")
    _mpl_save(fig, "03_trade_distribution", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 4: MONTHLY HEATMAP
# ══════════════════════════════════════════════════════════════════════════

def chart_monthly_heatmap(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    plt, _, mcolors, sns = _import_mpl()
    _mpl_style()

    dates = pd.to_datetime(df["date"] if "date" in df.columns else df.index)
    trades_col = "trade_return" if "trade_return" in df.columns else "equity"
    tmp = df.copy()
    # handle both Series and DatetimeIndex
    if isinstance(dates, pd.DatetimeIndex):
        tmp["year"] = dates.year
        tmp["month"] = dates.month
    else:
        tmp["year"] = dates.dt.year
        tmp["month"] = dates.dt.month
    mpnl = tmp.groupby(["year", "month"])[trades_col].sum().reset_index()
    pivot = mpnl.pivot_table(index="year", columns="month", values=trades_col, aggfunc="sum")
    for m in range(1, 13):
        if m not in pivot.columns:
            pivot[m] = np.nan
    pivot = pivot[sorted(pivot.columns)]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot.columns = [month_labels[c - 1] for c in pivot.columns]
    z_data, years = pivot.values, pivot.index.astype(str).tolist()

    fig = go.Figure(data=go.Heatmap(
        z=z_data, x=list(pivot.columns), y=years,
        colorscale=[[0.0, ROSE], [0.45, "#1a1a2e"], [0.5, NAVY], [0.55, "#1a2e2e"], [1.0, TEAL]],
        zmid=0,
        text=np.where(np.isnan(z_data), "", np.vectorize(lambda v: f"{v:+,.0f}")(z_data)),
        texttemplate="%{text}", textfont=dict(size=10, color=WHITE),
        hoverongaps=False,
        hovertemplate="Year: %{y}<br>Month: %{x}<br>PnL: %{z:+,.2f}<extra></extra>",
    ))
    fig.update_layout(**_plotly_template("Monthly PnL Heatmap"), height=200 + 40 * len(years))
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Year")
    _plotly_save(fig, "04_monthly_heatmap", output_dir)

    fig, ax = plt.subplots(figsize=(16, max(5, 1 + 0.4 * len(years))))
    cmap = mcolors.LinearSegmentedColormap.from_list("capohorn", [ROSE, NAVY, TEAL], N=256)
    sns.heatmap(pivot, cmap=cmap, center=0, annot=True, fmt="+,.0f", linewidths=0.5, linecolor=SLATE_700, cbar_kws={"label": "PnL ($)", "shrink": 0.75}, ax=ax)
    ax.set_title("Monthly PnL Heatmap", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.tick_params(colors=SLATE_100)
    _mpl_save(fig, "04_monthly_heatmap", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 5: LONG VS SHORT
# ══════════════════════════════════════════════════════════════════════════

def chart_long_short(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    if "direction" not in df.columns or "trade_return" not in df.columns:
        print("  \u26a0 Skipping Long/Short chart: missing 'direction' or 'trade_return' column")
        return

    direction = df["direction"].str.lower().str.strip()
    long_mask = direction.isin(["long", "l"])
    short_mask = direction.isin(["short", "s"])

    def _metrics(mask, label):
        sub = df.loc[mask, "trade_return"]
        if len(sub) == 0:
            return {"label": label, "n_trades": 0, "win_rate": 0, "profit_factor": 0, "avg_trade": 0, "total_pnl": 0}
        wins = sub[sub > 0]
        losses = sub[sub < 0]
        pf = abs(wins.sum() / losses.sum()) if losses.sum() != 0 else float("inf")
        return {"label": label, "n_trades": len(sub), "win_rate": len(wins) / len(sub) * 100, "profit_factor": pf if pf != float("inf") else 0, "avg_trade": sub.mean(), "total_pnl": sub.sum()}

    long_m, short_m = _metrics(long_mask, "Long"), _metrics(short_mask, "Short")

    categories = ["Win Rate (%)", "Profit Factor", "Avg Trade ($)", "Total PnL ($)"]
    fig = go.Figure()
    for idx, (m, color) in enumerate([(long_m, TEAL), (short_m, ROSE)]):
        vals = [m["win_rate"], m["profit_factor"], m["avg_trade"], m["total_pnl"]]
        fig.add_trace(go.Bar(name=m["label"], x=categories, y=vals, marker_color=color, offsetgroup=idx, width=0.35, text=[f"{v:+,.1f}" if abs(v) < 1000 else f"{v:+,.0f}" for v in vals], textposition="outside"))
    fig.update_layout(**_plotly_template(f"Long vs Short &nbsp;&nbsp;·&nbsp;&nbsp; Long: {long_m['n_trades']} trades &nbsp;|&nbsp; Short: {short_m['n_trades']} trades"), barmode="group", bargap=0.25)
    fig.update_yaxes(title_text="Value")
    _plotly_save(fig, "05_long_vs_short", output_dir)

    plt, _, _, _ = _import_mpl()
    _mpl_style()
    fig, axes = plt.subplots(1, 4, figsize=(20, 7))
    labels = [long_m, short_m]
    colors = [TEAL, ROSE]
    bar_data = [("Win Rate (%)", [m["win_rate"] for m in labels], "%", "+,.1f"), ("Profit Factor", [m["profit_factor"] for m in labels], "", "+,.2f"), ("Avg Trade ($)", [m["avg_trade"] for m in labels], "$", "+,.2f"), ("Total PnL ($)", [m["total_pnl"] for m in labels], "$", "+,.0f")]
    for ax, (title, vals, prefix, fmt) in zip(axes, bar_data):
        bars = ax.bar(["Long", "Short"], vals, color=colors, width=0.5)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{prefix}{v:{fmt}}", ha="center", va="bottom", fontsize=11, color=SLATE_100)
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.tick_params(colors=SLATE_100)
        ax.set_facecolor(NAVY)
        for spine in ax.spines.values():
            spine.set_color(SLATE_700)
    fig.suptitle("Long vs Short Comparison", fontsize=18, fontweight="bold", y=1.02)
    plt.tight_layout()
    _mpl_save(fig, "05_long_vs_short", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 6: PERFORMANCE TABLE
# ══════════════════════════════════════════════════════════════════════════

def _compute_perf_metrics(df: pd.DataFrame, regime_filter: str = None) -> dict:
    sub = df.copy()
    if regime_filter and "regime" in sub.columns:
        sub = sub[sub["regime"].str.lower().str.contains(regime_filter, na=False)]
    trades = sub["trade_return"].dropna() if "trade_return" in sub.columns else sub["equity"].dropna()
    eq = sub["equity"] if "equity" in sub.columns else trades.cumsum()

    n_trades = len(trades)
    if n_trades == 0:
        return {k: 0 for k in ["n_trades", "cagr", "sharpe", "sortino", "calmar", "profit_factor", "win_rate", "avg_trade", "max_dd", "pct_positive", "total_pnl"]}

    wins, losses = trades[trades > 0], trades[trades < 0]
    total_pnl = trades.sum()
    win_rate = len(wins) / n_trades * 100
    avg_trade = trades.mean()
    pct_positive = (trades > 0).mean() * 100
    loss_sum = abs(losses.sum()) if len(losses) else 0
    profit_factor = abs(wins.sum() / loss_sum) if loss_sum != 0 else (999.0 if len(wins) else 0)

    if len(eq) > 1:
        peak = eq.expanding().max()
        dd = (eq - peak) / peak * 100
        max_dd = dd.min()
        total_days = len(sub)
        years = total_days / 252
        cagr = ((eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1) * 100 if years > 0 and eq.iloc[0] != 0 else 0.0
    else:
        max_dd, cagr = 0.0, 0.0

    daily_returns = trades if len(trades) < len(eq) else eq.pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std()) * (252 ** 0.5) if len(daily_returns) > 1 and daily_returns.std() > 0 else 0.0
    downside = daily_returns[daily_returns < 0]
    sortino = (daily_returns.mean() / downside.std()) * (252 ** 0.5) if len(downside) > 1 and downside.std() > 0 else 0.0
    calmar = cagr / abs(max_dd) if max_dd != 0 else 0.0

    return {"n_trades": n_trades, "total_pnl": total_pnl, "cagr": cagr, "sharpe": sharpe, "sortino": sortino, "calmar": calmar, "profit_factor": profit_factor, "win_rate": win_rate, "avg_trade": avg_trade, "max_dd": max_dd, "pct_positive": pct_positive}


_METRIC_FORMATS = {
    "n_trades": lambda x: f"{int(x)}",
    "total_pnl": lambda x: f"${x:+,.0f}",
    "cagr": lambda x: f"{x:+.2f}%",
    "sharpe": lambda x: f"{x:.2f}",
    "sortino": lambda x: f"{x:.2f}",
    "calmar": lambda x: f"{x:.2f}",
    "profit_factor": lambda x: f"{x:.2f}",
    "win_rate": lambda x: f"{x:.1f}%",
    "avg_trade": lambda x: f"${x:+,.2f}",
    "max_dd": lambda x: f"{x:.1f}%",
    "pct_positive": lambda x: f"{x:.1f}%",
}

_METRIC_NAMES = {
    "n_trades": "N Trades", "total_pnl": "Total PnL", "cagr": "CAGR",
    "sharpe": "Sharpe Ratio", "sortino": "Sortino Ratio", "calmar": "Calmar Ratio",
    "profit_factor": "Profit Factor", "win_rate": "Win Rate", "avg_trade": "Avg Trade",
    "max_dd": "Max Drawdown", "pct_positive": "% Positive Trades",
}


def chart_performance_table(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()
    m = _compute_perf_metrics(df)
    rows = [(_METRIC_NAMES[k], _METRIC_FORMATS[k](m[k])) for k in _METRIC_NAMES]

    fig = go.Figure(data=[go.Table(
        header=dict(values=["Metric", "Value"], fill_color=NAVY, font=dict(color=WHITE, size=14, family="Inter"), align="center", height=36),
        cells=dict(values=[[r[0] for r in rows], [r[1] for r in rows]], fill_color=[SLATE_700, SLATE_500], font=dict(color=WHITE, size=13), align=["left", "center"], height=30),
    )])
    fig.update_layout(**_plotly_template("Performance Summary"), height=60 + 35 * len(rows))
    _plotly_save(fig, "06_performance_table", output_dir)

    plt, _, _, _ = _import_mpl()
    _mpl_style()
    fig, ax = plt.subplots(figsize=(12, 3 + 0.35 * len(rows)))
    ax.axis("off")
    table = ax.table(cellText=[[r[0], r[1]] for r in rows], colLabels=["Metric", "Value"], cellLoc="left", loc="center", colWidths=[0.4, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    for j in range(2):
        table[0, j].set_facecolor(NAVY)
        table[0, j].set_text_props(color=WHITE, fontweight="bold")
        table[0, j].set_edgecolor(SLATE_700)
    for i in range(1, len(rows) + 1):
        for j in range(2):
            table[i, j].set_edgecolor(NAVY)
            table[i, j].set_height(0.06)
        table[i, 0].set_facecolor(SLATE_700)
        table[i, 1].set_facecolor(SLATE_500)
        table[i, 0].set_text_props(color=WHITE)
        table[i, 1].set_text_props(color=WHITE)
    ax.set_title("Performance Summary", fontsize=16, fontweight="bold", pad=20)
    _mpl_save(fig, "06_performance_table", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# CHART 7: IS vs OOS
# ══════════════════════════════════════════════════════════════════════════

def chart_is_oos(df: pd.DataFrame, output_dir: Path):
    go = _import_plotly()

    if "regime" not in df.columns or "trade_return" not in df.columns:
        print("  \u26a0 Skipping IS/OOS chart: missing 'regime' or 'trade_return' column")
        return

    is_metrics = _compute_perf_metrics(df, "is|in|train")
    oos_metrics = _compute_perf_metrics(df, "oos|test|out")

    categories = ["Sharpe", "Max DD (%)", "Profit Factor"]
    is_vals = [is_metrics["sharpe"], is_metrics["max_dd"], is_metrics["profit_factor"]]
    oos_vals = [oos_metrics["sharpe"], oos_metrics["max_dd"], oos_metrics["profit_factor"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="IS", x=categories, y=is_vals, marker_color=TEAL, offsetgroup=0, width=0.35, text=[f"{v:.2f}" for v in is_vals], textposition="outside"))
    fig.add_trace(go.Bar(name="OOS", x=categories, y=oos_vals, marker_color=ROSE, offsetgroup=1, width=0.35, text=[f"{v:.2f}" for v in oos_vals], textposition="outside"))
    fig.update_layout(**_plotly_template(f"IS vs OOS &nbsp;&nbsp;·&nbsp;&nbsp; IS: {is_metrics['n_trades']} trades | OOS: {oos_metrics['n_trades']} trades"), barmode="group", bargap=0.25)
    fig.update_yaxes(title_text="Value")
    _plotly_save(fig, "07_is_vs_oos", output_dir)

    plt, _, _, _ = _import_mpl()
    _mpl_style()
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    colors = [TEAL, ROSE]
    for ax, (cat, isv, oosv) in zip(axes, zip(categories, is_vals, oos_vals)):
        bars = ax.bar(["IS", "OOS"], [isv, oosv], color=colors, width=0.5)
        for bar, v in zip(bars, [isv, oosv]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{v:.2f}", ha="center", va="bottom", fontsize=12, color=SLATE_100)
        ax.set_title(cat, fontsize=14, fontweight="bold")
        ax.tick_params(colors=SLATE_100)
        ax.set_facecolor(NAVY)
        for spine in ax.spines.values():
            spine.set_color(SLATE_700)

    # R² stability bar
    is_sharpe, oos_sharpe = is_metrics["sharpe"], oos_metrics["sharpe"]
    r2 = (1 - abs((oos_sharpe - is_sharpe) / (is_sharpe + 1e-8))) * 100
    r2 = max(0, min(100, r2))
    fig.text(0.5, 0.02, f"Stability (IS\u2192OOS R\u00b2 approximated): {r2:.1f}%", ha="center", fontsize=14, color=TEAL, fontweight="bold", transform=fig.transFigure)

    fig.suptitle("IS vs OOS Comparison", fontsize=18, fontweight="bold", y=1.02)
    plt.tight_layout()
    _mpl_save(fig, "07_is_vs_oos", output_dir)


# ══════════════════════════════════════════════════════════════════════════
# DEMO DATA GENERATOR
# ══════════════════════════════════════════════════════════════════════════

def generate_demo_data(n_days: int = 2520) -> pd.DataFrame:
    """Generate realistic-ish synthetic trade data for demo purposes."""
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=n_days, freq="D")

    # Walk with drift + noise for equity
    daily_ret = np.random.normal(0.0005, 0.012, n_days)
    equity = 100000 * np.cumprod(1 + daily_ret)

    # Drawdown
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak * 100

    # Trade returns (synthetic)
    trade_return = np.random.normal(0, 200, n_days)
    trade_return[::3] *= 1.5  # occasional larger moves

    # Direction
    direction = np.random.choice(["long", "short"], n_days)

    # Regime (first 70% IS, last 30% OOS)
    split = int(n_days * 0.7)
    regime = np.array(["is"] * split + ["oos"] * (n_days - split))

    return pd.DataFrame({
        "date": dates,
        "equity": equity,
        "drawdown": drawdown,
        "trade_return": trade_return,
        "direction": direction,
        "regime": regime,
    })


# ══════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════

CHART_FUNCTIONS = [
    ("01_equity_curve", chart_equity_curve),
    ("02_drawdown", chart_drawdown),
    ("03_trade_distribution", chart_trade_distribution),
    ("04_monthly_heatmap", chart_monthly_heatmap),
    ("05_long_vs_short", chart_long_short),
    ("06_performance_table", chart_performance_table),
    ("07_is_vs_oos", chart_is_oos),
]


def run_pipeline(df: pd.DataFrame, output_dir: Path):
    """Run all 7 chart functions on the given DataFrame."""
    os.makedirs(str(output_dir), exist_ok=True)
    print(f"\n{'='*60}")
    print(f"  Capo Horn Lab — Chart Pipeline")
    print(f"  Output: {output_dir}")
    print(f"  Rows: {len(df):,}")
    print(f"{'='*60}\n")

    for stem_name, chart_fn in CHART_FUNCTIONS:
        try:
            chart_fn(df, output_dir)
        except Exception as e:
            print(f"  \u274c {stem_name}: {e}")

    print(f"\n{'='*60}")
    print(f"  Done — {len(list(output_dir.glob('*.png')))} PNGs, {len(list(output_dir.glob('*.html')))} HTMLs")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Capo Horn Lab — Research Chart Pipeline")
    parser.add_argument("--csv", type=str, help="Path to CSV with trade data")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT), help="Output directory for charts")
    parser.add_argument("--demo", action="store_true", help="Run with synthetic demo data")
    args = parser.parse_args()

    if args.demo:
        print("\n  Generating synthetic demo data...")
        df = generate_demo_data()
    elif args.csv:
        print(f"\n  Loading CSV: {args.csv}")
        df = pd.read_csv(args.csv, parse_dates=["date"] if "date" in pd.read_csv(args.csv, nrows=0).columns else False)
    else:
        # No args — try CSV from stdin or show help
        parser.print_help()
        sys.exit(1)

    output_dir = Path(args.output_dir)
    run_pipeline(df, output_dir)


if __name__ == "__main__":
    main()

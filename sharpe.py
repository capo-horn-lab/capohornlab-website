from typing import List, Optional
from statistics import mean, stdev


def sharpe_ratio(
    daily_returns: List[float],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> Optional[float]:
    """Calculate the annualized Sharpe ratio from a list of daily returns.

    Sharpe ratio measures risk-adjusted return: excess return per unit of
    volatility (standard deviation of returns).

    Formula
    -------
        SR = (mean(R) - r_f) / std(R) * sqrt(N)

    where R are periodic returns, r_f is the periodic risk-free rate, and N
    is the number of periods per year.

    Parameters
    ----------
    daily_returns : List[float]
        Sequence of daily portfolio/strategy returns as decimals
        (e.g. 0.01 for +1%, -0.005 for -0.5%).
    risk_free_rate : float, optional
        Annual risk-free rate (default 0.0). Internally converted to the
        periodic rate: r_f_periodic = (1 + r_f_annual)^(1/N) - 1.
    periods_per_year : int, optional
        Number of trading periods per year (default 252 for daily equity
        markets; use 365 for crypto, 12 for monthly, etc.).

    Returns
    -------
    Optional[float]
        Annualized Sharpe ratio, or None if calculation is impossible
        (fewer than 2 data points, or zero volatility).

    Examples
    --------
    >>> sharpe_ratio([0.01, 0.02, -0.01, 0.005])
    1.279...
    >>> sharpe_ratio([0.001] * 5)
    None
    >>> sharpe_ratio([])
    None
    """
    n = len(daily_returns)
    if n < 2:
        return None

    avg_return = mean(daily_returns)

    # Convert annual risk-free rate to periodic rate
    periodic_rf = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

    excess_returns = avg_return - periodic_rf

    try:
        vol = stdev(daily_returns)
    except Exception:
        return None

    if vol == 0.0:
        return None

    return (excess_returns / vol) * (periods_per_year ** 0.5)

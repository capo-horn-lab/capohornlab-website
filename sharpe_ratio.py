from math import sqrt
from typing import Sequence


def sharpe_ratio(
    daily_returns: Sequence[float],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Calculate the annualised Sharpe ratio of a strategy from daily returns.

    Sharpe ratio = (E[R] - Rf) / sigma, where E[R] is the mean daily return,
    Rf the risk-free rate, and sigma the standard deviation of returns.
    The result is annualised by multiplying by sqrt(periods_per_year).

    Parameters
    ----------
    daily_returns : Sequence[float]
        One or more daily return values (e.g. 0.01 for +1%).
    risk_free_rate : float, optional
        Daily risk-free rate, by default 0.0.  For a 5 % annual
        risk-free rate pass ``0.05 / 252``.
    periods_per_year : int, optional
        Trading days per year for annualisation, by default 252.

    Returns
    -------
    float
        Annualised Sharpe ratio.  Returns 0.0 when there are fewer than
        2 data points or the standard deviation is zero.

    Examples
    --------
    >>> sharpe_ratio([0.01, -0.005, 0.02, 0.0, 0.015])
    12.249...
    """
    n = len(daily_returns)
    if n < 2:
        return 0.0

    mean_return = sum(daily_returns) / n
    variance = sum((r - mean_return) ** 2 for r in daily_returns) / (n - 1)

    if variance == 0.0:
        return 0.0

    excess_return = mean_return - risk_free_rate
    std_dev = sqrt(variance)
    daily_sharpe = excess_return / std_dev

    return daily_sharpe * sqrt(periods_per_year)

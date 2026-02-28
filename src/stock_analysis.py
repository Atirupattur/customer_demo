"""Stock market data analysis utilities.

Provides analysis functions for the stockmarketdata table with columns:
Ticker, DateID, Open, High, Low, Close, Vol, OpenInt.
"""

from __future__ import annotations

from typing import Any


def daily_price_range(high: float, low: float) -> float:
    """Return the difference between the daily high and low price."""
    return high - low


def price_change(open_price: float, close_price: float) -> float:
    """Return the absolute price change from open to close."""
    return close_price - open_price


def price_change_pct(open_price: float, close_price: float) -> float:
    """Return the percentage price change from open to close.

    Args:
        open_price: Opening price of the trading day.
        close_price: Closing price of the trading day.

    Returns:
        Percentage change as a float. Returns 0.0 when open_price is zero.
    """
    if open_price == 0:
        return 0.0
    return (close_price - open_price) / open_price * 100


def moving_average(prices: list[float], window: int) -> list[float]:
    """Compute a simple moving average over a list of prices.

    Args:
        prices: Ordered list of price values.
        window: Number of periods to include in each average.

    Returns:
        List of moving-average values. The first ``window - 1`` entries are
        ``None`` because there is insufficient history.
    """
    if window <= 0:
        raise ValueError("window must be a positive integer")
    result: list[float | None] = [None] * (window - 1)
    for i in range(window - 1, len(prices)):
        avg = sum(prices[i - window + 1 : i + 1]) / window
        result.append(avg)
    return result


def vwap(prices: list[float], volumes: list[int]) -> float:
    """Return the volume-weighted average price (VWAP).

    Args:
        prices: List of trade prices (e.g. closing prices).
        volumes: Corresponding trade volumes.

    Returns:
        VWAP as a float. Returns 0.0 when total volume is zero.

    Raises:
        ValueError: If ``prices`` and ``volumes`` have different lengths.
    """
    if len(prices) != len(volumes):
        raise ValueError("prices and volumes must have the same length")
    total_volume = sum(volumes)
    if total_volume == 0:
        return 0.0
    return sum(p * v for p, v in zip(prices, volumes)) / total_volume


def summarize_ticker(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a summary dict for a single ticker's records.

    Each record must contain the keys ``Open``, ``High``, ``Low``, ``Close``,
    and ``Vol``.

    Args:
        records: List of daily OHLCV records for one ticker.

    Returns:
        Dictionary with keys ``open_first``, ``close_last``, ``high_max``,
        ``low_min``, ``vol_total``, and ``price_change_pct``.

    Raises:
        ValueError: If ``records`` is empty.
    """
    if not records:
        raise ValueError("records must not be empty")
    open_first = records[0]["Open"]
    close_last = records[-1]["Close"]
    high_max = max(r["High"] for r in records)
    low_min = min(r["Low"] for r in records)
    vol_total = sum(r["Vol"] for r in records)
    return {
        "open_first": open_first,
        "close_last": close_last,
        "high_max": high_max,
        "low_min": low_min,
        "vol_total": vol_total,
        "price_change_pct": price_change_pct(open_first, close_last),
    }

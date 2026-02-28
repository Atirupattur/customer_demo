"""Tests for stock_analysis utilities."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from stock_analysis import (
    daily_price_range,
    moving_average,
    price_change,
    price_change_pct,
    summarize_ticker,
    vwap,
)


def test_daily_price_range():
    assert daily_price_range(110.0, 100.0) == pytest.approx(10.0)


def test_price_change():
    assert price_change(100.0, 115.0) == pytest.approx(15.0)
    assert price_change(100.0, 90.0) == pytest.approx(-10.0)


def test_price_change_pct_basic():
    assert price_change_pct(100.0, 110.0) == pytest.approx(10.0)


def test_price_change_pct_zero_open():
    assert price_change_pct(0.0, 50.0) == 0.0


def test_moving_average_basic():
    prices = [1.0, 2.0, 3.0, 4.0, 5.0]
    window = 3
    result = moving_average(prices, window)
    assert result[: window - 1] == [None] * (window - 1)
    assert result[2] == pytest.approx(2.0)
    assert result[3] == pytest.approx(3.0)
    assert result[4] == pytest.approx(4.0)


def test_moving_average_window_one():
    prices = [10.0, 20.0, 30.0]
    assert moving_average(prices, 1) == pytest.approx([10.0, 20.0, 30.0])


def test_moving_average_invalid_window():
    with pytest.raises(ValueError):
        moving_average([1.0, 2.0], 0)


def test_vwap_basic():
    prices = [10.0, 20.0, 30.0]
    volumes = [1, 2, 3]
    # (10*1 + 20*2 + 30*3) / 6 = 140/6
    assert vwap(prices, volumes) == pytest.approx(140 / 6)


def test_vwap_zero_volume():
    assert vwap([10.0, 20.0], [0, 0]) == 0.0


def test_vwap_length_mismatch():
    with pytest.raises(ValueError):
        vwap([1.0, 2.0], [1])


def test_summarize_ticker():
    records = [
        {"Open": 100.0, "High": 115.0, "Low": 95.0, "Close": 110.0, "Vol": 1000},
        {"Open": 110.0, "High": 120.0, "Low": 105.0, "Close": 118.0, "Vol": 2000},
    ]
    summary = summarize_ticker(records)
    assert summary["open_first"] == 100.0
    assert summary["close_last"] == 118.0
    assert summary["high_max"] == 120.0
    assert summary["low_min"] == 95.0
    assert summary["vol_total"] == 3000
    assert summary["price_change_pct"] == pytest.approx(18.0)


def test_summarize_ticker_empty():
    with pytest.raises(ValueError):
        summarize_ticker([])

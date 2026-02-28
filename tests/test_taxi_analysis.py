"""Tests for taxi_analysis utilities."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from taxi_analysis import (
    average_speed_mph,
    fare_breakdown,
    group_trips_by_payment,
    summarize_trips,
    tip_percentage,
)


def test_fare_breakdown():
    result = fare_breakdown(10.0, 0.5, 0.3, 2.0, 0.0)
    assert result["total"] == pytest.approx(12.8)
    assert result["fare"] == 10.0
    assert result["tip"] == 2.0


def test_average_speed_mph_basic():
    # 30 miles in 3600 seconds = 30 mph
    assert average_speed_mph(30.0, 3600) == pytest.approx(30.0)


def test_average_speed_mph_zero_duration():
    assert average_speed_mph(10.0, 0) == 0.0


def test_tip_percentage_basic():
    assert tip_percentage(2.0, 10.0) == pytest.approx(20.0)


def test_tip_percentage_zero_fare():
    assert tip_percentage(1.0, 0.0) == 0.0


def test_summarize_trips():
    trips = [
        {
            "TripDistanceMiles": 5.0,
            "TripDurationSeconds": 600,
            "FareAmount": 10.0,
            "TipAmount": 2.0,
            "PassengerCount": 1,
            "PaymentType": "Cash",
        },
        {
            "TripDistanceMiles": 10.0,
            "TripDurationSeconds": 1200,
            "FareAmount": 20.0,
            "TipAmount": 4.0,
            "PassengerCount": 2,
            "PaymentType": "Card",
        },
    ]
    summary = summarize_trips(trips)
    assert summary["trip_count"] == 2
    assert summary["total_distance_miles"] == pytest.approx(15.0)
    assert summary["avg_distance_miles"] == pytest.approx(7.5)
    assert summary["avg_fare"] == pytest.approx(15.0)
    assert summary["total_passengers"] == 3
    assert summary["avg_tip_pct"] == pytest.approx(20.0)


def test_summarize_trips_empty():
    with pytest.raises(ValueError):
        summarize_trips([])


def test_group_trips_by_payment():
    trips = [
        {"PaymentType": "Cash", "FareAmount": 10.0},
        {"PaymentType": "Card", "FareAmount": 12.0},
        {"PaymentType": "Cash", "FareAmount": 8.0},
    ]
    groups = group_trips_by_payment(trips)
    assert len(groups["Cash"]) == 2
    assert len(groups["Card"]) == 1


def test_group_trips_by_payment_missing_key():
    trips = [{"FareAmount": 5.0}]
    groups = group_trips_by_payment(trips)
    assert "Unknown" in groups

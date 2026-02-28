"""Taxi data analysis utilities.

Provides analysis functions for the taxi data warehouse tables:
Trip, Date, Geography, HackneyLicense, Medallion, Time, Weather.
"""

from __future__ import annotations

from typing import Any


def fare_breakdown(
    fare: float,
    surcharge: float,
    tax: float,
    tip: float,
    tolls: float,
) -> dict[str, float]:
    """Return a breakdown of all fare components and the computed total.

    Args:
        fare: Base fare amount.
        surcharge: Surcharge amount.
        tax: Tax amount.
        tip: Tip amount.
        tolls: Tolls amount.

    Returns:
        Dictionary with each component and a ``total`` key.
    """
    total = fare + surcharge + tax + tip + tolls
    return {
        "fare": fare,
        "surcharge": surcharge,
        "tax": tax,
        "tip": tip,
        "tolls": tolls,
        "total": total,
    }


def average_speed_mph(distance_miles: float, duration_seconds: int) -> float:
    """Return the average speed in miles per hour for a trip.

    Args:
        distance_miles: Trip distance in miles.
        duration_seconds: Trip duration in seconds.

    Returns:
        Average speed in mph. Returns 0.0 when duration is zero.
    """
    if duration_seconds <= 0:
        return 0.0
    return distance_miles / (duration_seconds / 3600)


def tip_percentage(tip: float, fare: float) -> float:
    """Return the tip as a percentage of the base fare.

    Args:
        tip: Tip amount.
        fare: Base fare amount.

    Returns:
        Tip percentage as a float. Returns 0.0 when fare is zero.
    """
    if fare == 0:
        return 0.0
    return tip / fare * 100


def summarize_trips(trips: list[dict[str, Any]]) -> dict[str, Any]:
    """Return aggregate statistics for a collection of trip records.

    Each record must contain the keys ``TripDistanceMiles``,
    ``TripDurationSeconds``, ``FareAmount``, ``TipAmount``, and
    ``PassengerCount``.

    Args:
        trips: List of trip records.

    Returns:
        Dictionary with keys ``trip_count``, ``total_distance_miles``,
        ``avg_distance_miles``, ``avg_duration_seconds``, ``avg_fare``,
        ``avg_tip_pct``, and ``total_passengers``.

    Raises:
        ValueError: If ``trips`` is empty.
    """
    if not trips:
        raise ValueError("trips must not be empty")
    trip_count = len(trips)
    total_distance = sum(t["TripDistanceMiles"] for t in trips)
    avg_duration = sum(t["TripDurationSeconds"] for t in trips) / trip_count
    avg_fare = sum(t["FareAmount"] for t in trips) / trip_count
    avg_tip_pct = (
        sum(tip_percentage(t["TipAmount"], t["FareAmount"]) for t in trips)
        / trip_count
    )
    total_passengers = sum(t["PassengerCount"] for t in trips)
    return {
        "trip_count": trip_count,
        "total_distance_miles": total_distance,
        "avg_distance_miles": total_distance / trip_count,
        "avg_duration_seconds": avg_duration,
        "avg_fare": avg_fare,
        "avg_tip_pct": avg_tip_pct,
        "total_passengers": total_passengers,
    }


def group_trips_by_payment(
    trips: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group trip records by their payment type.

    Args:
        trips: List of trip records, each containing a ``PaymentType`` key.

    Returns:
        Dictionary mapping each payment type string to its list of trips.
    """
    groups: dict[str, list[dict[str, Any]]] = {}
    for trip in trips:
        payment_type = trip.get("PaymentType", "Unknown")
        groups.setdefault(payment_type, []).append(trip)
    return groups

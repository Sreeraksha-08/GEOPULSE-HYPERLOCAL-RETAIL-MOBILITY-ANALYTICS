"""Automated quality tests for GeoPulse movement data."""

from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parent.parent
PARQUET_PATH = ROOT / "sample_data" / "device_movement_day5.parquet"

EXPECTED_ROWS = 336_000
EXPECTED_DEVICES = 1_000

EXPECTED_COLUMNS = [
    "timestamp",
    "device_id",
    "zone_id",
    "zone_type",
    "activity",
    "latitude",
    "longitude",
]

EXPECTED_ACTIVITIES = {
    "at_home",
    "morning_commute",
    "working",
    "lunch_visit",
    "evening_visit",
    "return_home",
    "weekend_visit",
}


@pytest.fixture(scope="module")
def movement_data():
    assert PARQUET_PATH.exists(), "Parquet dataset does not exist."
    return pd.read_parquet(PARQUET_PATH)


def test_correct_columns(movement_data):
    assert list(movement_data.columns) == EXPECTED_COLUMNS


def test_correct_number_of_records(movement_data):
    assert len(movement_data) == EXPECTED_ROWS


def test_unique_device_count(movement_data):
    assert movement_data["device_id"].nunique() == EXPECTED_DEVICES


def test_no_missing_values(movement_data):
    assert movement_data.isna().sum().sum() == 0


def test_no_duplicate_records(movement_data):
    assert not movement_data.duplicated().any()


def test_valid_activity_categories(movement_data):
    assert set(movement_data["activity"].unique()) == EXPECTED_ACTIVITIES


def test_valid_zone_types(movement_data):
    assert set(movement_data["zone_type"].unique()) == {
        "residential",
        "office",
        "retail",
    }


def test_valid_coordinates(movement_data):
    assert movement_data["latitude"].between(-90, 90).all()
    assert movement_data["longitude"].between(-180, 180).all()


def test_valid_timestamps(movement_data):
    assert pd.api.types.is_datetime64_any_dtype(
        movement_data["timestamp"]
    )
    assert movement_data["timestamp"].notna().all()
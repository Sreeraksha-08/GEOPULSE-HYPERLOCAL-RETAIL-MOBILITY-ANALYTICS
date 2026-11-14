"""Convert GeoPulse Day 4 movement data from CSV to Parquet."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = ROOT / "sample_data" / "device_movement_day4.csv"
PARQUET_PATH = ROOT / "sample_data" / "device_movement_day5.parquet"

EXPECTED_ROWS = 336_000
EXPECTED_DEVICES = 1_000

REQUIRED_COLUMNS = [
    "timestamp",
    "device_id",
    "zone_id",
    "zone_type",
    "activity",
    "latitude",
    "longitude",
]


def convert_to_parquet():
    print("Reading Day 4 CSV dataset...")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])

    # Validate the original dataset.
    assert len(df) == EXPECTED_ROWS, "Unexpected row count."
    assert df["device_id"].nunique() == EXPECTED_DEVICES
    assert df.isna().sum().sum() == 0
    assert not df.duplicated().any()
    assert list(df.columns) == REQUIRED_COLUMNS

    print(f"CSV records verified: {len(df):,}")

    # Convert to Parquet using PyArrow.
    df.to_parquet(
        PARQUET_PATH,
        engine="pyarrow",
        index=False,
        compression="snappy",
    )

    print("\nParquet file created.")

    # Read the Parquet file back and verify it.
    parquet_df = pd.read_parquet(
        PARQUET_PATH,
        engine="pyarrow",
    )

    assert len(parquet_df) == EXPECTED_ROWS
    assert parquet_df["device_id"].nunique() == EXPECTED_DEVICES
    assert parquet_df.isna().sum().sum() == 0
    assert not parquet_df.duplicated().any()
    assert list(parquet_df.columns) == REQUIRED_COLUMNS

    # Verify the data is identical after conversion.
    pd.testing.assert_frame_equal(
        df.reset_index(drop=True),
        parquet_df.reset_index(drop=True),
        check_dtype=True,
    )

    csv_size = CSV_PATH.stat().st_size
    parquet_size = PARQUET_PATH.stat().st_size

    print("\nDAY 5 PARQUET VALIDATION PASSED")
    print(f"Rows: {len(parquet_df):,}")
    print(f"Unique devices: {parquet_df['device_id'].nunique():,}")
    print(f"Missing values: {parquet_df.isna().sum().sum()}")
    print(f"Duplicate rows: {parquet_df.duplicated().sum()}")
    print(f"CSV size: {csv_size / 1024:.2f} KB")
    print(f"Parquet size: {parquet_size / 1024:.2f} KB")
    print(f"Parquet output: {PARQUET_PATH}")


if __name__ == "__main__":
    convert_to_parquet()
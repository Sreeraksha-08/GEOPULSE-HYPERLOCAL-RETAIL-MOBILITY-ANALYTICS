"""Fast, reproducible synthetic device movement simulator for GeoPulse."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
GEOJSON_PATH = ROOT / "sample_data" / "bengaluru_zones.geojson"
OUTPUT_PATH = ROOT / "sample_data" / "device_movement_day4.csv"

SEED = 42
DEVICE_COUNT = 1_000
DAYS = 7
INTERVAL_MINUTES = 30
START_DATE = "2026-11-02 00:00:00"
GPS_NOISE_METRES = 80

rng = np.random.default_rng(SEED)


def load_zones():
    with GEOJSON_PATH.open("r", encoding="utf-8") as file:
        geojson = json.load(file)

    zones = []

    for feature in geojson["features"]:
        props = feature["properties"]
        coordinates = feature["geometry"]["coordinates"][0]

        zones.append({
            "zone_id": props["zone_id"],
            "zone_type": props["zone_type"],
            "latitude": np.mean([p[1] for p in coordinates[:-1]]),
            "longitude": np.mean([p[0] for p in coordinates[:-1]]),
        })

    return pd.DataFrame(zones)


def generate_movement():
    zones = load_zones()

    required_types = {"residential", "office", "retail"}
    if not required_types.issubset(set(zones["zone_type"])):
        raise ValueError("City geography is missing a required zone type.")

    zone_ids = zones["zone_id"].to_numpy()
    zone_types = zones["zone_type"].to_numpy()
    latitudes = zones["latitude"].to_numpy(dtype=float)
    longitudes = zones["longitude"].to_numpy(dtype=float)

    residential = np.flatnonzero(zone_types == "residential")
    offices = np.flatnonzero(zone_types == "office")
    retail = np.flatnonzero(zone_types == "retail")

    timestamps = pd.date_range(
        start=START_DATE,
        periods=DAYS * 24 * 60 // INTERVAL_MINUTES,
        freq=f"{INTERVAL_MINUTES}min",
    )

    device_numbers = np.arange(1, DEVICE_COUNT + 1)
    device_ids = np.array([
        hashlib.sha256(
            f"geopulse-demo-device-{n:06d}".encode()
        ).hexdigest()[:16]
        for n in device_numbers
    ])

    # Assign each device a regular home and work zone.
    home_zones = rng.choice(residential, size=DEVICE_COUNT)
    work_zones = rng.choice(offices, size=DEVICE_COUNT)

    hours = timestamps.hour.to_numpy()
    weekdays = timestamps.day_of_week.to_numpy()
    weekends = weekdays >= 5

    activity = np.full(len(timestamps), "at_home", dtype=object)
    target_types = np.full(len(timestamps), "residential", dtype=object)

    morning = (hours >= 7) & (hours < 9)
    working = ((hours >= 9) & (hours < 12)) | (
        (hours >= 14) & (hours < 17)
    )
    lunch = (hours >= 12) & (hours < 14)
    evening = (hours >= 17) & (hours < 19)
    returning = (hours >= 19) & (hours < 21)
    weekend_visit = weekends & (hours >= 10) & (hours < 17)

    target_types[morning | working] = "office"
    target_types[lunch | evening | weekend_visit] = "retail"

    activity[morning] = "morning_commute"
    activity[working] = "working"
    activity[lunch] = "lunch_visit"
    activity[evening] = "evening_visit"
    activity[returning] = "return_home"
    activity[weekend_visit] = "weekend_visit"

    # Create one zone index for every device and timestamp.
    zone_indices = np.broadcast_to(
        home_zones[:, None],
        (DEVICE_COUNT, len(timestamps))
    ).copy()

    office_mask = target_types == "office"
    zone_indices[:, office_mask] = work_zones[:, None]

    retail_mask = target_types == "retail"
    retail_choices = rng.choice(
        retail, size=(DEVICE_COUNT, retail_mask.sum())
    )
    zone_indices[:, retail_mask] = retail_choices

    # Retrieve coordinates for all generated pings.
    base_latitudes = latitudes[zone_indices]
    base_longitudes = longitudes[zone_indices]

    longitude_scale = 111_320 * np.cos(np.radians(base_latitudes))

    latitude_noise = rng.normal(
        0, GPS_NOISE_METRES / 111_320,
        size=base_latitudes.shape
    )
    longitude_noise = rng.normal(
        0, GPS_NOISE_METRES / longitude_scale,
        size=base_longitudes.shape
    )

    total_records = DEVICE_COUNT * len(timestamps)

    movement = pd.DataFrame({
        "timestamp": np.tile(timestamps.to_numpy(), DEVICE_COUNT),
        "device_id": np.repeat(device_ids, len(timestamps)),
        "zone_id": zone_ids[zone_indices].ravel(),
        "zone_type": zone_types[zone_indices].ravel(),
        "activity": np.tile(activity, DEVICE_COUNT),
        "latitude": (base_latitudes + latitude_noise).ravel(),
        "longitude": (base_longitudes + longitude_noise).ravel(),
    })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    movement.to_csv(OUTPUT_PATH, index=False)

    print("GeoPulse Day 4 movement simulation completed.")
    print(f"Devices: {DEVICE_COUNT:,}")
    print(f"Days: {DAYS}")
    print(f"Records: {len(movement):,}")
    print(f"Expected records: {total_records:,}")
    print(f"Unique devices: {movement['device_id'].nunique():,}")
    print(f"Output: {OUTPUT_PATH}")
    print("\nActivity summary:")
    print(movement["activity"].value_counts().to_string())


if __name__ == "__main__":
    generate_movement()
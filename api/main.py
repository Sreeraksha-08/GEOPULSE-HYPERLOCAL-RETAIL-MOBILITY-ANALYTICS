from pathlib import Path
from functools import lru_cache
import csv

from fastapi import FastAPI, HTTPException, Query

ROOT = Path(__file__).resolve().parent.parent
MOVEMENT_FILE = ROOT / "sample_data" / "device_movement_day4.csv"
STORE_FILE = ROOT / "sample_data" / "bengaluru_stores.csv"

VALID_STORE_TYPES = {"existing", "candidate"}
VALID_ACTIVITIES = {
    "at_home",
    "working",
    "morning_commute",
    "lunch_visit",
    "evening_visit",
    "return_home",
    "weekend_visit",
}

app = FastAPI(
    title="GeoPulse API",
    description="Hyperlocal Retail Mobility Analytics API using simulated data",
    version="1.1.0",
)


@lru_cache(maxsize=1)
def load_movement():
    with MOVEMENT_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=1)
def load_stores():
    with STORE_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@app.get("/")
def root():
    return {
        "project": "GeoPulse",
        "message": "Hyperlocal Retail Mobility Analytics API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "project": "GeoPulse"}


@app.get("/stores")
def stores(
    store_type: str | None = Query(default=None)
):
    data = load_stores()

    if store_type is not None:
        normalized_type = store_type.lower()

        if normalized_type not in VALID_STORE_TYPES:
            raise HTTPException(
                status_code=422,
                detail="store_type must be 'existing' or 'candidate'",
            )

        data = [
            store for store in data
            if store["store_type"].lower() == normalized_type
        ]

    return {"count": len(data), "stores": data}


@app.get("/zones")
def zones():
    data = load_movement()
    summaries = {}

    for row in data:
        zone = row["zone_id"]

        if zone not in summaries:
            summaries[zone] = {
                "zone_id": zone,
                "zone_type": row["zone_type"],
                "records": 0,
                "unique_devices": set(),
                "activities": {},
            }

        summaries[zone]["records"] += 1
        summaries[zone]["unique_devices"].add(row["device_id"])

        activity = row["activity"]
        summaries[zone]["activities"][activity] = (
            summaries[zone]["activities"].get(activity, 0) + 1
        )

    result = []

    for item in summaries.values():
        item["unique_devices"] = len(item["unique_devices"])
        result.append(item)

    return {"count": len(result), "zones": result}


@app.get("/footfall")
def footfall(
    zone_id: str | None = Query(default=None),
    activity: str | None = Query(default=None),
):
    data = load_movement()

    if activity is not None:
        normalized_activity = activity.lower()

        if normalized_activity not in VALID_ACTIVITIES:
            raise HTTPException(
                status_code=422,
                detail="Invalid activity type",
            )

        activity = normalized_activity

    if zone_id:
        data = [row for row in data if row["zone_id"] == zone_id]

    if activity:
        data = [row for row in data if row["activity"] == activity]

    if not data:
        raise HTTPException(status_code=404, detail="No matching movement data")

    devices = set()
    activity_counts = {}
    zone_counts = {}

    for row in data:
        devices.add(row["device_id"])

        activity_counts[row["activity"]] = (
            activity_counts.get(row["activity"], 0) + 1
        )

        zone_counts[row["zone_id"]] = (
            zone_counts.get(row["zone_id"], 0) + 1
        )

    return {
        "records": len(data),
        "unique_devices": len(devices),
        "activity_counts": activity_counts,
        "zone_counts": zone_counts,
        "filters": {"zone_id": zone_id, "activity": activity},
    }

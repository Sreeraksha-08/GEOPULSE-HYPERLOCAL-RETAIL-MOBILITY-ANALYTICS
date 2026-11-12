import csv
import json
from pathlib import Path

def test_bengaluru_geojson_has_25_zones():
    path = Path("sample_data/bengaluru_zones.geojson")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 25

def test_zone_polygons_are_valid():
    data = json.loads(
        Path("sample_data/bengaluru_zones.geojson").read_text(encoding="utf-8")
    )
    for feature in data["features"]:
        assert feature["geometry"]["type"] == "Polygon"
        ring = feature["geometry"]["coordinates"][0]
        assert len(ring) == 5
        assert ring[0] == ring[-1]

def test_zone_categories():
    data = json.loads(
        Path("sample_data/bengaluru_zones.geojson").read_text(encoding="utf-8")
    )
    counts = {}
    for feature in data["features"]:
        kind = feature["properties"]["zone_type"]
        counts[kind] = counts.get(kind, 0) + 1
    assert counts == {"residential": 9, "office": 9, "retail": 7}

def test_store_counts_and_ids():
    with open("sample_data/bengaluru_stores.csv", newline="", encoding="utf-8") as f:
        stores = list(csv.DictReader(f))
    assert len(stores) == 16
    assert len({s["store_id"] for s in stores}) == 16
    assert sum(s["store_type"] == "existing" for s in stores) == 12
    assert sum(s["store_type"] == "candidate" for s in stores) == 4

def test_store_coordinates_and_zone_references():
    data = json.loads(
        Path("sample_data/bengaluru_zones.geojson").read_text(encoding="utf-8")
    )
    zone_ids = {f["properties"]["zone_id"] for f in data["features"]}
    with open("sample_data/bengaluru_stores.csv", newline="", encoding="utf-8") as f:
        stores = list(csv.DictReader(f))
    for store in stores:
        assert store["zone_id"] in zone_ids
        assert -5000 <= float(store["x_m"]) <= 5000
        assert -5000 <= float(store["y_m"]) <= 5000
        assert -180 <= float(store["longitude"]) <= 180
        assert -90 <= float(store["latitude"]) <= 90

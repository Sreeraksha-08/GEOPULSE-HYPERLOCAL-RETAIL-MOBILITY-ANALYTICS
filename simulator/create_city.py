import csv
import json
import math
import random
from pathlib import Path

# Bengaluru study area: approximate central reference point.
CENTER_LAT = 12.9716
CENTER_LON = 77.5946
CITY_SIZE_M = 10_000
GRID_SIZE = 5
ZONE_SIZE_M = CITY_SIZE_M / GRID_SIZE

OUTPUT_DIR = Path("sample_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

# Convert local simulated metre coordinates into approximate
# longitude/latitude coordinates around Bengaluru.
def to_lat_lon(x_m, y_m):
    latitude = CENTER_LAT + y_m / 111_320
    longitude = CENTER_LON + x_m / (
        111_320 * math.cos(math.radians(CENTER_LAT))
    )
    return round(longitude, 7), round(latitude, 7)


def zone_type(row, col):
    pattern = [
        ["residential", "residential", "office", "office", "retail"],
        ["residential", "office", "office", "retail", "retail"],
        ["residential", "residential", "retail", "retail", "office"],
        ["office", "office", "residential", "residential", "retail"],
        ["retail", "residential", "residential", "office", "office"],
    ]
    return pattern[row][col]


features = []

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        zone_id = f"BENG-Z{row * GRID_SIZE + col + 1:02d}"

        min_x = -CITY_SIZE_M / 2 + col * ZONE_SIZE_M
        max_x = min_x + ZONE_SIZE_M
        min_y = -CITY_SIZE_M / 2 + row * ZONE_SIZE_M
        max_y = min_y + ZONE_SIZE_M

        coordinates = [
            to_lat_lon(min_x, min_y),
            to_lat_lon(max_x, min_y),
            to_lat_lon(max_x, max_y),
            to_lat_lon(min_x, max_y),
            to_lat_lon(min_x, min_y),
        ]

        features.append({
            "type": "Feature",
            "properties": {
                "zone_id": zone_id,
                "zone_type": zone_type(row, col),
                "area_sq_km": 4.0,
                "grid_row": row + 1,
                "grid_column": col + 1,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates],
            },
        })

geojson = {
    "type": "FeatureCollection",
    "name": "GeoPulse_Bengaluru_Zones",
    "features": features,
}

with open(OUTPUT_DIR / "bengaluru_zones.geojson", "w") as file:
    json.dump(geojson, file, indent=2)

# Create 12 existing stores and 4 candidate locations.
stores = []
store_positions = [
    (-4200, -3500), (-2200, -3500), (0, -3500),
    (2200, -3500), (4200, -1500), (-4200, -1000),
    (-2000, 500), (1000, 1000), (3500, 1500),
    (-3500, 3500), (0, 3500), (3000, 4000),
    (-3000, -2000), (-500, -500), (2000, 2500),
    (4000, 3500),
]

for index, (x, y) in enumerate(store_positions):
    col = min(GRID_SIZE - 1, int((x + CITY_SIZE_M / 2) // ZONE_SIZE_M))
    row = min(GRID_SIZE - 1, int((y + CITY_SIZE_M / 2) // ZONE_SIZE_M))
    zone_id = f"BENG-Z{row * GRID_SIZE + col + 1:02d}"
    lon, lat = to_lat_lon(x, y)

    if index < 12:
        store_id = f"STORE-{index + 1:02d}"
        store_type = "existing"
    else:
        store_id = f"CANDIDATE-{index - 11:02d}"
        store_type = "candidate"

    stores.append({
        "store_id": store_id,
        "store_type": store_type,
        "zone_id": zone_id,
        "x_m": x,
        "y_m": y,
        "longitude": lon,
        "latitude": lat,
    })

with open(OUTPUT_DIR / "bengaluru_stores.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=stores[0].keys())
    writer.writeheader()
    writer.writerows(stores)

# Print generation summary.
print("===== GEOPULSE BENGALURU GEOGRAPHY =====")
print("Study area: 10 km x 10 km")
print("Grid: 5 x 5")
print("Total zones:", len(features))
print("Zone types:")

for kind in ["residential", "office", "retail"]:
    count = sum(
        f["properties"]["zone_type"] == kind for f in features
    )
    print(f"  {kind}: {count}")

print("Existing stores:", sum(s["store_type"] == "existing" for s in stores))
print("Candidate stores:", sum(s["store_type"] == "candidate" for s in stores))
print("GeoJSON:", OUTPUT_DIR / "bengaluru_zones.geojson")
print("CSV:", OUTPUT_DIR / "bengaluru_stores.csv")
print("Geography generation successful!")

# Day 11: Store Catchment Analysis

## Objective
Analyse synthetic movement data within 500-metre catchments around 12 existing stores and 4 candidate store locations using Apache Spark and Apache Sedona.

## Input Data
- Movement records: 336,000
- Synthetic devices: 1,000
- Existing stores: 12
- Candidate stores: 4
- Catchment radius: 500 metres

## Processing Steps
1. Loaded movement records using PySpark.
2. Created spatial point geometries from longitude and latitude.
3. Loaded 16 existing and candidate store locations.
4. Calculated distances between movement points and store locations using Sedona's ST_DistanceSphere.
5. Identified movement points within 500 metres of each store.
6. Generated store-level summaries.
7. Compared existing and candidate store catchment results.

## Results

| Metric | Result |
|---|---:|
| Movement records | 336,000 |
| Valid point geometries | 336,000 |
| Store locations | 16 |
| Existing stores | 12 |
| Candidate stores | 4 |
| Catchment matches | 54,458 |

### Existing vs Candidate Comparison

| Store Type | Movement Points |
|---|---:|
| Existing | 41,267 |
| Candidate | 13,191 |
| Total | 54,458 |

## Key Observations
- Candidate 03 recorded 8,429 movement points.
- Candidate 04 recorded 4,710 movement points.
- Four stores had no matching movement points within their 500-metre catchments.
- Device counts are calculated separately for each store. Summing them across stores may count the same device more than once.

## Validation
- All 336,000 movement records loaded successfully.
- All 336,000 records produced valid point geometries.
- All 16 store locations were loaded.
- The expected 12 existing and 4 candidate stores were verified.
- The spatial catchment analysis completed successfully.

## Technologies Used
- Python
- PySpark
- Apache Spark
- Apache Sedona
- Shapely
- CSV

## Final Status
GEOPULSE DAY 11 STORE CATCHMENT ANALYSIS PASSED

All movement data and locations used in this analysis are synthetic.
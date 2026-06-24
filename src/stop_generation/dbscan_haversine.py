"""
FILE:
dbscan_haversine.py

PURPOSE:
Generate school bus pickup stops using DBSCAN clustering
based on straight-line (Haversine) distance.

WORKFLOW:
1. Read student latitude and longitude coordinates
2. Convert coordinates from degrees to radians
3. Apply DBSCAN clustering using Haversine distance
4. Identify pickup clusters and isolated students
5. Create stop assignments for all students
6. Generate stop locations from cluster centroids

INPUT:
students_df

REQUIRED COLUMNS:
- student_id
- latitude
- longitude
- demand

OUTPUT:
stops_df
- stop_id
- latitude
- longitude

stop_assignments_df
- student_id
- stop_id

NOTES:
- Uses Haversine (straight-line) distance
- Does not require the number of stops to be
  specified beforehand
- Automatically determines cluster count
- Noise points become individual pickup stops
- Better suited than K-Means when student
  distribution is irregular

ADVANTAGES:
- Automatically discovers clusters
- Handles outliers naturally
- Adapts to varying student densities

LIMITATIONS:
- Ignores road network constraints
- May cluster students separated by walls,
  gated communities, dead-end streets, or
  disconnected road networks
- Walking distance may be significantly larger
  than straight-line distance

PROJECT:
School Transportation Planning Platform
Version 1 (Stop Generation Engine)
"""

import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN

def generate_stops_dbscan_haversine(
        students_df
):    
    coordinates = students_df[
        ["latitude","longitude"]
    ].values

    coordinates_rad = np.radians(
        coordinates
    )

    dbscan = DBSCAN(
        eps=0.3/6371,
        min_samples=2,
        metric="haversine"
    )
    labels = dbscan.fit_predict(
        coordinates_rad
    )
    stop_assignments_df = students_df[
        ["student_id"]
    ].copy()
    stop_ids = []
    next_noise_stop = max(labels)+1
    for label in labels:
        if label == -1:
            stop_ids.append(
                f"STOP_{next_noise_stop}"
            )
            next_noise_stop += 1
        else:
            stop_ids.append(
                f"STOP_{label}"
            )
    stop_assignments_df["stop_id"] = stop_ids
    students_with_stops = students_df.merge(
        stop_assignments_df,
        on="student_id"
    )
    stops_df = (
        students_with_stops.groupby("stop_id")
        .agg(
            latitude = ("latitude","mean"),
            longitude = ("longitude","mean")
        ).reset_index()
    )

    stops_df = stops_df[
        ["stop_id","latitude","longitude"]
    ]

    noise_students = sum(labels == -1)
    unique_labels = np.unique(labels)
    number_of_clusters = (
        len(unique_labels) - (-1 in unique_labels)
    )
    print()
    print("----------------------")
    print("Cluster Summary")
    print(
        f"Cluster: {number_of_clusters}"
    )
    print(
        f"Noise Students: {noise_students}"
    )
    print("----------------------")
    print()

    return stops_df, stop_assignments_df
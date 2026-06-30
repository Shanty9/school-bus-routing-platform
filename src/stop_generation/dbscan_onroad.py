"""
FILE:
dbscan_onroad.py

PURPOSE:
Generate school bus pickup stops using DBSCAN clustering
based on actual road-network distances.

WORKFLOW:
1. Read student latitude and longitude coordinates
2. Generate an NxN road distance matrix using OSRM
3. Apply DBSCAN clustering using precomputed distances
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

DEPENDENCIES:
- Local OSRM Server
- distance_matrix.py

NOTES:
- Uses actual road-network distances rather than
  straight-line distances
- Distances are measured in metres
- Does not require the number of stops to be
  specified beforehand
- Automatically determines cluster count
- Noise points become individual pickup stops
- Designed to generate operationally realistic
  pickup clusters

ADVANTAGES:
- Accounts for road network geometry
- Avoids unrealistic clustering across walls,
  gated communities, lakes, dead-end streets,
  and disconnected road networks
- Produces pickup locations that more closely
  match real-world walking behaviour
- Better representation of actual student access
  to pickup points

LIMITATIONS:
- Requires OSRM preprocessing and server setup
- Computationally slower than Haversine methods
- Quality depends on OpenStreetMap road data
- Large datasets may require batching of
  distance matrix requests

RESEARCH OBJECTIVE:
Compare the effectiveness of road-network-based
clustering against traditional straight-line
(Haversine) clustering for school transportation
planning.

PROJECT:
School Transportation Planning Platform
Version 1 (Stop Generation Engine)
"""

from traveltime_engine.distance_matrix import generate_distance_matrix
from sklearn.cluster import DBSCAN

def generate_stops_dbscan_onroad (
        students_df
):
    
    distance_matrix = generate_distance_matrix(
        students_df
    )
    dbscan = DBSCAN(
        eps = 400,
        min_samples=2,
        metric="precomputed"
    )
    labels = dbscan.fit_predict(
        distance_matrix
    )
    import pandas as pd
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
        students_with_stops
        .groupby("stop_id").agg(
            latitude = ("latitude","mean"),
            longitude = ("longitude","mean")
        )
        .reset_index()
    )
    stops_df = stops_df[
        ["stop_id","latitude","longitude"]
        ]

    import numpy as np
    unique_labels = np.unique(labels)
    noise_labels = sum(labels == -1)
    number_of_clusters = (
        len(unique_labels)
        - (-1 in unique_labels)
    )
    #for label in unique_labels:
     #   count = sum(labels==label)
      #  print(f"Cluster {label}: {count} Students")
    print("--------------------------")
    print("CLUSTER SUMMARY")
    print(f"Number of Clusters: {number_of_clusters}")
    print(f"Noise Clusters: {noise_labels}")
    print("--------------------------")

    return stops_df, stop_assignments_df
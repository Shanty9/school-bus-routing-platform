"""
FILE:
kmeans_haversine.py

PURPOSE:
Generate school bus pickup stops using K-Means clustering
based on straight-line (Haversine) distance.

WORKFLOW:
1. Read student latitude and longitude coordinates
2. Group students into a predefined number of clusters
3. Calculate cluster centroids
4. Create one pickup stop at each centroid
5. Assign every student to a stop

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
- Number of stops must be specified beforehand
- Every student is assigned to a cluster
- No concept of noise or outliers
- Uses straight-line geographic distance
- Serves as a baseline clustering approach for
  comparison against DBSCAN-based methods

LIMITATIONS:
- May place stop locations in unrealistic positions
- Does not consider road network constraints
- Requires predefined cluster count
- Forces all students into clusters

PROJECT:
School Transportation Planning Platform
Version 1 (Stop Generation Engine)
"""


import pandas as pd
import math

target_students_per_stop = 2


from sklearn.cluster import KMeans

def generate_stops_kmeans(students_df):
    
    coordinates_df = students_df[["latitude","longitude"]]
    coordinates = coordinates_df.values
    k=math.ceil(
        len(students_df)/target_students_per_stop
    )
    print(f"K = {k}")
    
    kmeans=KMeans(n_clusters=k , random_state=42)
    kmeans.fit(coordinates)
    labels=kmeans.labels_
     
    stop_assignments_df = students_df[["student_id"]].copy()
    stop_assignments_df["stop_id"] = labels
    stop_assignments_df["stop_id"] = (stop_assignments_df["stop_id"]+1)
    stop_assignments_df["stop_id"] = (
        "STOP_"+
        stop_assignments_df["stop_id"]
        .astype(str)
        .str.zfill(3)
    )
    stops_df = pd.DataFrame(
        kmeans.cluster_centers_,columns=["latitude","longitude"]
    )
    stops_df["stop_id"] = (stops_df.index + 1)
    stops_df["stop_id"] = (
        "STOP_" +
        stops_df["stop_id"].astype(str).str.zfill(3)
    )
    stops_df = stops_df[
        ["stop_id","latitude","longitude"]
    ]
    return stops_df, stop_assignments_df
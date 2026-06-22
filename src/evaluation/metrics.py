"""

FILE:
metrics.py

PURPOSE:
Evaluate and compare school bus stop generation
algorithms using operational and planning metrics.

WORKFLOW:
1. Receive generated stops and stop assignments
2. Calculate performance metrics
3. Compare results across clustering methods
4. Quantify trade-offs between stop count,
   walking distance, and stop utilization

INPUT PARAMETERS:

students_df
Required Columns:
- student_id
- latitude
- longitude
- demand

stops_df
Required Columns:
- stop_id
- latitude
- longitude

stop_assignments_df
Required Columns:
- student_id
- stop_id

OUTPUT:
Individual metric values and algorithm
performance summaries.

CURRENT METRICS:
- Number of Stops
- Average Students Per Stop
- Maximum Students Per Stop

PLANNED METRICS:
- Average Walking Distance
- Maximum Walking Distance
- Total Walking Distance
- Average Walking Time
- Maximum Walking Time
- Total Walking Time
- Average Distance to School
- Maximum Distance to School
- Average Route Length
- Maximum Route Length
- Average Stop Utilization
- Stop Density
- Cluster Compactness
- Silhouette Score
- Number of Single-Student Stops
- Number of Multi-Student Stops

COMPARISON OBJECTIVE:

Evaluate differences between:

1. KMeans + Haversine Distance
2. KMeans + Road Distance
3. DBSCAN + Haversine Distance
4. DBSCAN + Road Distance

KEY RESEARCH QUESTION:

Does using road-network-aware clustering
produce operationally superior pickup stops
compared to traditional straight-line
distance approaches?

PROJECT:
School Transportation Planning Platform
Version 1 (Evaluation Engine)
"""
import numpy as np
import pandas as pd
from traveltime_engine.distance_matrix import(
     generate_distance_matrix
)
def calculate_haversine_distance(
        lat1,
        lon1,
        lat2,
        lon2
):
     earth_radius = 6371000
     lat1 = np.radians(lat1)
     lon1 = np.radians(lon1)
     lat2 = np.radians(lat2)
     lon2 = np.radians(lon2)

     delta_lat = lat2-lat1
     delta_lon = lon2-lon1

     a = (
          np.sin(delta_lat/2)**2
          +
          np.cos(lat1)
          *
          np.cos(lat2)
          *
          np.sin(delta_lon/2) **2
     )
     c = (
          2
          *
          np.arctan2(
               np.sqrt(a),
               np.sqrt(1-a)
          )
     )
     distance = earth_radius * c
     return distance
def calculate_number_of_stops(
            stops_df
    ):
        """calculate total number of generated stops"""
        return len(stops_df)
def calculate_average_students_per_stop(
        stops_assignment_df
):
    """calculate average number of students assigned to each stop"""
    students_per_stop = (
        stops_assignment_df
        .groupby("stop_id").size()
    )
    return students_per_stop.mean()
def calculate_max_students_per_stop(
        stop_assignment_df
):
    """calculate maximum number of students assigned to any stop"""
    students_per_stop = (
        stop_assignment_df
        .groupby("stop_id").size()    
    )
    return students_per_stop.max()

def calculate_walking_distance_metrics(
          student_df,
          stops_df,
          stop_assignments_df
):
     student_coordinates_df = (
          student_df[
               ["latitude","longitude"]
          ]
          .copy()
     )
     stop_coordinates_df = (
          stops_df[
               ["latitude","longitude"]
          ]
          .copy()
     )
     combined_coordinates_df = pd.concat(
          [
               student_coordinates_df,
               stop_coordinates_df
          ],
          ignore_index=True
     )
     
     distance_matrix= (
          generate_distance_matrix(
               combined_coordinates_df
          )
     )
     student_count = len(student_coordinates_df)
     stop_index_lookup = {}
     for i, stop_id in enumerate(stops_df["stop_id"]):
          stop_index_lookup[stop_id] = (
               student_count + i
          )
     walking_distances = []
     for student_index, row in (
          stop_assignments_df.iterrows()
     ):
          stop_id = row["stop_id"]
          stop_index = (
               stop_index_lookup[stop_id]
          )
          distance = min(
               distance_matrix[
                    student_index,
                    stop_index
               ],
               distance_matrix[
                    stop_index,
                    student_index
               ]
          )
          walking_distances.append(
               distance
          )
     print()
     walking_distances = np.array(
          walking_distances
     )
     average_distance = (
          walking_distances.mean()
     )
     median_distance = (
          np.median(walking_distances)
     )
     p95_distance = (
          np.percentile(
               walking_distances,
               95
          )
     )
     max_distance = (
          walking_distances.max()
     )
     print()
     print("------------------------")
     print("ACCESS DISTANCE")
     print(
          f"AVERAGE: "
          f"{average_distance:.1f} m"
     )
     print(
          f"Median: "
          f"{median_distance:.1f} m"
     )
     print(
          f"95th %ile: "
          f"{p95_distance:.1f} m"
     )
     print(
          f"Maximum: "
          f"{max_distance:.1f} m"
     )
     print("------------------------")
     print()

     return {
     "average_access_distance":
          average_distance,
     "median_access_distance":
          median_distance,
     "p95_access_distance":
          p95_distance,
     "max_access_distance":
          max_distance
}
     
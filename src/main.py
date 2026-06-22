"""
FILE:
main.py

PURPOSE:
Run the complete school bus stop generation workflow.

WORKFLOW:
1. Load student and school input data
2. Generate pickup stops using a selected algorithm
3. Create stop assignments for all students
4. Calculate stop-level statistics
5. Generate visualization datasets
6. Display results and create map outputs

INPUT:
- Student data
- School data

OUTPUT:
- stops_df
- stop_assignments_df
- visualization map
- summary statistics

NOTES:
- This file acts as the project controller
- Stop generation logic is implemented in the
  stop_generation module
- Travel time and distance calculations are
  implemented in the traveltime_engine module
- Evaluation metrics are implemented in the
  evaluation module
- The selected stop generation algorithm can be
  swapped without modifying the rest of the workflow

PROJECT:
School Transportation Planning Platform
Version 1 (Stop Generation Engine)

CURRENT CONFIGURATION:
- Stop Generation: DBSCAN (Road Distance)
- Distance Source: OSRM
- School: YIPS
"""
from evaluation.metrics import(
    calculate_average_students_per_stop, calculate_max_students_per_stop, calculate_number_of_stops, calculate_walking_distance_metrics
)
import pandas as pd
students_df = pd.read_csv("Inputs/students.csv")
whichschool = "YIPS"
school_students_df = students_df[students_df["school_id"]== whichschool]

from stop_generation.dbscan_onroad import generate_stops_dbscan_onroad

stops_df, stop_assignments_df = generate_stops_dbscan_onroad(school_students_df)
"""METRIC CALCULATION"""
calculate_walking_distance_metrics(
    school_students_df,
    stops_df,
    stop_assignments_df
) 
number_of_stops = (
    calculate_number_of_stops(stops_df)
)
average_students_per_stops = (
    calculate_average_students_per_stop(stop_assignments_df)
)
max_students_per_stop = (
    calculate_max_students_per_stop(stop_assignments_df)
)
print()
print("---------------------")
print("METRICS")
print(
    f"Number of Stops: "
    f"{number_of_stops}"
)
print(
    f"Average Students per Stop: "
    f"{average_students_per_stops:.2f}"
)
print(
    f"Maximum Students per Stop: "
    f"{max_students_per_stop}"
)
print("---------------------")
print()
"""VISUALIZATION CALCULATION"""
student_counts = (
    stop_assignments_df
    .groupby("stop_id")
    .size()
)
student_counts_df =  student_counts.to_frame(name="student_count")
student_counts_df = student_counts_df.reset_index()
stops_df = stops_df.merge(
    student_counts_df,
    on="stop_id"
)
assignments_by_demand = stop_assignments_df.merge(
    students_df[["student_id","demand"]],
    on="student_id"

)
total_demand = (
    assignments_by_demand
    .groupby("stop_id")["demand"]
    .sum()
)
total_demand_df = total_demand.to_frame(name="total_demand")
total_demand_df = total_demand_df.reset_index()
stops_df = stops_df.merge(
    total_demand_df,
    on="stop_id"
)
stops_df.to_csv(
    "Outputs/stops.csv",
    index=False
)
stop_assignments_df.to_csv(
    "Outputs/stop_assignment.csv",
    index=False
)
#Visualization on Map
visualization_df = stop_assignments_df.merge(
    students_df[
        ["student_id", "latitude", "longitude"]
    ],
    on="student_id"
)
visualization_df = visualization_df.rename(
    columns={
        "latitude" : "student_lat",
        "longitude" : "student_lng"
    }
)

visualization_df = visualization_df.merge(
    stops_df[
        ["stop_id","latitude","longitude"]
    ],
    on="stop_id"
)
visualization_df = visualization_df.rename(
    columns={
        "latitude":"stop_lat",
        "longitude":"stop_lng"
    }
)

import folium
map_centre = [
    school_students_df["latitude"].mean(),
    school_students_df["longitude"].mean()
]
m = folium.Map(
    location = map_centre,
    zoom_start=12
)
#plotting students
for _, row in visualization_df.iterrows():
    folium.CircleMarker(
        location=[
            row["student_lat"],
            row["student_lng"]
        ],
        radius=2,
        color="blue",
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

for _, row in stops_df.iterrows():
    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        radius=8,
        color = "red",
        fill = True,
        fill_color = "red",
        fill_opacity = 0.1,
        popup=(
            f"{row['stop_id']}<br>"
            f"Students: {row['student_count']}"
        )
    ).add_to(m)

for _, row in visualization_df.iterrows():
    folium.PolyLine(
        locations=[
            [row["student_lat"],row["student_lng"]],
            [row["stop_lat"],row["stop_lng"]]
        ],
        color="black",
        weight=1,
        opacity=0.4
    ).add_to(m)



    m.save("Outputs/stop_generation.html")
print("fin")
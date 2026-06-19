import pandas as pd
from sklearn.cluster import KMeans

def generate_stops_kmeans(students_df):
    
    coordinates_df = students_df[["latitude","longitude"]]
    coordinates = coordinates_df.values
    k=20
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
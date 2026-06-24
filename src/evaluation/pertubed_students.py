import pandas as pd
import numpy as np

students_df = pd.read_csv(
    "Inputs/students.csv"
)

earth_radius = 6371000  # metres

for index, row in students_df.iterrows():

    distance = np.random.uniform(
        0,
        300
    )

    bearing = np.random.uniform(
        0,
        2 * np.pi
    )

    lat_rad = np.radians(
        row["latitude"]
    )

    lon_rad = np.radians(
        row["longitude"]
    )

    angular_distance = (
        distance / earth_radius
    )

    new_lat = np.arcsin(
        np.sin(lat_rad)
        * np.cos(angular_distance)
        +
        np.cos(lat_rad)
        * np.sin(angular_distance)
        * np.cos(bearing)
    )

    new_lon = lon_rad + np.arctan2(
        np.sin(bearing)
        * np.sin(angular_distance)
        * np.cos(lat_rad),
        np.cos(angular_distance)
        -
        np.sin(lat_rad)
        * np.sin(new_lat)
    )

    students_df.loc[
        index,
        "latitude"
    ] = np.degrees(new_lat)

    students_df.loc[
        index,
        "longitude"
    ] = np.degrees(new_lon)

students_df.to_csv(
    "Inputs/students_perturbed1.csv",
    index=False
)

print(
    "Perturbed dataset created."
)
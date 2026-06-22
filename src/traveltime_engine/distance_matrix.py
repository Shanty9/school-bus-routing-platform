"""
FILE:
distance_matrix.py

PURPOSE:
Generate a pairwise road-distance matrix between all
student locations using a locally hosted OSRM server.

WORKFLOW:
1. Extract latitude and longitude coordinates from
   the student dataset
2. Build an OSRM Table API request
3. Send coordinates to the local OSRM server
4. Retrieve road-network distances between all
   student pairs
5. Convert results into a NumPy distance matrix
6. Return the matrix for clustering algorithms

INPUT:
students_df

REQUIRED COLUMNS:
- latitude
- longitude

OUTPUT:
distance_matrix

FORMAT:
NxN NumPy Array

Example:

                Student A   Student B   Student C

Student A           0         1240         890
Student B         1240           0         540
Student C          890         540           0

Values represent road-network distance in metres.

DEPENDENCIES:
- Local OSRM Server
- OpenStreetMap Road Network
- requests
- numpy

NOTES:
- Uses OSRM Table API
- Distances represent actual travel distance along
  the road network
- Distance matrix is symmetric in most cases but
  may differ slightly due to one-way roads
- Negative or invalid values are replaced with zero
- Supports batching for larger datasets if required

ADVANTAGES:
- Captures real-world road connectivity
- Avoids unrealistic straight-line assumptions
- Enables road-network-aware clustering

LIMITATIONS:
- Requires OSRM preprocessing and server setup
- Accuracy depends on OpenStreetMap data quality
- Large matrices increase computational cost
- OSRM Table API has coordinate limits which may
  require batching

PROJECT:
School Transportation Planning Platform
Version 1 (Travel Time Engine)
"""

import requests
import numpy as np

def generate_distance_matrix(
        students_df
):
    num_students = len(students_df)

    coordinates = students_df[
        ["longitude","latitude"]
    ].values.tolist()

    coordinate_string = ";".join(
        [
            f"{lng},{lat}"
            for lng, lat in coordinates
        
        ]
    )
    
    url = (
        f"http://localhost:5000/table/v1/driving/"
        f"{coordinate_string}"
        f"?annotations=distance"
    )

    response = requests.get(url)

    data = response.json()
 
    if response.status_code != 200:
        print(data)
        return None

    distance_matrix = np.array(data["distances"])
    distance_matrix[distance_matrix<0] = 0
    
    return distance_matrix
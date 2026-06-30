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
#================================================================================================================================================
# IMPORTS
#================================================================================================================================================
import pandas as pd
from evaluation.metrics import(
    calculate_average_students_per_stop, calculate_max_students_per_stop, calculate_number_of_stops, calculate_walking_distance_metrics
)
from evaluation.evaluate_stops import evaluate_stops
from stop_generation.dbscan_onroad import generate_stops_dbscan_onroad
from visualization.stop_generation_map import (
    create_stop_generation_map
)
from file_io.save_outputs import(save_outputs)
from visualization.prepare_visualization_data import (prepare_visualization_data)
from outputs.prepare_stop_outputs import (prepare_stop_outputs)
from stop_placement.stop_placement import (place_stops)
#================================================================================================================================================
# LOAD INPUT DATA
#================================================================================================================================================

students_df = pd.read_csv("Inputs/students_perturbed5.csv")
whichschool = "YIPS"
school_students_df = students_df[students_df["school_id"]== whichschool]

#================================================================================================================================================
# GENERATE STOPS
#================================================================================================================================================

stops_df, stop_assignments_df = generate_stops_dbscan_onroad(school_students_df)


#================================================================================================================================================
# PLACE STOPS ON ROAD
#================================================================================================================================================
stops_df = place_stops(
    stops_df
)
#================================================================================================================================================
# EVALUATE STOP GENERATION
#================================================================================================================================================
evaluate_stops(
    school_students_df,
    stops_df,
    stop_assignments_df
)
#================================================================================================================================================
# PREPARE STOP OUTPUTS
#================================================================================================================================================
stops_df = prepare_stop_outputs(
    students_df,
    stops_df,
    stop_assignments_df
)

#================================================================================================================================================
# EXPORT OUTPUT DATASETS
#================================================================================================================================================

save_outputs(
    stops_df,
    stop_assignments_df
)

#================================================================================================================================================
# CREATE VISUALIZATION
#================================================================================================================================================

visualization_df = (
    prepare_visualization_data(
        students_df,
        stops_df,
        stop_assignments_df
    )
)

create_stop_generation_map(
    school_students_df,
    stops_df,
    visualization_df,
    "Outputs/stops_generated_map.html"
)
print("----------------")
print("Stops Generated")
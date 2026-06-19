import pandas as pd
students_df = pd.read_csv("Inputs/students.csv")
whichschool = "YIPS"
school_students_df = students_df[students_df["school_id"]== whichschool]

from stop_generation.kmeans import generate_stops_kmeans

stops_df, stop_assignments_df = generate_stops_kmeans(school_students_df)
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
print(assignments_by_demand.head(10))
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
# print(stops_df.head(10))
# print(student_counts_df.head(10))
# print(stops_df)
# print(stop_assignments_df)

def save_outputs(
        stops_df,
        stop_assignments_df
):
    stops_df.to_csv(
        "Outputs/stops.csv",
        index = False
    )
    stop_assignments_df.to_csv(
        "outputs/stop_assignment.csv",
        index = False
    )
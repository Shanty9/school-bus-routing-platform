from evaluation.metrics import (
    calculate_walking_distance_metrics,
    calculate_number_of_stops,
    calculate_average_students_per_stop,
    calculate_max_students_per_stop
)

def evaluate_stop_generation(
        student_df,
        stops_df,
        stop_assignments_df
):

    calculate_walking_distance_metrics(
        student_df,
        stops_df,
        stop_assignments_df
    )

    number_of_stops = (
        calculate_number_of_stops(stops_df)
    )

    average_students_per_stop = (
        calculate_average_students_per_stop(
            stop_assignments_df
        )
    )

    maximum_students_per_stop = (
        calculate_max_students_per_stop(
            stop_assignments_df
        )
    )

    print()
    print("---------------------")
    print("METRICS")
    print(
        f"Number of Stops: {number_of_stops}"
    )
    print(
        f"Average Students per Stop: "
        f"{average_students_per_stop:.2f}"
    )
    print(
        f"Maximum Students per Stop: "
        f"{maximum_students_per_stop}"
    )
    print("---------------------")
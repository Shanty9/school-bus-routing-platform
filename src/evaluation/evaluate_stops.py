from evaluation.metrics import calculate_haversine_distance

def evaluate_stops(
        school_students_df,
        stops_df,
        stop_assignment_df
):
    evaluation_df = prepare_evaluation_dataframe(
        school_students_df,
        stops_df,
        stop_assignment_df
    )
    print(evaluation_df.head())
    evaluate_student_access(
        evaluation_df
    )
    evaluate_stop_placement(
        stops_df
    )

def prepare_evaluation_dataframe(
        school_students_df,
        stops_df,
        stop_assignements_df
):
    evaluation_df = (
        stop_assignements_df.merge(
            school_students_df[
                [
                    "student_id", "latitude", "longitude"
                ]
            ], on = "student_id"
        )
    )
    evaluation_df = evaluation_df.rename(
        columns={
            "latitude":"student_lat",
            "longitude":"student_lng"
        }
    )
    evaluation_df = evaluation_df.merge(
        stops_df[
            [
                "stop_id",
                "latitude",
                "longitude",
                "generated_latitude",
                "generated_longitude"
            ]
        ], on="stop_id"
    )
    evaluation_df = evaluation_df.rename(
        columns={
            "latitude": "snapped_stop_lat",
            "longitude": "snapped_stop_lng",
            "generated_latitude": "generated_stop_lat",
            "generated_longitude": "generated_stop_lng"
        }
    )
    print("Evaluation DF Columns")
    print(evaluation_df.columns.tolist())
    return evaluation_df

def evaluate_student_access(
        evaluation_df
):
    evaluation_df["walking_distance"] = (
        calculate_haversine_distance(
            evaluation_df["student_lat"],
            evaluation_df["student_lng"],
            evaluation_df["snapped_stop_lat"],
            evaluation_df["snapped_stop_lng"],
        )
    )
    print("------------------------")
    print("Snapped Access Distance")
    print("------------------------")
    print(
        f"Average: {evaluation_df['walking_distance'].mean():.1f} m"
    )
    print(
        f"Median: {evaluation_df['walking_distance'].median():.1f} m"
    )
    print(
        f"95th %-ile: {evaluation_df['walking_distance'].quantile(0.95):.1f} m"
    )
    print(
        f"Maximum: {evaluation_df['walking_distance'].max():.1f} m"
    )
    print(
        f"Within 250m: {(evaluation_df['walking_distance'] <= 250).mean():.0%}"
    )
    print(
        f"Within 500m: {(evaluation_df['walking_distance'] <= 500).mean():.0%}"
    )
    print("------------------------")
    print()
    
def evaluate_stop_placement(
        stops_df
):
    pass
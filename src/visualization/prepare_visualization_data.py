import pandas as pd


def prepare_visualization_data(
        students_df,
        stops_df,
        stop_assignments_df
):

    visualization_df = (
        stop_assignments_df.merge(
            students_df[
                [
                    "student_id",
                    "latitude",
                    "longitude"
                ]
            ],
            on="student_id"
        )
    )

    visualization_df = visualization_df.rename(
        columns={
            "latitude": "student_lat",
            "longitude": "student_lng"
        }
    )

    visualization_df = visualization_df.merge(
        stops_df[
            [
                "stop_id",
                "latitude",
                "longitude"
            ]
        ],
        on="stop_id"
    )

    visualization_df = visualization_df.rename(
        columns={
            "latitude": "stop_lat",
            "longitude": "stop_lng"
        }
    )

    return visualization_df
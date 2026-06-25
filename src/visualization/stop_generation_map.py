import folium


def create_stop_generation_map(
        school_students_df,
        stops_df,
        visualization_df,
        output_file
):

    map_centre = [
        school_students_df["latitude"].mean(),
        school_students_df["longitude"].mean()
    ]

    m = folium.Map(
        location=map_centre,
        zoom_start=12
    )

    # Plot students
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

    # Plot stops
    for _, row in stops_df.iterrows():
        folium.CircleMarker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            radius=8,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.1,
            popup=(
                f"{row['stop_id']}<br>"
                f"Students: {row['student_count']}"
            )
        ).add_to(m)

    # Plot assignment lines
    for _, row in visualization_df.iterrows():
        folium.PolyLine(
            locations=[
                [row["student_lat"], row["student_lng"]],
                [row["stop_lat"], row["stop_lng"]]
            ],
            color="black",
            weight=1,
            opacity=0.4
        ).add_to(m)

    m.save(output_file)
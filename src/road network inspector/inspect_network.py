import subprocess

OSM_DIRECTORY = "D:/OSRM/data"
OSM_FILE = "hyderabad.osm.pbf"


def export_roads():

    print()
    print("--------------------------------")
    print("EXPORTING ROAD NETWORK")
    print("--------------------------------")

    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{OSM_DIRECTORY}:/data",
            "iboates/osmium",
            "tags-filter",
            f"/data/{OSM_FILE}",
            "w/highway",
            "-o",
            "/data/highways.osm.pbf",
            "--overwrite"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Road network extracted successfully.")
    else:
        print(result.stderr)


export_roads()

def export_roads_geojson():

    print()
    print("--------------------------------")
    print("EXPORTING ROAD GEOJSON")
    print("--------------------------------")

    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{OSM_DIRECTORY}:/data",
            "iboates/osmium",
            "export",
            "/data/highways.osm.pbf",
            "-o",
            "/data/highways.geojson",
            "--overwrite"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Road GeoJSON exported successfully.")
    else:
        print(result.stderr)

export_roads()

export_roads_geojson()
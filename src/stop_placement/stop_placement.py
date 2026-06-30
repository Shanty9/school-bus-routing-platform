search_radii = [100,200,300,400]

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
ROAD_PLACEMENT_POLICY = {
    "living_street": {
        "allowed":True,
        "base_cost": 0
        },
    "residential": {
        "allowed": True,
        "base_cost": 0
        },
    "service": {
        "allowed": True,
        "base_cost": 2
        },
    "unclassified": {
        "allowed": True,
        "base_cost": 5
        },
    "tertiary":{
        "allowed": True,
        "base_cost": 10
        },
    "secondary": {
        "allowed": True,
        "base_cost": 25
        },
    "primary": {
        "allowed": True,
        "base_cost": 50
        },
    "trunk": {
        "allowed": True,
        "base_cost": 50
        },
    "motorway":{
        "allowed": False,
        "base_cost": 9999
        }

    }

def load_road_network():
    roads_df = gpd.read_file(
        "D:/OSRM/data/highways.geojson"
    )

    roads_df = roads_df[
        roads_df.geom_type == "LineString"
    ]
    roads_df = roads_df.to_crs(
        epsg=32644
    )

    return roads_df

def get_candidate_roads(
    stop_point,
    roads_df,
    spatial_index,
    search_radius
):
    search_area = stop_point.buffer(
        search_radius
    )
    candidate_indices = spatial_index.query(
        search_area,
        predicate="intersects"
    )
    candidate_roads = roads_df.iloc[
        candidate_indices
    ]
    return candidate_roads

def filter_serviceable_roads(
    candidate_roads
):
    allowed_highways = [
        highway
        for highway, policy
        in ROAD_PLACEMENT_POLICY.items()
        if policy["allowed"]
    ]
    serviceable_roads = candidate_roads[
        candidate_roads["highway"].isin(
            allowed_highways
        )
    ]

    return serviceable_roads

def place_single_stop(
        stop_row,
        roads_df,
        spatial_index
):
    stop_point =  gpd.GeoSeries(
        [
            Point(
                stop_row["longitude"],
                stop_row["latitude"]
            )
        ],
        crs = "EPSG:4326"
    )

    stop_point = stop_point.to_crs(
        epsg = 32644
    ).iloc[0]

    
    serviceable_roads = None
    candidate_roads = None
    radius_used = None

    for radius in search_radii:

        candidate_roads = get_candidate_roads(
            stop_point,
            roads_df,
            spatial_index,
            radius
        )

        serviceable_roads = filter_serviceable_roads(
            candidate_roads
        )

        if not serviceable_roads.empty:
            radius_used = radius
            if radius > 100:
                print(
                    f"{stop_row['stop_id']} used {radius_used}m search_radius."
                )
            break


    evaluated_roads = evaluate_candidate_roads(
        stop_point,
        serviceable_roads
    )
    if serviceable_roads.empty:
        print("NO Serviceable Roads Found")
        print("==========================")
        print(f"Stop ID: {stop_row['stop_id']}")
        print(
            f"Latitude: {stop_row['latitude']}"
        )

        print(
            f"Longitude:  {stop_row['longitude']}")
        print()
        print("original stop row")
        print(stop_row)
        print()
        print(f"Candidate Roads Found: {len(candidate_roads)}")
        
        if len(candidate_roads) > 0:
            print(candidate_roads[
                [
                "highway",
                "name",
                "oneway"
                ]
            ])
        return None
    
    best_road = select_best_road(
        evaluated_roads
    )
    snapped_point = snap_stop_to_road(
        stop_point,
        best_road
    )

    return (
        snapped_point,
        radius_used,
        best_road
    )

def place_stops(
    stops_df
):
    roads_df = load_road_network()
    spatial_index = roads_df.sindex
    
    stops_df["generated_latitude"] = stops_df["latitude"]
    stops_df["generated_longitude"] = stops_df["longitude"]
    stops_df["snap_distance"] = None
    stops_df["road_type"] = None
    stops_df["road_name"] = None
    stops_df["search_radius"] = None
    

    placement_report = []

    for index, stop_row in stops_df.iterrows():
        snapped_point, radius_used, best_road = place_single_stop(
            stop_row,
            roads_df,
            spatial_index
        )
        if snapped_point is None:
            continue
        latitude, longitude = convert_to_latlon(
            snapped_point
        )
        stops_df.loc[index, "latitude"] = latitude
        stops_df.loc[index, "longitude"] = longitude

        

        stops_df.loc[index, "snap_distance"] = (
            best_road["distance"]
        )

        stops_df.loc[index, "road_type"] = (
            best_road["highway"]
        )

        stops_df.loc[index, "road_name"] = (
            best_road["name"]
        )

        stops_df.loc[index, "search_radius"] = (
            radius_used
        )

        placement_report.append(
            {
                "stop_id": stop_row["stop_id"],
                "generated_latitude": stop_row["generated_latitude"],
                "generated_longitude": stop_row["generated_longitude"],
                "snapped_latitude": latitude,
                "snapped_longitude": longitude,
                "search_radius": radius_used,
                "snap_distance": best_road["distance"],
                "road_type": best_road["highway"],
                "road_name": best_road["name"]
            }
        )
    placement_report_df = pd.DataFrame(
        placement_report
    )
    print()

    return stops_df

def convert_to_latlon(
        snapped_point
):
    snapped_gfd = gpd.GeoSeries(
        [snapped_point], crs= "EPSG:32644"
    )
    snapped_gfd = snapped_gfd.to_crs( 
        epsg = 4326
    )
    latitude = snapped_gfd.iloc[0].y
    longitude = snapped_gfd.iloc[0].x

    return latitude, longitude
def evaluate_candidate_roads(
    stop_point,
    serviceable_roads
):
    serviceable_roads = serviceable_roads.copy()

    serviceable_roads["distance"] = (
        serviceable_roads.geometry.distance(
        stop_point
        )
    )

    serviceable_roads["road_cost"] = (
        serviceable_roads["highway"].map(
            lambda highway:
            ROAD_PLACEMENT_POLICY[
                highway
            ]["base_cost"]
        )
    )
    serviceable_roads ["total_cost"] = (
        serviceable_roads["distance"] 
        +
        serviceable_roads["road_cost"]
    )
    serviceable_roads = (
        serviceable_roads.sort_values("total_cost")
    )
    return serviceable_roads
def select_best_road(
        evaluated_roads
):
    best_road = evaluated_roads.iloc[0]
    return best_road
    


def snap_stop_to_road(
        stop_point,
        best_road
):
    distance_along_road = (
        best_road.geometry.project(
            stop_point
        )
    )
    snapped_point = (
        best_road.geometry.interpolate(
            distance_along_road
        )
    )
    return snapped_point
    

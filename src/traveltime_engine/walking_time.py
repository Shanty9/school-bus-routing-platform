import requests

def get_walking_time(
        origin_lat,
        origin_lng,
        destination_lat,
        destination_lng
):
    url = (
        f"https://router.project-osrm.org/route/v1/walking/"
        f"{origin_lng},{origin_lat};"
        f"{destination_lng},{destination_lat}"
        f"?overview=false"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(response.json())
        return None
    data = response.json()
    distance = data["routes"][0]["distance"]
    duration = data["routes"][0]["duration"]
    
    return{
        "distance": distance,
        "time": duration        
    }

result = get_walking_time(
    17.400221,
    78.367261,
    17.402233,
    78.380569
)
print(result)

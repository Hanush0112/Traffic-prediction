import requests

def get_alternate_routes(origin, destination, api_key):
    url = (
        "https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&alternatives=true&key={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        raise Exception(f"API Error: {data.get('error_message', 'Unknown error')}")

    routes_info = []
    for route in data["routes"]:
        leg = route["legs"][0]
        summary = {
            "summary": route.get("summary", "No summary"),
            "duration": leg["duration"]["text"],
            "distance": leg["distance"]["text"],
            "steps": [(step["html_instructions"], step["distance"]["text"]) for step in leg["steps"]],
            "polyline": route["overview_polyline"]["points"]
        }
        routes_info.append(summary)
    
    return routes_info

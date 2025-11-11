import requests

def get_current_temp(lat: float, lon: float) -> float:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current=temperature_2m"
    )
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    return float(data["current"]["temperature_2m"])

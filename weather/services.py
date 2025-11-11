import requests


def get_current_temp(lat: float, lon: float) -> float:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current=temperature_2m"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return float(response.json()["current"]["temperature_2m"])

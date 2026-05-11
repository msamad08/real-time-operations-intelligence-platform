from pathlib import Path
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = "56e96713bcc78e052f73e85be6d0614f"

locations = [
    {"zone_id": "ZONE_001", "city": "Nashville"},
    {"zone_id": "ZONE_002", "city": "Memphis"},
    {"zone_id": "ZONE_003", "city": "Clarksville"},
    {"zone_id": "ZONE_004", "city": "Knoxville"},
    {"zone_id": "ZONE_005", "city": "Chattanooga"}
]

weather_data = []

for loc in locations:
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={loc['city']},US&appid={API_KEY}&units=imperial"
    )

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        weather_data.append({
            "zone_id": loc["zone_id"],
            "city": loc["city"],
            "temperature_f": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather_condition": data["weather"][0]["main"]
        })
    else:
        print(f"FAILED: {loc['city']}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")

df = pd.DataFrame(weather_data)

output_path = OUTPUT_DIR / "live_weather_data.csv"
df.to_csv(output_path, index=False)

if df.empty:
    print("No weather data was retrieved. Check API key activation or API response above.")
else:
    print("Live weather data ingested successfully.")
    print(df)
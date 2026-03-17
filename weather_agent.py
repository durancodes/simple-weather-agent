import time
import requests
from geopy.geocoders import Nominatim
from huggingface_hub import InferenceClient


# =========================
# GEOCODING
# =========================

_geolocator = Nominatim(user_agent="free-weather-agent")

def geocode_with_retry(location: str, retries: int = 2, delay: float = 1.0):
    """Convert city name to latitude/longitude with retries."""
    for _ in range(retries + 1):
        try:
            geo = _geolocator.geocode(location)
            if geo:
                return geo
        except Exception:
            pass
        time.sleep(delay)
    return None


# =========================
# TOOL: WEATHER FETCH
# =========================

def get_weather_forecast(location: str) -> str:
    """
    Fetch real weather data from Open-Meteo.
    This function is the SINGLE SOURCE OF TRUTH.
    """

    geo = geocode_with_retry(location)
    if geo is None:
        raise RuntimeError("Location not found")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": geo.latitude,
        "longitude": geo.longitude,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "precipitation"
        ]
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    current = response.json()["current"]

    return (
        f"Weather forecast for {location}:\n"
        f"- Temperature: {current['temperature_2m']} °C\n"
        f"- Wind Speed: {current['wind_speed_10m']} km/h\n"
        f"- Precipitation: {current['precipitation']} mm\n"
    )


# =========================
# AGENT RULES
# =========================

SYSTEM_PROMPT = """
You are a STRICT tool-using agent.

You have access to ONE tool:
get_weather_forecast

Rules:
- You may use the tool AT MOST ONCE
- You MUST stop after emitting Action
- You MUST NOT invent weather data
- You MUST NOT add new fields not in Observation
- Final Answer MUST repeat the Observation verbatim.
- DO NOT summarize, infer, or describe conditions.


Format:

Question: <question>
Thought: <why tool is needed>
Action:
{"action": "get_weather_forecast", "action_input": {"location": "<city>"}}

After Observation:

Thought: I now know the final answer
Final Answer: <repeat Observation exactly>

Begin.
"""


# =========================
# AGENT CONTROLLER
# =========================

client = InferenceClient(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct"
)

def run_weather_agent(location: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"What's the weather in {location}?"}
    ]

    # Step 1: Reasoning
    decision = client.chat.completions.create(
        messages=messages,
        max_tokens=200,
        stop=["Observation:"]
    )

    partial = decision.choices[0].message.content

    # Step 2: Tool execution (Python-controlled)
    try:
        observation = get_weather_forecast(location)
    except Exception as e:
        observation = f"Weather error: {e}\n"

    # Step 3: Inject observation
    messages.append({
        "role": "assistant",
        "content": partial + "\nObservation:\n" + observation
    })

    # Step 4: Final answer
    final = client.chat.completions.create(
        messages=messages,
        max_tokens=150
    )

    return final.choices[0].message.content


# =========================
# CLI
# =========================

def ask_weather():
    while True:
        location = input("📍 Enter a location (or 'exit'): ").strip()
        if location.lower() in {"exit", "quit"}:
            print("👋 Exiting")
            break

        try:
            print("\n" + run_weather_agent(location) + "\n")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    ask_weather()

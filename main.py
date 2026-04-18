import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# TOOL FUNCTION
# -----------------------------
def get_current_weather(city: str, unit: str = "celsius") -> str:
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        with urllib.request.urlopen(geo_url) as response:
            geo_data = json.loads(response.read().decode())

        if "results" not in geo_data:
            return f"City not found: {city}"

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
        with urllib.request.urlopen(weather_url) as response:
            weather_data = json.loads(response.read().decode())

        temp = weather_data["current"]["temperature_2m"]

        return f"Weather in {city}: {temp}°C"

    except Exception as ex:
        return f"Error: {ex}"


# -----------------------------
# TOOL SCHEMA
# -----------------------------
tools = [
    {
        "function_declarations": [
            {
                "name": "get_current_weather",
                "description": "Get current weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "unit": {"type": "string"}
                    },
                    "required": ["city"]
                }
            }
        ]
    }
]


# -----------------------------
# MAIN
# -----------------------------
def main():
    user_query = input("Ask something: ")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=user_query,
        config={
            "tools": tools
        }
    )

    candidate = response.candidates[0]
    part = candidate.content.parts[0]

    # TOOL CALL
    if hasattr(part, "function_call") and part.function_call:
        function_name = part.function_call.name
        args = dict(part.function_call.args)

        print(f"\n[TOOL CALL] {function_name} -> {args}")

        if function_name == "get_current_weather":
            result = get_current_weather(**args)
            print(f"\n[RESULT] {result}")

    #  NORMAL RESPONSE
    else:
        print("\n[RESPONSE]")
        print(response.text)


if __name__ == "__main__":
    main()
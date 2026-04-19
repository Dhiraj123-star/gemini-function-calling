import os
import json
import sqlite3
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

def get_current_time(timezone:str="Asia/Kolkata")-> str:
    """"Gets the current time (default: IST)"""
    try:
        url = f"https://timeapi.io/api/Time/current/zone?timeZone={urllib.parse.quote(timezone)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": 'GeminiToolCalling/1.0',
                'Accept':'application/json'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        time_str= data.get("time")
        date_str = data.get("date")

        if time_str and date_str:
            return f"The current time in {timezone} is {time_str} on {date_str}."
        
        return f"Could not fetch time for {timezone}"
    
    except Exception as e:
        return f"Error fetching time: {e}"

def get_user_info(user_id: int)->str:
    try:
        conn = sqlite3.connect("app.db")
        cursor= conn.cursor()

        cursor.execute("SELECT id, name, email,city FROM users WHERE id= ?",(user_id,))

        row =cursor.fetchone()

        conn.close()
        
        if row:
            return f"User {row[1]} lives in {row[3]} and their email is {row[2]}."
        else:
            return f"No user found with ID {user_id}."
        
    except Exception as e:
        return f"Database error: {e}"
    
# -----------------------------
# TOOL SCHEMA
# -----------------------------
tools = [
    {
        "function_declarations": [
            {
                "name":"get_current_weather",
                "description":"Get current weather for a city",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "city":{"type":"string"},
                        "unit":{"type":"string"}
                    },
                    "required":["city"]
                }
            },
            {
                "name": "get_current_time",
                "description": "Get current time for a timezone (default IST if not provided)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "Timezone like 'Asia/Kolkata', 'Europe/London'"
                        }
                    }
                }
            },
            {
                "name": "get_user_info",
                "description": "Fetch user details from database using user ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID to fetch details"
                        }
                    },
                    "required":["user_id"]
                }
            }
        ]
    }
]

def extract_text(response):
    try:
        parts = response.candidates[0].content.parts
        return " ".join(
            part.text for part in parts
            if hasattr(part,"text") and part.text
        )
    except:
        return "No valid response"

# -----------------------------
# MAIN
# -----------------------------
def main():
    user_query = input("Ask something: ")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=user_query,
        config={
            "system_instruction": """
        If the user asks about user details, profiles or database info, use the get_user_info tool. 
""",
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
            tool_result = get_current_weather(**args)
        
        elif function_name == "get_current_time":
            if "timezone" not in args:
                args["timezone"]= "Asia/Kolkata"
            tool_result = get_current_time(**args)

        elif function_name == "get_user_info":
            tool_result = get_user_info(**args)

        print(f"\n[RESULT] {tool_result}")

        # send result back to gemini
        follow_up_response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": user_query}]

                },
                candidate.content, # model's tool call
                {
                    "role": "tool",
                    "parts": [
                        {
                            "function_response": {
                                "name": function_name,
                                "response": {"result":tool_result}
                            }
                        }
                    ]
                }
            ],
            config ={
                "system_instruction": """
            You are a helpful and friendly AI assistant. 

            Instructions:
            - Always respond in a natural, human-friendly tone
            - Do not just repeat the tool result
            - Add helpful context (e.g., is it hot, cold ,pleasant?)
            - Optionally suggest what the user might do (e.g, carry a jacket,stay hydrated)
            - Keep the answer but engaging
            - Add some humour at last but friendly 
            
            """
            }
        )
        print("\n[Final response]")
        print(extract_text(follow_up_response))

    #  NORMAL RESPONSE
    else:
        print("\n[RESPONSE]")
        print(response.text)


if __name__ == "__main__":
    main()
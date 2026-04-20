import json
import urllib.request
import urllib.parse
import sqlite3

# -----------------------------
# TOOL FUNCTION
# -----------------------------

# -------- WEATHER -----------
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

# --------- TIME ----------
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

# ------ DB TOOL ----------
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
    
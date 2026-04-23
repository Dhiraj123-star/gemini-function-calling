import json
import urllib.request
import urllib.parse
import sqlite3
from app.cache import get_cache,set_cache

# -----------------------------
# TOOL FUNCTION
# -----------------------------

# -------- WEATHER -----------
def get_current_weather(city: str, unit: str = "celsius") -> str:
    cache_key = f"weather:{city.lower()}"
    cached = get_cache(cache_key)
    if cached:
        print("cached hit !!")
        return f"(cached) {cached}"
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

        result= f"Weather in {city}: {temp}°C"

        set_cache(cache_key,result,ttl=600) # 10 min
        return result

    except Exception as ex:
        return f"Error: {ex}"

# --------- TIME ----------
def get_current_time(timezone:str="Asia/Kolkata")-> str:
    """"Gets the current time (default: IST)"""
    cache_key = f"time:{timezone}"
    cached = get_cache(cache_key)
    if cached:
        return f"(cached) {cached}"
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
            result= f"The current time in {timezone} is {time_str} on {date_str}."
            set_cache(cache_key,result,ttl=60) # 1 min
            return result
        
        return f"Could not fetch time for {timezone}"
    
    except Exception as e:
        return f"Error fetching time: {e}"

# ------ DB TOOL ----------
def get_user_info(user_id: int)->str:
    cache_key = f"user:{user_id}"

    cached= get_cache(cache_key)

    if cached:
        return f"(cached) {cached}"
    try:
        conn = sqlite3.connect("app.db")
        cursor= conn.cursor()

        cursor.execute("SELECT id, name, email,city FROM users WHERE id= ?",(user_id,))

        row =cursor.fetchone()

        conn.close()
        
        if row:
            result=  f"User {row[1]} lives in {row[3]} and their email is {row[2]}."
            set_cache(cache_key,result,ttl=300) # 5 min
            return result
        else:
            return f"No user found with ID {user_id}."
        
    except Exception as e:
        return f"Database error: {e}"
    
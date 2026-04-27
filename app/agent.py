import os
from dotenv import load_dotenv
from google import genai
from app.tools import get_current_weather,get_current_time,get_user_info

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Tool registry
TOOL_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_current_time" : get_current_time,
    "get_user_info": get_user_info
}

# Tool schema

TOOLS = [
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

# -----------------------
# Multi-step Agent loop
# -----------------------

def run_agent(user_query:str,max_steps:int=5) ->str:
    messages=[
        {
            "role": "user",
            "parts": [{"text":user_query}]
        }
    ]
    for step in range(max_steps):
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            content=messages,
            config={
                "tools": TOOLS,
                "system_instructions":"""
You are a helpful and friendly AI Assistant.
Instructions:
- Use tools when needed
- If user asks about database/user info -> use get_user_info
- If multiple data points are needed -> call tools step by step
- Always combine results before answering

Tone:
- Natural and human-friendly
- Add helpful context (hot/cold/pleasant etc.)
- Suggest actions if useful
- Add light friendly humor at the end

"""
            }
        )
        candidate= response.candidates[0]
        parts= candidate.content.parts

        # -----------------------
        # Check for tool call
        # -----------------------
        function_part =None
        for p in parts:
            if hasattr(p,"function_call") and p.function_call:
                function_part=p
                break
        if function_part:
            fn_name = function_part.function_call.name
            args = dict(function_part.function_call.args)

            if fn_name not in TOOL_FUNCTIONS:
                return f"Unknown tool: {fn_name}"
            
            # Execute tool
            tool_result = TOOL_FUNCTIONS[fn_name](**args)

            # Add model's function call
            messages.append({
                "role":"model",
                "parts":[function_part]
            })

            # Add tool response
            messages.append({
                "role":"user",
                "parts":[
                    {
                        "function_response":{
                            "name":fn_name,
                            "response":{"result":tool_result}
                        }
                    }
                ]
            })
        else:
            # Final response
            return extract_text(response)

    return "Max steps reached without final response!!"
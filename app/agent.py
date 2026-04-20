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

def run_agent(user_query:str)-> str:
    # Step 1
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=user_query,
        config={
            "system_instruction": """
        If the user asks about user details, profiles or database info, use the get_user_info tool. 
""",
            "tools": TOOLS
        }
    ) 
    part = response.candidates[0].content.parts[0]

    # Step 2 -> Tool call
    if hasattr(part,"function_call") and part.function_call:
        fn_name = part.function_call.name
        args = dict(part.function_call.args)

        tool_result= TOOL_FUNCTIONS[fn_name](**args)
    
        # Step 3 -> send back 
        final_response = client.models.generate_content (
            model="gemini-3.1-flash-lite-preview",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": user_query}]

                    },
                    response.candidates[0].content, # model's tool call
                    {
                        "role": "tool",
                        "parts": [
                            {
                                "function_response": {
                                    "name": fn_name,
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
        return extract_text(final_response)

    return extract_text(response)
        
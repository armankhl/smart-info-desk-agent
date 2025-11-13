# main.py (Simplified for Phase 1)
import os
import json
from dotenv import load_dotenv
import together
from tools import get_weather

load_dotenv()
together.api_key = os.environ.get("TOGETHER_API_KEY")

# Define the schema for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

user_prompt = "What's the weather like in Tokyo?"

print(f"User: {user_prompt}")

# --- Step 1: Call the LLM to decide which tool to use ---
response = together.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1", # A good model for tool use
    messages=[{"role": "user", "content": user_prompt}],
    tools=tools,
    tool_choice="auto",
)

message = response.choices[0].message

# --- Step 2: Execute the tool and get the final response ---
if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    if function_name == "get_weather":
        # Call the actual Python function
        weather_result = get_weather(location=arguments["location"])
        
        # Send the result back to the LLM for a natural language response
        final_response = together.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "user", "content": user_prompt},
                message, # The model's previous turn
                {
                    "role": "tool",
                    "content": weather_result,
                    "tool_call_id": tool_call.id,
                }
            ]
        )
        print(f"Agent: {final_response.choices[0].message.content}")
else:
    # The model decided not to call a function
    print(f"Agent: {message.content}")
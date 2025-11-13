import os
import json
from dotenv import load_dotenv
import openai
from tools import get_weather, get_top_news, get_crypto_price, get_movie_summary

# --- 1. SETUP ---
load_dotenv()

client = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.environ.get("TOGETHER_API_KEY"),
)

available_tools = {
    "get_weather": get_weather,
    "get_top_news": get_top_news,
    "get_crypto_price": get_crypto_price,
    "get_movie_summary": get_movie_summary,
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specified location.",
            "parameters": {
                "type": "object",
                "properties": { "location": { "type": "string", "description": "The city and state, e.g., San Francisco, CA" } },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_news",
            "description": "Get the top news headline for a given country.",
            "parameters": {
                "type": "object",
                "properties": { "country_code": { "type": "string", "description": "The 2-letter ISO 3166-1 alpha-2 code for the country, e.g., 'us' for United States, 'gb' for Great Britain." } },
                "required": ["country_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_crypto_price",
            "description": "Get the current price of a cryptocurrency in USD.",
            "parameters": {
                "type": "object",
                "properties": { "coin_id": { "type": "string", "description": "The ID of the cryptocurrency as per CoinGecko, e.g., 'bitcoin', 'ethereum'." } },
                "required": ["coin_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_movie_summary",
            "description": "Get a brief summary of a movie from its title.",
            "parameters": {
                "type": "object",
                "properties": { "title": { "type": "string", "description": "The full title of the movie." } },
                "required": ["title"],
            },
        },
    }
]

# --- 2. CONVERSATIONAL LOOP ---
print("🤖 Smart Info-Desk is active. Type 'quit' to exit.")

while True:
    user_prompt = input("You: ")
    if user_prompt.lower() in ["quit", "exit"]:
        print("🤖 Goodbye!")
        break

    messages_for_tool_selection = [
        # This prompt is good. We will keep it.
        {"role": "system", "content": "You are an expert function-calling agent. Your sole purpose is to identify the correct tool and its arguments based on the user's query. You must call a tool if one is appropriate. Do not provide conversational chatter or explanations; only generate tool calls."},
        {"role": "user", "content": user_prompt}
    ]

    print("🤖 Thinking...")

    try:
        # STEP 1: Call the model to get the tool and arguments
        first_response = client.chat.completions.create(
            # +++ FIX 1: Use a model fine-tuned for function calling +++
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=messages_for_tool_selection,
            tools=tools_schema,
            # +++ FIX 2: Force the model to use a tool +++
            tool_choice="required",
        )
        message = first_response.choices[0].message

    except Exception as e:
        print(f"An API error occurred during tool selection: {e}")
        continue

    # Proceed only if the model returned a tool call
    if not message.tool_calls:
        # With tool_choice="required", this block should ideally not be reached
        # unless there's an API error or a very confusing query.
        print("Agent: I was unable to select a tool to answer your question.")
        continue

    # STEP 2: Execute the tool
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    
    if function_name not in available_tools:
        print(f"Error: Model tried to call an unknown function '{function_name}'.")
        continue

    function_to_call = available_tools[function_name]
    try:
        arguments = json.loads(tool_call.function.arguments)
        print(f"🤖 Calling tool: {function_name} with arguments: {arguments}")
        tool_output = function_to_call(**arguments)
    except Exception as e:
        print(f"Error executing tool: {e}")
        continue
                
    print("🤖 Synthesizing answer...")

    messages_for_synthesis = [
        {
            "role": "system",
            "content": "You are a helpful assistant. The user asked a question, and I have provided the answer from a tool. Your job is to formulate a friendly, natural language response to the user based on this information."
        },
        {
            "role": "user",
            "content": f"The original question was: '{user_prompt}'\n\nThe information I found is: '{tool_output}'"
        }
    ]

    try:
        # STEP 3: Call the model a second time to synthesize a natural language response
        final_response = client.chat.completions.create(
            # Using the same powerful model for synthesis is fine
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=messages_for_synthesis,
        )
        final_answer = final_response.choices[0].message.content
        print(f"Agent: {final_answer}")

    except Exception as e:
        print(f"An API error occurred during synthesis: {e}")
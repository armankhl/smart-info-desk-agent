import os
import json
from dotenv import load_dotenv
import openai
from tools import get_weather

# --- 1. SETUP ---
load_dotenv()

client = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.environ.get("TOGETHER_API_KEY"),
)

available_tools = {
    "get_weather": get_weather,
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specified location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA",
                    },
                },
                "required": ["location"],
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

    # Stateless messages for the first call
    messages_for_tool_selection = [
        {"role": "system", "content": "You are a function calling agent. Call the appropriate function based on the user's query."},
        {"role": "user", "content": user_prompt}
    ]

    print("🤖 Thinking...")

    try:
        # STEP 1: Call the model to get the tool and arguments
        first_response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=messages_for_tool_selection,
            tools=tools_schema,
            tool_choice="required",
        )
        message = first_response.choices[0].message

    except Exception as e:
        print(f"An API error occurred during tool selection: {e}")
        continue

    # Proceed only if the model returned a tool call
    if not message.tool_calls:
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
                
    # print("4:", message[3]['content'])
    print("🤖 Synthesizing answer...")

    # ======================================================================================
    # THE DEFINITIVE FIX: A completely new, simple message list for the synthesis step.
    # We are no longer continuing the old conversation. We are starting a new, simple one.
    # ======================================================================================
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
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=messages_for_synthesis,
            # No tools needed for this call
        )
        final_answer = final_response.choices[0].message.content
        print(f"Agent: {final_answer}")

    except Exception as e:
        print(f"An API error occurred during synthesis: {e}")
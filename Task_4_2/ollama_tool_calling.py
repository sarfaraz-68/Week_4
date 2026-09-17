import ollama
from datetime import datetime
from zoneinfo import ZoneInfo


def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid mathematical expression."


def get_current_time(timezone):
    try:
        current_time = datetime.now(ZoneInfo(timezone))
        return current_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "Invalid timezone."


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression such as 4892*17"
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time for a specific timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "An IANA timezone such as Asia/Tokyo or Asia/Karachi"
                    }
                },
                "required": ["timezone"],
            },
        },
    },
]


question = input("Enter your question: ")

messages = [
    {
        "role": "user",
        "content": question
    }
]


response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=tools,
)

messages.append(response["message"])


if response["message"].tool_calls:

    for tool_call in response["message"].tool_calls:

        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        print(f"\nTool requested: {tool_name}")
        print(f"Arguments: {arguments}")

        if tool_name == "calculator":
            result = calculator(arguments["expression"])

        elif tool_name == "get_current_time":
            result = get_current_time(arguments["timezone"])

        else:
            result = "Unknown tool."

        print(f"Tool result: {result}")

        messages.append(
            {
                "role": "tool",
                "content": result,
            }
        )

    final_response = ollama.chat(
        model="llama3.2",
        messages=messages,
        tools=tools,
    )

    print("\nFinal LLM Response:")
    print(final_response["message"]["content"])

else:
    print("\nNo tool required.")
    print("LLM Response:")
    print(response["message"]["content"])
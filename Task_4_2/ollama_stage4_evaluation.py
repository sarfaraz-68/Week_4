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
            "description": "Use this ONLY when the user asks you to perform a mathematical calculation. Do NOT use it for general questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
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
            "description": "Use this ONLY when the user explicitly asks for the current time or what time it is in a specific location. NEVER use this tool for general knowledge, history, science, people, places, or other questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The IANA timezone requested by the user, such as Asia/Tokyo, Asia/Karachi, or Europe/London."
                    }
                },
                "required": ["timezone"],
            },
        },
    },
]


system_message = (
    "You are a helpful assistant. "
    "Use tools only when they are genuinely required. "
    "Use calculator only for mathematical calculations. "
    "Use get_current_time only when the user asks for the current time. "
    "For general knowledge questions, history, science, people, "
    "places, or explanations, answer directly without using any tool."
)


tests = [
    ("What is 4892 * 17?", "calculator"),
    ("What is 125 + 875?", "calculator"),
    ("Calculate 72 divided by 8.", "calculator"),
    ("What time is it in Tokyo?", "get_current_time"),
    ("What time is it in Karachi?", "get_current_time"),
    ("Tell me the current time in London.", "get_current_time"),
    ("Who wrote Hamlet?", "none"),
    ("What is the capital of France?", "none"),
    ("Who was Albert Einstein?", "none"),
    ("Explain photosynthesis in one sentence.", "none"),
]


correct = 0


for number, (question, expected) in enumerate(tests, 1):

    messages = [
        {
            "role": "system",
            "content": system_message
        },
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

    tool_used = "none"

    if response["message"].tool_calls:

        tool_call = response["message"].tool_calls[0]
        tool_used = tool_call.function.name
        arguments = tool_call.function.arguments

        if tool_used == "calculator":
            result = calculator(arguments["expression"])

        elif tool_used == "get_current_time":
            result = get_current_time(arguments["timezone"])

        else:
            result = "Unknown tool."

        messages.append(response["message"])

        messages.append(
            {
                "role": "tool",
                "content": result
            }
        )

        ollama.chat(
            model="llama3.2",
            messages=messages,
            tools=tools,
        )

    is_correct = tool_used == expected

    if is_correct:
        correct += 1

    print(f"{number}. {question}")
    print(f"   Expected: {expected}")
    print(f"   Actual:   {tool_used}")
    print(f"   Result:   {'CORRECT' if is_correct else 'WRONG'}")
    print()


accuracy = correct / len(tests) * 100

print("=" * 40)
print(f"Correct: {correct}/{len(tests)}")
print(f"Accuracy: {accuracy:.1f}%")
print("=" * 40)
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """
You are a friendly and helpful AI assistant.

Keep a consistent friendly personality.

Remember useful information the user provides during the conversation.

If the user tells you their name, what they are learning,
their interests, or other useful personal information,
remember it and use it correctly in later responses.

Use previous conversation messages when answering questions.

Answer clearly and briefly unless the user asks for more detail.
"""

messages = [
    {
        "role": "user",
        "parts": [
            {
                "text": SYSTEM_PROMPT
            }
        ]
    }
]

TEST_MODE = True

TEST_MESSAGES = [
    "My name is Sarfaraz. I am learning Python. I am working on Week 4 of my AI course.",
    "What is my name?",
    "What programming language am I learning?",
    "What week am I working on?",
    "What have I told you about myself?",
    "My favorite programming topic is AI and automation.",
    "What are the things you remember about me?",
    "Please summarize everything you remember about me from this conversation."
]


def trim_conversation():
    max_messages = 21

    if len(messages) > max_messages:
        system_message = messages[0]
        recent_messages = messages[-20:]

        messages.clear()
        messages.append(system_message)
        messages.extend(recent_messages)


def ask_gemini(user_message):
    messages.append(
        {
            "role": "user",
            "parts": [
                {
                    "text": user_message
                }
            ]
        }
    )

    trim_conversation()

    response = client.models.generate_content(
        model=MODEL,
        contents=messages
    )

    answer = response.text

    messages.append(
        {
            "role": "model",
            "parts": [
                {
                    "text": answer
                }
            ]
        }
    )

    return answer


print("--- STAGE 5: MULTI-TURN CHATBOT ---")

if TEST_MODE:
    print("Running combined memory test.")
    print()

    for number, test_message in enumerate(
        TEST_MESSAGES,
        start=1
    ):
        print(f"Turn {number}")
        print("You:", test_message)

        try:
            answer = ask_gemini(test_message)
            print("Chatbot:", answer)

        except Exception as error:
            print("ERROR:", error)

        print("-" * 60)

else:
    print("Type 'quit' to exit.")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                print("Please enter a message.")
                continue

            if user_input.lower() in {
                "quit",
                "exit"
            }:
                print("Chatbot: Goodbye!")
                break

            answer = ask_gemini(user_input)

            print("Chatbot:", answer)
            print()

        except KeyboardInterrupt:
            print("\nChatbot: Goodbye!")
            break

        except Exception as error:
            print("ERROR:", error)
            print()
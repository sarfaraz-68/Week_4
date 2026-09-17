import ollama


model = "llama3.2"

system_message = {
    "role": "system",
    "content": (
        "You are a friendly and helpful AI assistant. "
        "Remember information the user shares during the conversation. "
        "Answer clearly and simply. "
        "Stay friendly and consistent throughout the conversation."
    )
}

messages = [system_message]

max_messages = 12


print("Ollama Memory Chatbot")
print("-" * 40)
print("Type 'quit' or 'exit' to end the conversation.")
print()


while True:

    user_input = input("You: ").strip()

    if not user_input:
        print("Please enter a message.")
        continue

    if user_input.lower() in ["quit", "exit"]:
        print("Assistant: Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:

        if len(messages) > max_messages:
            messages = [system_message] + messages[-(max_messages - 1):]

        response = ollama.chat(
            model=model,
            messages=messages
        )

        assistant_message = response["message"]["content"]

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )

        print(f"Assistant: {assistant_message}")
        print()

    except Exception as e:
        print(f"Error: {e}")
import ollama

print("Ollama LLM Demo")
print("-" * 30)

prompt = input("Enter your question: ")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI tutor. Explain concepts simply for beginners."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nLLM Response:")
print(response["message"]["content"])
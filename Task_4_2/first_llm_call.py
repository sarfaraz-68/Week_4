import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant. Answer in simple English.",
        temperature=0.2,
    ),
    contents="Explain artificial intelligence in two simple sentences.",
)

print(response.text)
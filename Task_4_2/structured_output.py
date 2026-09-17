import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"


class TicketResult(BaseModel):
    category: str
    priority: str
    summary: str
    sentiment: str


class TicketResults(BaseModel):
    results: List[TicketResult]


tickets = [
    "I was charged twice for my subscription.",
    "The app crashes when uploading a photo.",
    "I forgot my password and cannot log into my account.",
    "I want a refund for my recent payment.",
    "The website shows an error when I try to open my dashboard.",
    "Please help me change the email address on my account.",
    "Why was I charged an extra $20 this month?",
    "The login page keeps showing a technical error.",
    "I need to update my account profile information.",
    "My payment was declined even though I have enough money.",
    "I was charged for a cancelled subscription.",
    "The mobile application freezes when I open it.",
    "I cannot remember my account password.",
    "I need to update my billing information.",
    "The website is displaying a server error.",
    "How can I change my account email?",
    "There is an unrecognized charge on my statement.",
    "The app will not open after the latest update.",
    "I want to change my profile name.",
    "My refund has not appeared in my account."
]


prompt = """
Analyze the support tickets below.

For every ticket return:

category:
Billing, Technical, or Account

priority:
Low, Medium, or High

summary:
A short summary of the problem.

sentiment:
Positive, Neutral, or Negative.

Return one structured result for every ticket.
Do not skip any ticket.

Tickets:
"""

for number, ticket in enumerate(tickets, start=1):
    prompt += f"{number}. {ticket}\n"


print("\n--- STAGE 3: STRUCTURED OUTPUT ---\n")


try:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=TicketResults
        )
    )

    parsed = response.parsed

    if parsed is None:
        raise ValueError("The model did not return structured data.")

    for number, result in enumerate(
        parsed.results,
        start=1
    ):
        print(f"Ticket {number}")
        print(f"Category: {result.category}")
        print(f"Priority: {result.priority}")
        print(f"Summary: {result.summary}")
        print(f"Sentiment: {result.sentiment}")
        print("-" * 40)

    total_results = len(parsed.results)

    print(f"\nTotal results: {total_results}")
    print(f"Valid schema results: {total_results}")
    print(f"Expected results: {len(tickets)}")

    if total_results == len(tickets):
        print("Stage 3 validation target: PASSED")
    else:
        print("Stage 3 validation target: NOT PASSED")

except Exception as error:
    print("ERROR:", error)
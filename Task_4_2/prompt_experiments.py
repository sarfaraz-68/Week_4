import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

test_inputs = [
    "I was charged twice for my subscription.",
    "The app crashes whenever I try to upload a photo.",
    "I forgot my password and cannot log into my account.",
    "I want a refund for my recent payment.",
    "The website shows an error when I try to open my dashboard.",
    "Please help me change the email address on my account.",
    "Why was I charged an extra $20 this month?",
    "The login page keeps showing a technical error.",
    "I need to update my account profile information.",
    "My payment was declined even though I have enough money."
]

labels = [
    "Billing",
    "Technical",
    "Account"
]

def call_model(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0
        )
    )

    return response.text


prompt_version_1 = """
Classify each support ticket into exactly one of these categories:

Billing
Technical
Account

Return only the category for each ticket.

Tickets:
"""

for number, ticket in enumerate(test_inputs, start=1):
    prompt_version_1 += f"{number}. {ticket}\n"

print("\n--- PROMPT VERSION 1 ---\n")

try:
    result = call_model(prompt_version_1)
    print(result)
except Exception as error:
    print("ERROR:", error)


few_shot_examples = """
Example 1:
Ticket: I was charged twice for my subscription.
Category: Billing

Example 2:
Ticket: The app crashes when I upload a photo.
Category: Technical

Example 3:
Ticket: I forgot my password.
Category: Account
"""

prompt_version_3 = f"""
You are a support ticket classification system.

Classify each ticket into exactly one category:

Billing
Technical
Account

{few_shot_examples}

Now classify these tickets.

Return only the category for each ticket, numbered 1 to 10.

"""

for number, ticket in enumerate(test_inputs, start=1):
    prompt_version_3 += f"{number}. {ticket}\n"

print("\n--- PROMPT VERSION 3: FEW-SHOT ---\n")

try:
    result = call_model(prompt_version_3)
    print(result)
except Exception as error:
    print("ERROR:", error)


prompt_version_4 = """
You are an expert customer-support ticket classifier.

Your job is to classify every ticket into exactly one
of these three categories:

Billing
Technical
Account

Rules:

Billing:
Use Billing for payments, charges, refunds,
subscriptions, and billing information.

Technical:
Use Technical for application errors, crashes,
website problems, server errors, and technical issues.

Account:
Use Account for passwords, profile information,
email changes, and account-management requests.

Return only the category names.
Do not explain your answers.
Number the answers from 1 to 10.

Tickets:
"""

for number, ticket in enumerate(test_inputs, start=1):
    prompt_version_4 += f"{number}. {ticket}\n"

print("\n--- PROMPT VERSION 4: ROLE / SYSTEM ---\n")

try:
    result = call_model(prompt_version_4)
    print(result)
except Exception as error:
    print("ERROR:", error)


prompt_version_5 = """
Classify the following support tickets.

For every ticket:

1. Identify the main problem.
2. Decide whether it is Billing, Technical, or Account.
3. Return only the final category.
4. Keep the original ticket order.
5. Number the results from 1 to 10.

Categories:

Billing
Technical
Account

Tickets:
"""

for number, ticket in enumerate(test_inputs, start=1):
    prompt_version_5 += f"{number}. {ticket}\n"

print("\n--- PROMPT VERSION 5: STEP-BY-STEP ---\n")

try:
    result = call_model(prompt_version_5)
    print(result)
except Exception as error:
    print("ERROR:", error)
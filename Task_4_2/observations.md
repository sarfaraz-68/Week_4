Week 4 — Task 4.2 Observations
Overview

In Week 4 Task 4.2, I worked with Large Language Models (LLMs) and learned how to connect Python applications with LLMs.

I implemented the task using two different approaches:

Ollama — for running an LLM locally.
Google Gemini API — for using a cloud-based LLM through an API.

I kept the Ollama and Gemini implementations in separate Python files so that both approaches could be tested independently.

The task was completed progressively through five stages:

Stage 1 — First LLM Call
Stage 2 — Prompt Engineering
Stage 3 — Structured Output
Stage 4 — Tool Calling
Stage 5 — Multi-Turn Chatbot

1. Environment Setup

A Python virtual environment was used for the project.

The main packages used during the work included:

python-dotenv
google-genai
pydantic

For Gemini, the API key was stored inside a .env file instead of writing it directly inside the Python code.

A .gitignore file was also created so that the .env file containing the API key would not accidentally be committed.

This taught me an important practice:

API keys and other secrets should not be hard-coded inside source code.

2. Ollama Implementation
Purpose

Ollama was used to understand how an LLM can be run locally instead of depending completely on a cloud API.

The Ollama implementation was kept separately from the Gemini implementation.

The basic workflow was:

Python program
      ↓
   Ollama
      ↓
  Local LLM
      ↓
Generated response

This approach is useful because the model can run locally and does not require a cloud API request for every response.

What I learned

With Ollama, I learned the basic structure of communicating with a locally running LLM.

I also learned that different models can be used through Ollama while keeping the Python application structure relatively similar.

3. Gemini Implementation
Purpose

Gemini was used as the cloud/API-based implementation of the same LLM concepts.

The Gemini API key was loaded from .env.

The basic workflow was:

Python program
      ↓
Gemini API
      ↓
Gemini model
      ↓
Generated response

The Gemini implementation was kept in separate Python files from the Ollama implementation.

API and Model Issues

Initially, I experimented with the OpenAI API, but the available API credits were exhausted.

Because of this, I shifted the implementation to Gemini.

During development, some Gemini model names were unavailable for the account, so the model name had to be updated.

The working model used in the final Gemini code was:

gemini-3.6-flash

I also encountered Gemini free-tier quota limits during testing.

This showed that API-based LLM development can be affected by:

API credits
request limits
model availability
free-tier quotas
Stage 1 — First LLM Call
Goal

The goal of Stage 1 was to make the first successful LLM request from Python and understand the basic request-response process.

Ollama

I created a separate Ollama implementation that sends a prompt to a locally running model and prints the generated response.

Gemini

I also created a separate Gemini implementation.

The Gemini program:

Loads the API key.
Creates the Gemini client.
Sends a prompt.
Receives the model response.
Prints the response.

A successful test produced a simple explanation of Artificial Intelligence.

What I learned

An LLM API call basically follows:

Prompt → Model → Response

The Python program acts as the connection between the user/application and the model.

Stage 2 — Prompt Engineering
Goal

The goal of Stage 2 was to understand how changing the prompt can change the quality and consistency of an LLM's output.

The same test inputs were used for different prompt versions so that the results could be compared.

Experiment 1 — Sentiment Classification

The model was asked to classify text into:

Positive
Negative
Neutral

The test examples included:

"I love this product!"
"This is terrible."
"The movie was amazing."
"I hate this service."
"The food was okay."
"I am very happy with my purchase."
"This is the worst experience."
"The phone works perfectly."
"I am disappointed."
"It was fine, nothing special."

The expected classifications were produced successfully.

Prompt Version 1

A basic classification instruction was used.

The model was able to classify the examples correctly.

Prompt Version 2

The prompt was improved by explicitly requesting a simple numbered output.

The output became easier to read and evaluate.

Prompt Version 3 — Few-Shot Prompting

Examples were provided to the model before the actual test inputs.

This demonstrated few-shot prompting.

The model again produced the expected classifications.

Prompt Version 4 — Role/System Prompt

A system/role instruction was added to tell the model what type of assistant it should behave as.

The expected classifications were produced.

Prompt Version 5 — Step-by-Step Instructions

The model was given clearer step-by-step instructions about how to perform the classification and format the answer.

The expected classifications were again produced.

Experiment 2 — Support Ticket Classification

A second classification task was created using three categories:

Billing
Technical
Account

Ten support tickets were tested.

The results were:

1. Billing
2. Technical
3. Account
4. Billing
5. Technical
6. Account
7. Billing
8. Technical
9. Account
10. Billing
What I learned

Prompt engineering is not just asking the model a question.

The prompt can control:

the model's role
the required output
examples
reasoning instructions
formatting
consistency

The experiments showed that clearer prompts generally make outputs easier to control and evaluate.

Stage 3 — Structured Output
Goal

The goal of Stage 3 was to make the LLM return information in a predefined structure instead of returning uncontrolled text.

Pydantic was used for schema validation.

Output Structure

Each support ticket contained:

Category
Priority
Summary
Sentiment
Test Dataset

20 support tickets were processed.

Examples included:

Ticket 1

Category: Billing

Priority: High

Summary: Customer was charged twice for subscription.

Sentiment: Negative

Ticket 2

Category: Technical

Priority: Medium

Summary: App crashes when uploading a photo.

Sentiment: Negative

Ticket 3

Category: Account

Priority: Medium

Summary: Forgotten password preventing account login.

Sentiment: Negative

Ticket 10

Category: Billing

Priority: High

Summary: Payment declined despite sufficient funds.

Sentiment: Negative

Validation

The final validation showed:

Total results: 20
Valid schema results: 20
Expected results: 20
Stage 3 validation target: PASSED

Therefore, all 20 generated results matched the required structure.

What I learned

Structured output is useful when an application needs predictable data from an LLM.

Instead of relying on normal text formatting, a schema can define exactly what information the application expects.

Pydantic then provides an additional validation layer.

Stage 4 — Tool Calling
Goal

Stage 4 introduced tools that the LLM can request when it needs external functionality.

Two tools were implemented:

Calculator
Current-time tool
Calculator Tool

The calculator accepts a mathematical expression and evaluates it safely using Python's AST-based approach.

Examples include:

4892 * 17
125 * 64
9876 - 4321
15% of 240
Current Time Tool

The second tool accepts a timezone and returns the current time for that timezone.

Examples include:

Tokyo
London
New York
Important Concept

The model does not directly execute Python code.

The process is:

User question
      ↓
LLM decides whether a tool is needed
      ↓
Tool is selected
      ↓
Python executes the tool
      ↓
Tool result
      ↓
LLM gives final response
Tool Abstention

The evaluation also included questions where no tool should be used.

Examples:

Who wrote Hamlet?
What is the capital of France?
Explain photosynthesis briefly.

This is important because a good tool-calling system should not use a tool unnecessarily.

Evaluation

Ten evaluation queries were prepared.

The expected behavior included:

calculator for mathematical questions
time tool for timezone questions
no tool for general knowledge questions

The target was at least 9 correct decisions out of 10.

Current Status

The Stage 4 code and evaluation are prepared.

The final successful evaluation run is pending because the Gemini free-tier quota was exhausted during development.

Once quota becomes available, the evaluation can be run without changing the overall design.

Stage 5 — Multi-Turn Chatbot
Goal

Stage 5 was designed to build a chatbot that can maintain conversation history and remember information from earlier messages.

The chatbot was given a system instruction defining its personality and memory behavior.

Conversation Memory

The chatbot stores previous messages and sends the conversation history along with new messages.

The basic idea is:

User message
      ↓
Conversation history
      ↓
     LLM
      ↓
   Response
      ↓
Add response to history
    Memory Test

The prepared test conversation starts with:

My name is Sarfaraz. I am learning Python.
I am working on Week 4 of my AI course.

Later questions test whether the chatbot remembers:

my name
the programming language
the week being studied
previously provided information
a favorite programming topic

The chatbot is also asked to summarize everything it remembers.

Conversation Management

The implementation includes conversation trimming so that the message history does not continue growing indefinitely.

The chatbot also handles:

empty input
quit
exit
normal conversation
errors
Current Status

The Stage 5 implementation is prepared.

The final multi-turn test is pending because of the Gemini quota limitation.

The code itself is ready to be tested once the quota becomes available.

Ollama vs Gemini

Both approaches were useful because they demonstrate two different ways of working with LLMs.

| Feature                           | Ollama         | Gemini |
| --------------------------------- | -------------- | ------ |
| Runs locally                      | Yes            | No     |
| Cloud API required                | No             | Yes    |
| API key required                  | No             | Yes    |
| Internet required for generation  | No             | Yes    |
| Free-tier API quota               | No cloud quota | Yes    |
| Useful for learning LLM basics    | Yes            | Yes    |
| Useful for API-based applications | Limited        | Yes    |
| Model hosted locally              | Yes            | No     |


Ollama allowed me to experiment with an LLM locally.

Gemini allowed me to learn how a Python application communicates with a cloud-hosted LLM through an API.

Using both gave me a better understanding of the difference between local LLM inference and cloud API-based LLM inference.

Problems Encountered and Solutions
OpenAI API Credit Error

The OpenAI API initially returned an insufficient-quota error.

Solution

I moved the implementation to Gemini because I wanted to continue the task without purchasing OpenAI API credits.

Gemini Model Not Found

Some Gemini model names returned a 404 NOT_FOUND error because the model was unavailable for the account.

Solution

The model name was updated to the available Gemini model.

Gemini Quota Exceeded

During repeated testing, the Gemini free-tier request quota was reached.

The API returned a 429 RESOURCE_EXHAUSTED error.

Solution

The remaining Stage 4 and Stage 5 validation runs were postponed until the quota becomes available again.

Overall Learning

Week 4 Task 4.2 helped me understand the progression from a simple LLM call to a more complete LLM application.

The progression was:

Basic LLM Call
      ↓
Prompt Engineering
      ↓
Structured Output
      ↓
Tool Calling
      ↓
Multi-Turn Chatbot


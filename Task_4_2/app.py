from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

GEMINI_MODEL = "gemini-3.5-flash-lite"

conversation = []


def ask_gemini(message):
    conversation.append({
        "role": "user",
        "text": message
    })

    history = "\n".join(
        f"{item['role']}: {item['text']}"
        for item in conversation
    )

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=history
    )

    answer = response.text

    conversation.append({
        "role": "assistant",
        "text": answer
    })

    return answer


def ask_ollama(message):
    conversation.append({
        "role": "user",
        "text": message
    })

    messages = [
        {
            "role": "user" if item["role"] == "user" else "assistant",
            "content": item["text"]
        }
        for item in conversation
    ]

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    answer = data["message"]["content"]

    conversation.append({
        "role": "assistant",
        "text": answer
    })

    return answer


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    message = data.get("message", "")
    model = data.get("model", "gemini")

    if not message:
        return jsonify({
            "error": "Please enter a message."
        }), 400

    try:
        if model == "ollama":
            answer = ask_ollama(message)
        else:
            answer = ask_gemini(message)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/clear", methods=["POST"])
def clear_chat():
    conversation.clear()

    return jsonify({
        "message": "Chat cleared."
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
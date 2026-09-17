import os
import ast
import operator
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

tool_log = []


def calculate(expression: str) -> str:
    tool_log.append("calculator")

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)

            operation = operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(value)

        raise ValueError("Invalid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except Exception as error:
        return f"Calculation error: {error}"


def get_current_time(timezone: str) -> str:
    tool_log.append("get_current_time")

    try:
        current_time = datetime.now(
            ZoneInfo(timezone)
        )

        return current_time.strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )

    except Exception as error:
        return f"Time error: {error}"


tools = [
    calculate,
    get_current_time
]


def ask_gemini(question: str):
    global tool_log

    tool_log = []

    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            temperature=0,
            tools=tools,
            system_instruction=(
                "You are a helpful assistant. "
                "Use the calculator tool for arithmetic questions. "
                "Use the get_current_time tool for current time questions. "
                "Do not use tools for questions that do not require them."
            )
        )
    )

    response = chat.send_message(question)

    return response.text, list(tool_log)


evaluation_queries = [
    {
        "query": "What is 4892 * 17?",
        "expected_tool": "calculator"
    },
    {
        "query": "What is 125 * 64?",
        "expected_tool": "calculator"
    },
    {
        "query": "What is 9876 - 4321?",
        "expected_tool": "calculator"
    },
    {
        "query": "What time is it in Tokyo?",
        "expected_tool": "get_current_time"
    },
    {
        "query": "What time is it in London?",
        "expected_tool": "get_current_time"
    },
    {
        "query": "What time is it in New York?",
        "expected_tool": "get_current_time"
    },
    {
        "query": "Who wrote Hamlet?",
        "expected_tool": None
    },
    {
        "query": "What is the capital of France?",
        "expected_tool": None
    },
    {
        "query": "Explain photosynthesis briefly.",
        "expected_tool": None
    },
    {
        "query": "What is 15% of 240?",
        "expected_tool": "calculator"
    }
]


def evaluate():
    results = []
    correct = 0

    print("\n--- STAGE 4: TOOL CALLING EVALUATION ---\n")

    for number, item in enumerate(
        evaluation_queries,
        start=1
    ):
        query = item["query"]
        expected_tool = item["expected_tool"]

        print(f"Query {number}: {query}")
        print(
            f"Expected tool: "
            f"{expected_tool or 'No tool'}"
        )

        try:
            answer, used_tools = ask_gemini(query)

            actual_tool = (
                used_tools[0]
                if used_tools
                else None
            )

            passed = actual_tool == expected_tool

            if passed:
                correct += 1

            result = {
                "query_number": number,
                "query": query,
                "expected_tool": expected_tool,
                "actual_tool": actual_tool,
                "used_tools": used_tools,
                "passed": passed,
                "answer": answer
            }

            results.append(result)

            print(
                f"Actual tool: "
                f"{actual_tool or 'No tool'}"
            )

            print(
                f"Result: "
                f"{'PASS' if passed else 'FAIL'}"
            )

            print(f"Answer: {answer}")

        except Exception as error:
            result = {
                "query_number": number,
                "query": query,
                "expected_tool": expected_tool,
                "actual_tool": None,
                "used_tools": [],
                "passed": False,
                "answer": "",
                "error": str(error)
            }

            results.append(result)

            print(f"ERROR: {error}")

        print("-" * 60)

    total = len(evaluation_queries)

    score = (correct / total) * 100

    print("\n--- STAGE 4 EVALUATION REPORT ---")
    print(f"Total queries: {total}")
    print(f"Correct tool decisions: {correct}")
    print(f"Score: {score:.1f}%")

    if score >= 90:
        print("Stage 4 validation target: PASSED")
    else:
        print("Stage 4 validation target: NOT PASSED")

    return results


if __name__ == "__main__":
    print("\n--- STAGE 4: TOOL CALLING ---")
    print("Evaluation is starting.")
    print("")

    evaluate()
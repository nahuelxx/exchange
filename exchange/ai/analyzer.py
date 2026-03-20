import json
from .claude_client import ask_claude
from .prompts import build_financial_prompt

def analyze_exchange_data(data, question):

    prompt = build_financial_prompt(
        json.dumps(data, indent=2),
        question
    )

    result = ask_claude(prompt)

    return result
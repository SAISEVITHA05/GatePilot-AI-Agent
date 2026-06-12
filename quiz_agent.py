from groq_client import ask_groq
import json


def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


def generate_quiz(topic):

    prompt = f"""
Create a GATE DA quiz on {topic}.

Return ONLY valid JSON, with no extra text, no markdown formatting, and no code fences.

Format:

[
  {{
    "question":"...",
    "options":["option text 1","option text 2","option text 3","option text 4"],
    "answer":"option text that is correct (must exactly match one of the items in options)",
    "explanation":"..."
  }}
]

Rules:
- Generate exactly 10 MCQs.
- 4 options each.
- "answer" must be the exact text of the correct option, not a letter like A/B/C/D.
- Include explanation.
- GATE DA difficulty.
- Avoid very basic questions.
- Include at least one previous-year style question.
"""

    response = ask_groq(prompt)

    return json.loads(clean_json(response))
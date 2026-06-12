import json
from groq_client import ask_groq


def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


def generate_formulas_for_topic(topic):
    prompt = f"""
You are GatePilot AI, a GATE DA mentor.

Give a COMPLETE formula sheet for the topic: {topic}

Cover ALL important formulas, theorems, and identities related to this topic
that are relevant for GATE Data Science & AI exam preparation.
Base this on standard GATE DA reference textbooks and standard syllabus coverage
for this topic — be thorough, not selective.

Return ONLY valid JSON, no markdown, no code fences, in this exact format:

[
  {{"name": "Formula name", "formula": "LaTeX formula here", "note": "short 1-line note on when/why to use it"}}
]

Rules:
- Write each "formula" in proper LaTeX syntax (e.g. \\\\frac{{a}}{{b}}, \\\\sum_{{i=1}}^{{n}}, \\\\sqrt{{x}}, P(A|B), \\\\sigma, \\\\mu).
- Do NOT wrap formulas in $ or $$ — just the raw LaTeX.
- Include every formula a student would need for this topic, not just a few examples.
- Group related formulas together in the order they appear (basic to advanced).
- "note" should be brief (max 15 words) — what it's used for or a key condition.
"""

    response = ask_groq(prompt)
    return json.loads(clean_json(response))
import json
from groq_client import ask_groq

with open("syllabus.json", "r") as f:
    syllabus = json.load(f)


def generate_plan(score, days):

    prompt = f"""
You are a GATE DA mentor.

Target Score: {score}
Days Left: {days}

Use ONLY the following syllabus:

{json.dumps(syllabus, indent=2)}

Rules:
1. Do NOT include any subject outside this syllabus.
2. Prioritize high-weightage topics.
3. Create a WEEKLY study timetable (group into weeks, not day-by-day).
4. Include revision weeks and mock test weeks.
5. Explain briefly why each subject matters for GATE DA.
6. Use simple English.
7. Give output as a markdown table.

Keep the response concise enough to not get cut off.
"""

    return ask_groq(prompt)
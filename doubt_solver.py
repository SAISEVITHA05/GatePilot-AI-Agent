from gemini_client import ask_gemini
from groq_client import ask_groq

def explain_topic(topic, history):

    conversation = ""

    for item in history:

        conversation += (
            f"User: {item['user']}\n"
            f"Assistant: {item['assistant']}\n\n"
        )

    prompt = f"""
You are GatePilot AI, a GATE DA mentor.

Previous Conversation:

{conversation}

Current Question:

{topic}

Instructions:
1. If the current question refers to previous discussion
   (e.g. "give example", "explain more", "why?")
   use the conversation history.

2. Explain for a GATE DA student in simple English.

3. Format your ENTIRE response as raw HTML using EXACTLY this structure
   (no markdown, no ```html fences, no extra text outside these tags):

<span class="gp-concept-label">Definition</span>
<p>...definition here...</p>

<span class="gp-concept-label">Simple Explanation</span>
<p>...explanation here...</p>

<span class="gp-concept-label">Example</span>
<p>...example here...</p>

<span class="gp-concept-label">GATE DA Relevance</span>
<p>...relevance here...</p>

<span class="gp-concept-label">Practice Questions</span>
<p>...1-2 practice questions here...</p>

Do not include any text before the first <span> or after the last </p>.
"""

    try:
        return ask_gemini(prompt)

    except Exception:

        return ask_groq(prompt)
    

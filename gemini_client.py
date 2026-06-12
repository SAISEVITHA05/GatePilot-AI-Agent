import google.generativeai as genai

genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt):

    response = model.generate_content(prompt)

    return response.text
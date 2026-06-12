# 🌌 GatePilot AI

> Your personal AI mentor for cracking GATE Data Science & Artificial Intelligence

GatePilot AI isn't just another quiz app — it's an intelligent study companion that adapts to *you*. Built with a futuristic dark-themed interface inspired by OpenAI, Perplexity, and Apple Vision Pro, it feels like having a dedicated mentor guiding your GATE DA prep, one focused session at a time.

---

## ✨ Features

### 📅 Personalized Study Plan Generator
Enter your target score and days remaining — GatePilot AI builds a custom week-by-week roadmap covering the official GATE DA syllabus, prioritized by topic weightage.

### 🧠 Adaptive Quiz Generator
Real exam-style MCQs generated on the fly for any topic. One question at a time, with detailed explanations and a review section showing exactly where you went right or wrong.

### 💬 AI Doubt Solver
A conversational tutor that remembers your previous questions. Every explanation follows a structured format:
- **Definition**
- **Simple Explanation**
- **Example**
- **GATE Relevance**
- **Practice Questions**

### 📊 Performance Dashboard
Visual score trends and topic-wise performance — track your growth over time with animated charts, and instantly see your strong and weak areas.

### 📐 AI-Generated Formula Sheet
Request a complete, exam-ready formula sheet for any topic — rendered in proper LaTeX with quick-use notes for each formula.

---

## 🎨 Design

- **Dark mode only** — deep navy background with sky-blue accents and slowly twinkling gold stars
- **Glassmorphism cards** with soft glowing hover effects
- Smooth animations throughout, designed to keep students focused and motivated

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend/UI | Streamlit + Custom CSS |
| AI Models | Groq (Llama 3.3 70B) + Gemini 2.5 Flash |
| Visualizations | Plotly |
| Data | JSON-based syllabus & score tracking |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gatepilot-ai.git
cd gatepilot-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API keys

Create `groq_client.py`:

```python
from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

Create `gemini_client.py`:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
```

> Get your free API keys from [Groq Console](https://console.groq.com) and [Google AI Studio](https://aistudio.google.com)

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📂 Project Structure
---

## 💡 Vision

> "I have my own intelligent AI mentor helping me crack GATE DA."

That's the feeling GatePilot AI is built to deliver — a premium, futuristic, and genuinely helpful study experience for serious aspirants.

---

## 📜 License

This project is open source and available for educational use.
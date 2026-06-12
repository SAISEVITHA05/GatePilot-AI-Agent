import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.write("Groq Secret Exists:",
         "GROQ_API_KEY" in st.secrets)

from study_plan import generate_plan
from quiz_agent import generate_quiz
from doubt_solver import explain_topic
from formula_sheet import generate_formulas_for_topic

def clean_html(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("GatePilot AI")
st.subheader("Your Personal GATE DA Mentor")

st.markdown(
    '<div class="gp-focus-banner">'
    '<span class="gp-spark">✦</span> '
    '<b>AI Tip:</b> Consistency beats intensity — '
    'show up for one focused session today. '
    '<span class="gp-spark">✦</span>'
    '</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Study Plan", "Quiz Generator", "Doubt Solver", "Dashboard", "Formula Sheet"]
)
# ==========================
# STUDY PLAN
# ==========================
with tab1:

    score = st.number_input("Target Score", min_value=1, max_value=100, value=60)
    days = st.number_input("Days Left", min_value=1, max_value=365, value=180)

    if st.button("Generate Study Plan"):
        plan = generate_plan(score, days)
        st.session_state.study_plan = plan

    if "study_plan" in st.session_state:
        plan = st.session_state.study_plan
        st.markdown(f'<div class="gp-card">{plan}</div>', unsafe_allow_html=True)

# ==========================
# QUIZ GENERATOR
# ==========================
with tab2:

    quiz_topic = st.text_input("Enter Topic for Quiz")

    if st.button("Generate Quiz"):
        quiz = generate_quiz(quiz_topic)
        st.session_state.quiz = quiz
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.quiz_saved = False
        st.session_state.quiz_topic = quiz_topic

    if "quiz" in st.session_state:

        quiz = st.session_state.quiz
        current = st.session_state.current_question

        st.progress(min(current, len(quiz)) / len(quiz))

        if current < len(quiz):

            q = quiz[current]

            st.markdown(f"""
            <div class="gp-quiz-card">
                <span class="gp-quiz-tag">Question {current + 1} of {len(quiz)}</span>
                <div class="gp-quiz-question">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)

            answer = st.radio(
                "Select your answer",
                q["options"],
                key=f"question_{current}",
                label_visibility="collapsed"
            )

            if st.button("Save & Next", key=f"next_{current}"):
                st.session_state.answers[current] = answer
                st.session_state.current_question += 1
                st.rerun()

        else:
            score = 0

            for i, q in enumerate(quiz):
                user_answer = st.session_state.answers.get(i)
                if user_answer and user_answer == q["answer"]:
                    score += 1

            percentage = round(score * 100 / len(quiz), 2)

            st.markdown(f"""
            <div class="gp-stat-grid">
                <div class="gp-stat-card">
                    <div class="gp-stat-label">Score</div>
                    <div class="gp-stat-value">{score}/{len(quiz)}</div>
                </div>
                <div class="gp-stat-card">
                    <div class="gp-stat-label">Percentage</div>
                    <div class="gp-stat-value">{percentage}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.quiz_saved:
                with open("scores.json", "r") as f:
                    data = json.load(f)

                data.append({
                    "topic": st.session_state.quiz_topic,
                    "score": score,
                    "total": len(quiz)
                })

                with open("scores.json", "w") as f:
                    json.dump(data, f, indent=4)

                st.session_state.quiz_saved = True

            st.subheader("Review & Explanations")

            for i, q in enumerate(quiz):
                user_answer = st.session_state.answers.get(i)
                is_correct = bool(user_answer and user_answer == q["answer"])
                css_class = "gp-correct" if is_correct else "gp-incorrect"

                options_html = ""
                correct_letter = ""
                user_letter = ""

                for idx, opt in enumerate(q["options"]):
                    letter = chr(65 + idx)  # A, B, C, D

                    if opt == q["answer"]:
                        correct_letter = letter
                        opt_class = "gp-pill-strong"
                    elif opt == user_answer:
                        user_letter = letter
                        opt_class = "gp-pill-weak"
                    else:
                        opt_class = ""

                    options_html += f'<span class="gp-pill {opt_class}">{letter}. {opt}</span><br>'

                st.markdown(f"""
                <div class="gp-card">
                    <b>Q{i+1}: {q['question']}</b><br><br>
                    {options_html}<br>
                    Your answer: <i>{(user_letter + ". " + user_answer) if user_answer else "Not answered"}</i><br>
                    Correct answer: <span class="gp-pill gp-pill-strong">{correct_letter}. {q['answer']}</span>
                    <div class="gp-explanation {css_class}">{q['explanation']}</div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("Try Another Quiz"):
                for key in ["quiz", "current_question", "answers", "quiz_saved", "quiz_topic"]:
                    st.session_state.pop(key, None)
                st.rerun()

# ==========================
# DOUBT SOLVER
# ==========================
with tab3:

    st.subheader("Ask GatePilot AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    doubt_topic = st.text_input("Enter Topic")

    if st.button("Explain Topic", key="explain_btn"):
        with st.spinner("GatePilot AI is thinking..."):
            answer = explain_topic(doubt_topic, st.session_state.chat_history)

        st.session_state.chat_history.append({
            "user": doubt_topic,
            "assistant": answer
        })

    for chat in st.session_state.chat_history:
        st.markdown(f'<div class="gp-chat-user">{chat["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="gp-chat-ai">{clean_html(chat["assistant"])}</div>', unsafe_allow_html=True)

# ==========================
# DASHBOARD
# ==========================
with tab4:

    st.header("Performance Dashboard")

    with open("scores.json", "r") as f:
        data = json.load(f)

    if data:

        total_tests = len(data)
        avg = sum(x["score"] / x["total"] * 100 for x in data) / total_tests

        st.markdown(f"""
        <div class="gp-stat-grid">
            <div class="gp-stat-card">
                <div class="gp-stat-label">Tests Taken</div>
                <div class="gp-stat-value">{total_tests}</div>
            </div>
            <div class="gp-stat-card">
                <div class="gp-stat-label">Average %</div>
                <div class="gp-stat-value">{round(avg, 2)}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
          
        topic_stats = {}
        for item in data:
            topic = item["topic"]
            percentage = item["score"] / item["total"] * 100
            topic_stats.setdefault(topic, []).append(percentage)

        topic_average = {
            topic: sum(scores) / len(scores)
            for topic, scores in topic_stats.items()
        }
        # ---- Score Trend Line Chart ----
        st.subheader("Score Trend Over Time")

        attempts = list(range(1, len(data) + 1))
        percentages = [round(x["score"] / x["total"] * 100, 2) for x in data]
        topics_list = [x["topic"] for x in data]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=attempts,
            y=percentages,
            mode="lines+markers",
            line=dict(color="#38BDF8", width=3),
            marker=dict(color="#FBBF24", size=8, line=dict(color="#0B1020", width=1)),
            text=topics_list,
            hovertemplate="Attempt %{x}<br>Topic: %{text}<br>Score: %{y}%<extra></extra>",
        ))

        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e0f2fe"),
            xaxis=dict(title="Attempt #", gridcolor="rgba(125,211,252,0.1)", dtick=1),
            yaxis=dict(title="Score (%)", gridcolor="rgba(125,211,252,0.1)", range=[0, 100]),
            margin=dict(l=40, r=20, t=20, b=40),
            height=350,
            transition=dict(duration=500, easing="cubic-in-out"),
        )

        st.plotly_chart(fig_line, use_container_width=True)

        strong_topics = [t for t, a in topic_average.items() if a >= 70]
        weak_topics = [t for t, a in topic_average.items() if a < 50]

        st.subheader("Strong Topics")
        if strong_topics:
            pills = "".join(f'<span class="gp-pill gp-pill-strong">{t}</span>' for t in strong_topics)
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.write("No strong topics identified yet.")

        # ---- Topic-wise Performance Pie Chart ----
        st.subheader("Topic-wise Performance")

        pie_topics = list(topic_average.keys())
        pie_values = [round(v, 2) for v in topic_average.values()]

        colors = []
        for v in pie_values:
            if v >= 70:
                colors.append("#38BDF8")
            elif v < 50:
                colors.append("#FBBF24")
            else:
                colors.append("#60A5FA")

        fig_pie = go.Figure(data=[go.Pie(
            labels=pie_topics,
            values=pie_values,
            hole=0.45,
            marker=dict(colors=colors, line=dict(color="#0B1020", width=2)),
            textinfo="label+percent",
            textfont=dict(color="#e0f2fe", size=12),
            pull=[0.03] * len(pie_topics),
        )])

        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e0f2fe"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=400,
            showlegend=True,
            legend=dict(font=dict(color="#e0f2fe")),
            transition=dict(duration=500, easing="cubic-in-out"),
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Topics Needing Work")
        if weak_topics:
            pills = "".join(f'<span class="gp-pill gp-pill-weak">{t}</span>' for t in weak_topics)
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.write("No weak topics identified yet.")

        st.subheader("Previous Tests")
        for item in data:
            st.markdown(f"""
            <div class="gp-card">
                📚 <b>{item['topic']}</b> → {item['score']}/{item['total']}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No tests attempted yet.")

# ==========================
# FORMULA SHEET
# ==========================
with tab5:

    st.header("Formula Sheet")

    formula_topic = st.text_input("Enter a topic (e.g. Probability, Linear Algebra, Hypothesis Testing)")

    if st.button("Generate Formula Sheet"):
        with st.spinner("GatePilot AI is preparing your formula sheet..."):
            try:
                formulas = generate_formulas_for_topic(formula_topic)
                st.session_state.formula_sheet = formulas
                st.session_state.formula_topic = formula_topic
            except Exception:
                st.error("Could not generate formulas. Try again or rephrase the topic.")

    if "formula_sheet" in st.session_state:

        st.subheader(f"Formula Sheet — {st.session_state.formula_topic}")

        for f in st.session_state.formula_sheet:
            st.markdown(f'<div class="gp-formula-name">{f["name"]}</div>', unsafe_allow_html=True)
            st.latex(f["formula"])
            if f.get("note"):
                st.markdown(
                    f'<div class="gp-explanation">{f["note"]}</div>',
                    unsafe_allow_html=True
                )

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.header("GatePilot AI")
    st.write("GATE DA Preparation Assistant")


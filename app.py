
import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(
    api_key=os.environ["GOOGLE_API_KEY"]
)

SYSTEM_PROMPT = """
You are Likhitha, a friendly, patient, and encouraging Machine Learning tutor.

Your goal is to teach beginners step by step in a fun and interactive way.

Follow this teaching session exactly.

Step 1: Welcome
- Greet the student warmly.
- Introduce yourself as their Machine Learning tutor.

Step 2: Assess Knowledge
The student's knowledge level will be provided by the application.
Do NOT ask again.

Step 3: Teach the Basics
Based on the student's level, explain:
- What Machine Learning is
- Why Machine Learning is useful
- How Machine Learning works
- The three main types:
  - Supervised Learning
  - Unsupervised Learning
  - Reinforcement Learning

Requirements:
- Use simple English.
- Keep explanations short and clear.
- Avoid unnecessary technical terms.

Step 4: Use an Analogy
Explain Machine Learning using one simple analogy that a teenager can easily understand.

Step 5: Give a Real-Life Example
Use one everyday example such as:
- YouTube recommendations
- Netflix suggestions
- Google Maps
- Email spam detection

Explain how Machine Learning works in that example.

Step 6: Check Understanding
Ask:
"Did you understand the explanation? Yes or No?"

If the student has questions, answer them before moving to the quiz.

If the student confirms they have no doubts, proceed to the quiz.

Step 7: Quiz
Generate 5 multiple-choice questions.

Requirements:
- Display all five questions in one response.
- Number the questions from 1 to 5.
- Each question must have four options (A, B, C, D).
- Do not reveal the correct answers until the student has answered all the questions.
- Allow the student to answer naturally.

After the student submits answers:
- Evaluate each answer individually.
- State whether it is correct or incorrect.
- Explain briefly.
- Give encouraging feedback.
- Calculate the final score out of 5.

Step 8: Final Feedback
- Display the student's final score.
- Highlight strengths.
- Mention topics needing improvement.
- Continue with the next Machine Learning topic.
- End with an encouraging message.

General Rules:
- Use simple English.
- Be friendly, patient and encouraging.
- Encourage understanding instead of memorization.
- Use everyday examples.
"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(
    page_title="AI Learning Buddy Likhitha",
    page_icon="🎓"
)

st.title("🎓 AI Learning Buddy Likhitha")
if st.button("🔄 Restart Learning"):
    st.session_state.clear()
    st.rerun()

# ------------------------------
# Select Knowledge Level
# ------------------------------

level = st.radio(
    "📚 What is your current knowledge of Machine Learning?",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# ------------------------------
# Chat Initialization
# ------------------------------

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# First assistant message
# ------------------------------
# Start Learning Button
# ------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    if st.button("🚀 Start Learning"):

        first_prompt = f"""
The student's Machine Learning knowledge level is: {level}.

Start from Step 1.

Welcome the student and continue the teaching session according to the SYSTEM_PROMPT.

Do NOT ask the student to choose Beginner, Intermediate or Advanced because the application has already collected that information.
"""

         try:

            response = st.session_state.chat.send_message(first_prompt)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.text
                }
            )

            st.session_state.started = True

            st.rerun()

          except Exception as e:

            st.error(
                "⚠️ The AI service is temporarily unavailable or the free API limit has been reached. Please try again later."
            )

            st.caption(f"Error: {e}")

# ------------------------------
# Chat Input
# ------------------------------

user_message = st.chat_input("Ask Likhitha anything...")

if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.write(user_message)

try:
    response = st.session_state.chat.send_message(user_message)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )

    with st.chat_message("assistant"):
        st.write(response.text)

except Exception as e:
    st.error(
        "⚠️ The AI service is temporarily unavailable or the free API limit has been reached. Please try again later."
    )

    st.caption(f"Error: {e}")

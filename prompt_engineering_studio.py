import os
import time
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

try:
    load_dotenv()
    client = Groq()
except Exception as ex:
    st.error(st(ex))

st.set_page_config(
    page_title="Prompt Engineering Studio",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns([9.5, 2.0, 2.0])
with col1:
    st.header("WELCOME TO :blue[PROMPT ENGINEERING STUDIO]")
with col2:
    if st.button(":green[Export Current Chat]"):
        os.makedirs("chats", exist_ok=True)
        filename = f"chats/chat_{datetime.now().strftime('%Y_%m_%d')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for message in st.session_state.messages:
                file.write(f"Role: {message['role']}\n")
                file.write(f"Content: {message['content']}.\n\n")
        st.success("Successfully Exported")
        time.sleep(0.5)
        st.rerun()
with col3:
    if st.button(":red[Clear Current Chat]"):
        st.session_state.messages = []
st.markdown(
    ":blue[Prompt Engineering Studio] is an interactive application for designing, testing, and comparing prompt engineering techniques across multiple LLMs. It enables users to experiment with roles, system prompts, sampling parameters, and structured outputs to understand and optimize AI responses."
)

role = ""
col1, col2, col3, col4 = st.columns(4)
with col1:
    model = st.selectbox(
        "Select your Model",
        ("llama-3.1-8b-instant", "llama-3.3-70b-versatile", "groq/compound"),
    )
with col2:
    role_ = st.selectbox(
        "Select Role for AI",
        (
            "Default",
            "AI Engineer",
            "Doctor",
            "Teacher",
            "Software Achitect",
            "Recruiter",
            "Career Mentor",
            "Islamic Scholar",
            "Travel Guide",
            "Lawyer",
        ),
    )
    if role_ == "Default":
        role += ""
    else:
        role += f"You are an experienced {role_}"
with col3:
    templates = {
        "Default": "",
        "💻 Code Review": """
Review the following code.

Code:
[Paste code here]

Requirements:
- Identify bugs
- Suggest improvements
- Evaluate readability
- Rate the code out of 10""",
        "📄 Resume Review": """
Review my resume.

Requirements:
- ATS Score
- Strengths
- Weaknesses
- Missing Skills
- Improvement Suggestions""",
        "🚀 Startup Idea Validator": """
Evaluate the following startup idea.

Idea:
[Describe your idea]

Requirements:
- Market potential
- Competition
- Revenue model
- Risks
- Final Rating (/10)""",
        "📚 Study Planner": """
Create a study plan for:

Subject:
[Enter subject]

Requirements:
- Daily schedule
- Weekly milestones
- Recommended free resources
- Mini projects""",
        "📊 SWOT Analysis": """
Perform a SWOT analysis for:

Business/Idea:
[Enter business]

Return the answer in a table with:
- Strengths
- Weaknesses
- Opportunities
- Threats""",
        "📰 Blog Writer": """
Write a professional blog about:

Topic:
[Enter topic]

Requirements:
- Catchy title
- Introduction
- Main sections
- Conclusion
- SEO-friendly headings""",
        "📱 Social Media Post": """
Create a LinkedIn post.

Topic:
[Enter topic]

Requirements:
- Professional tone
- Hook in the first sentence
- Use emojis moderately
- Include relevant hashtags""",
        "🔍 Research Assistant": """
Research the following topic.

Topic:
[Enter topic]

Requirements:
- Overview
- Key Concepts
- Advantages
- Challenges
- Future Scope
- References (if available)""",
        "📈 Project Planner": """
Create a complete project plan.

Project:
[Enter project]

Requirements:
- Objectives
- Features
- Tech Stack
- Development Phases
- Timeline
- Risks""",
        "🧠 Interview Preparation": """
You are a Senior Technical Interviewer.

Conduct a mock interview for:

Role:
[Enter role]

Requirements:
- Ask one question at a time
- Wait for my answer
- Evaluate my response
- Suggest improvements
- Continue until 10 questions are completed""",
    }
    action = st.selectbox(
        "Select your template]",
        (
            "Default",
            "💻 Code Review",
            "📄 Resume Review",
            "🚀 Startup Idea Validator",
            "📚 Study Planner",
            "📊 SWOT Analysis",
            "📰 Blog Writer",
            "📱 Social Media Post",
            "🔍 Research Assistant",
            "📈 Project Planner",
            "🧠 Interview Preparation",
        ),
    )
    role += templates[action]
with col4:
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.5
    )
st.markdown("Output Format")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.checkbox("Simple text", value=True):
        hidden_command = ""
with col2:
    if st.checkbox("JSON"):
        hid = " (JSON Format)"
with col3:
    if st.checkbox("README.md"):
        hidden_command = " (create a README.md file)"
with col4:
    if st.checkbox("Table"):
        hidden_command = " (Table Format)"

user_input = st.text_area("Ask Anything...", value=role, height=10)


if st.button("Generate Response"):
    st.session_state.messages.append(
        {"role": "user", "content": user_input + hidden_command}
    )
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        temperature=temperature,
        top_p=1,
    )

    response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.container(height=500):
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("User").write(message["content"])
            if message["role"] == "assistant":
                st.chat_message("Assistant").write(message["content"])

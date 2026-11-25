
import os
import textwrap
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from agents.marketing_agent import marketing_agent
from agents.email_agent import email_agent
from agents.business_analyst import business_analyst
from agents.task_manager import task_manager
from agents.coordinator import run_coordinator

from database.db import create_database, save_chat, get_chat_history


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BizPilot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# LOAD SETTINGS AND DATABASE
# --------------------------------------------------

load_dotenv()
create_database()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)


# --------------------------------------------------
# CUSTOM DESIGN / CSS
# --------------------------------------------------

st.markdown(textwrap.dedent("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080F1E;
    color: #E8EEF9;
}

[data-testid="stHeader"] {
    background: rgba(8, 15, 30, 0.95);
}

[data-testid="stSidebar"] {
    background: #0D1729;
    border-right: 1px solid #1C2B45;
}

[data-testid="stSidebar"] * {
    color: #DCE7F8;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #F4F7FF !important;
    font-weight: 700 !important;
}

p, label {
    color: #B7C5DA;
}


div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #132440, #0F1C31);
    border: 1px solid #29466D;
    border-radius: 16px;
    padding: 24px 20px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}

div[data-testid="stMetricLabel"] {
    color: #A9BAD3 !important;
    font-size: 14px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #55A5FF !important;
    font-size: 30px;
    font-weight: 800;
}

.stButton > button {
    background: #1769E8;
    color: white;
    border: 1px solid #3284FF;
    border-radius: 9px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #3284FF;
    border-color: #69A9FF;
    color: white;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background: #111F35;
    color: white;
    border-color: #2A4263;
    border-radius: 9px;
}

[data-testid="stChatMessage"] {
    background: #111F35;
    border: 1px solid #243B5B;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111F35;
    border: 1px solid #243B5B;
    border-radius: 14px;
}

hr {
    border-color: #243B5B;
}

.small-muted {
    color: #8FA4C1;
    font-size: 13px;
}

.brand-title {
    font-size: 25px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.7px;
}

.brand-accent {
    color: #4B9BFF;
}

.hero {
    background: linear-gradient(120deg, #10294A, #142044, #19264D);
    border: 1px solid #2B4D78;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 32px;
    margin-bottom: 8px;
}

.hero p {
    color: #B9CBE5;
    margin-bottom: 0;
}

.agent-card {
    background: #111F35;
    border: 1px solid #243B5B;
    border-radius: 13px;
    padding: 18px;
    min-height: 125px;
}

.agent-card h3 {
    font-size: 17px;
    margin-bottom: 8px;
}

.agent-card p {
    font-size: 13px;
    color: #A9BAD3;
}
/* Chat input styling */

[data-testid="stChatInput"] {
    background: #111F35 !important;
    border: 1px solid #2B4D78 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #F4F7FF !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8FA4C1 !important;
}

[data-testid="stBottom"] {
    background: #080F1E !important;
}

[data-testid="stChatInput"] button {
    background: #1769E8 !important;
    color: white !important;
    border-radius: 9px !important;
}
</style>
"""), unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand-title">BizPilot <span class="brand-accent">AI</span></div>',
        unsafe_allow_html=True
    )

    st.caption("INTELLIGENT BUSINESS PLATFORM")

    st.divider()

    st.markdown("### Workspace")

    page = st.radio(
        "Navigation",
        ["Dashboard", "AI Chat", "Chat History", "About"],
        label_visibility="collapsed"
    )

    st.session_state.page = page

    st.divider()

    st.markdown("### AI Configuration")

    agent_choice = st.selectbox(
        "Choose your AI agent",
        [
            "AI Coordinator (Auto)",
            "General Assistant",
            "Marketing Agent",
            "Email Agent",
            "Business Analyst Agent",
            "Task Manager Agent"
        ]
    )

    st.caption("Select Auto to let BizPilot route your request.")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.page = "AI Chat"
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<p class="small-muted">BizPilot AI · Business made smarter</p>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# GET DATABASE HISTORY
# --------------------------------------------------

history = get_chat_history()


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Business Intelligence, Powered by AI.</h1>
        <p>Your intelligent workspace for marketing, business analysis,
        email writing and productivity.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Overview")

    total_interactions = len(history)
    available_agents = 5

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Saved Interactions", total_interactions)

    with col2:
        st.metric("Available AI Agents", available_agents)

    with col3:
        st.metric("AI Model", "Groq API")

    st.divider()

    st.subheader("Your AI Workspace")

    agent_col1, agent_col2 = st.columns(2)

    with agent_col1:
        st.markdown("""
        <div class="agent-card">
            <h3>📣 Marketing Agent</h3>
            <p>Marketing strategies, social media content
            and promotional campaigns.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <h3>📊 Business Analyst</h3>
            <p>Business insights, sales analysis,
            opportunities and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <h3>🗓️ Task Manager</h3>
            <p>Task planning, priorities, deadlines
            and productivity suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    with agent_col2:
        st.markdown("""
        <div class="agent-card">
            <h3>✉️ Email Agent</h3>
            <p>Professional emails, customer replies
            and business follow-ups.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <h3>🤖 General Assistant</h3>
            <p>Ask questions and get practical
            business assistance.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <h3>⚡ AI Coordinator</h3>
            <p>Automatically routes your request
            to a suitable specialized agent.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # RECENT ACTIVITY
    st.divider()
    st.subheader("Recent Activity")
    st.caption("Your latest interactions with BizPilot AI")

    if history:

        for chat in history[:5]:

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown("**" + str(chat[2]) + "**")

                with col2:
                    st.caption(str(chat[3]))

                st.markdown("**Your request:**")
                st.write(str(chat[0]))

                with st.expander("View AI response"):
                    st.markdown(str(chat[1]))

    else:
        st.info("Your recent activity will appear here after your first chat.")

    # AI AGENT USAGE
    st.divider()
    st.subheader("AI Agent Usage")
    st.caption("Overview of saved interactions by agent")

    total_interactions = len(history)

    if history:

        agent_usage = {}

        for chat in history:
            agent_name = chat[2]
            agent_usage[agent_name] = agent_usage.get(agent_name, 0) + 1

        for agent_name, count in agent_usage.items():

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{agent_name}**")

            with col2:
                word = "interaction" if count == 1 else "interactions"
                st.markdown(f"**{count} {word}**")

            st.progress(count / total_interactions)
            st.write("")


# --------------------------------------------------
# AI CHAT PAGE
# --------------------------------------------------

 
elif st.session_state.page == "AI Chat":

    st.markdown("""
    <div style="margin-bottom:25px;">
        <div style="
            color:#55A5FF;
            font-size:13px;
            font-weight:700;
            letter-spacing:2px;
        ">
            BIZPILOT AI WORKSPACE
        </div>
        <h1 style="
            font-size:34px;
            margin:8px 0;
            color:#F4F7FF;
        ">
            Your Business Assistant
        </h1>
        <p style="color:#8FA4C1;font-size:15px;">
            Get intelligent support for your everyday business tasks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:linear-gradient(110deg,#112746,#14213D);
        border:1px solid #2B4D78;
        border-radius:12px;
        padding:15px 20px;
        margin-bottom:22px;
    ">
        <span style="color:#8FA4C1;font-size:12px;">
            ACTIVE AI AGENT
        </span>
        <div style="
            color:#55A5FF;
            font-size:17px;
            font-weight:700;
            margin-top:5px;
        ">
            ⚡ {agent_choice}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div style="
            text-align:center;
            padding:35px 15px;
            background:#0D1729;
            border:1px solid #243B5B;
            border-radius:15px;
            margin-bottom:20px;
        ">
            <div style="font-size:38px;">🤖</div>
            <h3 style="margin:10px 0;">How can I help your business?</h3>
            <p style="color:#8FA4C1;">
                Ask me about marketing, emails, business analysis
                or task management.
            </p>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:

        avatar = "🧑‍💼" if message["role"] == "user" else "🤖"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask BizPilot AI anything...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🤖"):

            with st.spinner("Your AI assistant is thinking..."):

                try:

                    selected_agent = agent_choice

                    if agent_choice == "AI Coordinator (Auto)":
                        selected_agent, answer = run_coordinator(
                            client,
                            user_input
                        )

                    elif agent_choice == "Marketing Agent":
                        answer = marketing_agent(client, user_input)

                    elif agent_choice == "Email Agent":
                        answer = email_agent(client, user_input)

                    elif agent_choice == "Business Analyst Agent":
                        answer = business_analyst(client, user_input)

                    elif agent_choice == "Task Manager Agent":
                        answer = task_manager(client, user_input)

                    else:
                        response = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            max_tokens=700,
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are BizPilot AI, a helpful "
                                        "professional business assistant. "
                                        "Keep answers clear and practical."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": user_input
                                }
                            ]
                        )

                        answer = response.choices[0].message.content

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                    save_chat(
                        user_input,
                        answer,
                        selected_agent
                    )

                except Exception as error:
                    st.error("Something went wrong: " + str(error))

# --------------------------------------------------
# CHAT HISTORY PAGE
# --------------------------------------------------

elif st.session_state.page == "Chat History":

    st.title("Conversation History")
    st.caption("Review your previously saved AI interactions.")

    if history:

        st.write("Total saved interactions:", len(history))

        for chat in history:

            with st.container(border=True):

                st.markdown("**" + str(chat[2]) + "**")
                st.markdown("**You:** " + str(chat[0]))
                st.markdown("**BizPilot AI:**")

                with st.expander("View AI response"):
                    st.markdown(str(chat[1]))

                st.caption("Date: " + str(chat[3]))

    else:
        st.info("No saved conversations yet.")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif st.session_state.page == "About":

    st.markdown("""
    <div class="hero">
        <h1>About BizPilot AI</h1>
        <p>One intelligent platform. Multiple specialized AI agents.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.subheader("What is BizPilot AI?")

    st.write("""
    BizPilot AI is an AI-powered business assistant designed to
    help users handle everyday business tasks through specialized
    AI agents.

    Instead of using separate tools for different tasks, users can
    interact with one platform and select the agent they need.
    """)

    st.divider()

    st.subheader("Our Core Capabilities")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📢 Marketing Agent
        Generates marketing strategies and promotional content.

        ### ✉️ Email Agent
        Helps draft professional business emails.

        ### 📊 Business Analyst
        Provides business insights and analyzes business-related requests.
        """)

    with col2:
        st.markdown("""
        ### ✅ Task Manager
        Helps organize tasks and plan work.

        ### 🤖 AI Coordinator
        Routes requests to specialized agents using predefined keywords.

        ### 💾 Chat History
        Stores conversations in a local SQLite database.
        """)

    st.divider()

    st.subheader("Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Frontend**")
        st.info("Streamlit")

    with col2:
        st.markdown("**AI Integration**")
        st.info("Groq API + Qwen")

    with col3:
        st.markdown("**Database**")
        st.info("SQLite")

    st.divider()

   
    st.subheader("Project Architecture")
    st.caption("How BizPilot AI processes a user request")

    st.components.v1.html("""
    <html>
    <body style="background:transparent; font-family:Arial; color:white;">

        <div style="background:#142B4D; border:1px solid #2878E8;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>👤 User</h2>
        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="background:#142B4D; border:1px solid #2878E8;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>🖥️ Streamlit Interface</h2>
        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="background:#173B70; border:2px solid #55A5FF;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>🤖 AI Coordinator</h2>
            <p>Keyword-based request routing</p>
        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="display:flex; flex-wrap:wrap; gap:10px; justify-content:center;">

            <div style="background:#142B4D; border:1px solid #2878E8;
            padding:18px; border-radius:12px; text-align:center; flex:1; min-width:120px;">
                <h3>📢 Marketing</h3>
                <p>Agent</p>
            </div>

            <div style="background:#142B4D; border:1px solid #2878E8;
            padding:18px; border-radius:12px; text-align:center; flex:1; min-width:120px;">
                <h3>✉️ Email</h3>
                <p>Agent</p>
            </div>

            <div style="background:#142B4D; border:1px solid #2878E8;
            padding:18px; border-radius:12px; text-align:center; flex:1; min-width:120px;">
                <h3>📊 Business</h3>
                <p>Analyst</p>
            </div>

            <div style="background:#142B4D; border:1px solid #2878E8;
            padding:18px; border-radius:12px; text-align:center; flex:1; min-width:120px;">
                <h3>✅ Task</h3>
                <p>Manager</p>
            </div>

        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="background:#142B4D; border:1px solid #2878E8;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>⚡ Groq API — Qwen Model</h2>
        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="background:#173B70; border:2px solid #55A5FF;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>💬 AI Response</h2>
        </div>

        <h2 style="text-align:center; color:#55A5FF;">↓</h2>

        <div style="background:#142B4D; border:1px solid #2878E8;
        padding:18px; border-radius:12px; text-align:center; margin:10px;">
            <h2>💾 SQLite Chat History</h2>
        </div>

    </body>
    </html>
    """, height=1100, scrolling=True)

    st.divider()

    st.subheader("Project Vision")

    st.write("""
    The goal of BizPilot AI is to demonstrate how multiple
    specialized AI agents can work together in one business
    assistance platform.

    This project is being developed as a practical exploration
    of AI integration, automation, Python development and
    multi-agent application design.
    """)

    st.caption("BizPilot AI | Built with Python, Streamlit and AI.")

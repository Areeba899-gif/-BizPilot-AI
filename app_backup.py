from agents.business_analyst import business_analyst
import streamlit as st
import os
from agents.email_agent import email_agent
from agents.coordinator import run_coordinator
from agents.task_manager import task_manager
from database.db import create_database, save_chat, get_chat_history

from groq import Groq
from dotenv import load_dotenv
create_database()

# Import Marketing Agent
from agents.marketing_agent import marketing_agent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="BizPilot AI",
    page_icon="🤖",
    layout="wide"
)

# Application heading
st.title("🤖 BizPilot AI")

st.subheader("Business AI Dashboard")

history = get_chat_history()

total_chats = len(history)

agents_count = 5

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Conversations", total_chats)

with col2:
    st.metric("Available AI Agents", agents_count)

with col3:
    st.metric("AI Coordinator", "Active")

st.divider()

st.subheader("Recent Activity")

if history:

    for chat in history[:5]:

        st.write("Agent:", chat[2])
        st.write("User:", chat[0])
        st.caption("Date: " + chat[3])
        st.divider()

else:
    st.info("No recent activity yet.")
    st.divider()

st.subheader("AI Agent Usage Analytics")

if history:

    agent_usage = {}

    for chat in history:
        agent = chat[2]

        if agent in agent_usage:
            agent_usage[agent] += 1
        else:
            agent_usage[agent] = 1

    st.bar_chart(agent_usage)

else:
    st.info("No agent usage data available yet.")

st.caption("Your Intelligent Business Assistant")

st.divider()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

# Connect to Groq
client = Groq(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.header("BizPilot AI")

    st.write("Choose your AI assistant:")

    agent_choice = st.selectbox(
        "Select Agent",
        [
            
   
    
    "AI Coordinator (Auto)",
    "General Assistant",
    "Marketing Agent",
    "Email Agent",
    "Business Analyst Agent",
    "Task Manager Agent"



        ]
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        st.divider()

st.subheader("Chat History")

if st.button("View Saved Chats"):

    history = get_chat_history()

    if history:
        for chat in history:

            st.write("Agent:", chat[2])
            st.write("You:", chat[0])
            st.write("AI:", chat[1])
            st.caption("Date: " + chat[3])

            st.divider()

    else:
        st.info("No saved conversations yet.")

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input(
    "Ask your question here..."
)

if user_input:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:
                # Marketing Agent
                if agent_choice == "AI Coordinator (Auto)":
                  selected_agent, answer = run_coordinator(
                          client, user_input
                         )
                  if agent_choice == "AI Coordinator (Auto)":
                   st.info(f"Selected Agent: {selected_agent}")
                elif agent_choice == "Marketing Agent":
                  answer = marketing_agent(client, user_input)
                # Email Agent
                elif agent_choice == "Email Agent":
                    answer = email_agent(client, user_input)
                elif agent_choice == "Business Analyst Agent":
                   answer = business_analyst(client, user_input)
                elif agent_choice == "Task Manager Agent":
                    answer = task_manager(client, user_input)
                # General Assistant
                else:
                    response = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are BizPilot AI, a helpful "
                                    "professional business assistant."
                                )
                            }
                        ] + st.session_state.messages
                    )

                    answer = response.choices[0].message.content

                # Display answer
                st.markdown(answer)

                # Save answer
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                save_chat(
                              user_input,
                               answer,
                               selected_agent if agent_choice == "AI Coordinator (Auto)" else agent_choice
                          )

            except Exception as error:
                st.error(f"AI Error: {error}")


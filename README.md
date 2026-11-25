<<<<<<< HEAD
# BizPilot AI 🤖

### An AI-Powered Multi-Agent Business Assistant

BizPilot AI is an AI-powered business assistant built with Python and Streamlit. It provides a single platform where users can interact with specialized AI agents to handle different business-related tasks.

The application integrates the Groq API with a Qwen language model and stores conversation history locally using SQLite.

## ✨ Key Features

- **AI Coordinator:** Routes user requests to specialized agents using predefined keywords.
- **General Assistant:** Handles general questions and requests.
- **Marketing Agent:** Generates marketing strategies and promotional content.
- **Email Agent:** Helps write professional business emails.
- **Business Analyst Agent:** Assists with business-related analysis.
- **Task Manager Agent:** Helps organize tasks and schedules.
- **Chat History:** Saves previous interactions in an SQLite database.
- **Dashboard:** Displays interaction statistics, recent activity and agent usage.
- **Dark UI:** A dark navy and electric blue interface built with Streamlit.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | User interface |
| Groq API | AI model integration |
| Qwen | Language model |
| SQLite | Local conversation storage |
| python-dotenv | Environment variable management |

## 🏗️ Project Architecture

```text
BizPilot AI
│
├── app.py
│
├── agents/
│   ├── coordinator.py
│   ├── marketing_agent.py
│   ├── email_agent.py
│   ├── business_analyst.py
│   └── task_manager.py
│
├── database/
│   ├── db.py
│   └── bizpilot.db
│
├── utils/
│
├── requirements.txt
├── .env
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "BizPilot AI"
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key. Never publish your API key.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database

BizPilot AI uses SQLite to store chat interactions, including:

- User messages
- AI responses
- Selected agent
- Interaction timestamps

The database is managed through the `database/db.py` module.

## 🧠 AI Agent Workflow

1. The user submits a business-related request.
2. The application receives the request through the Streamlit interface.
3. The AI Coordinator identifies the appropriate agent using predefined keywords.
4. The selected agent processes the request using the Groq API.
5. The response is displayed to the user.
6. The interaction is saved in the SQLite database.

## 🔐 Security Notes

- Keep API keys inside the `.env` file.
- Never upload `.env` or virtual environment folders to GitHub.
- Use `.gitignore` to exclude sensitive and unnecessary files.

## 🎯 Project Goals

This project explores practical AI integration, specialized AI agents, business workflow assistance, Python application development and database management.

## 👩‍💻 Developer

Developed as an AI student portfolio project.

## 📌 Project Status

Core application interface, specialized agents, coordinator, and local chat history have been implemented. Further testing and improvements are ongoing.

---

## 📸 Application Screenshots

### 1. Dashboard
![BizPilot AI Dashboard](screenshots/dashboard-full.png)

### 2. AI Chat
![BizPilot AI Chat](screenshots/ai-chat-full.png)

### 3. Chat History
![BizPilot AI Chat History](screenshots/chat-history-full.png)

### 4. About Page
![BizPilot AI About Page](screenshots/about-full.png)
=======
# -BizPilot-AI
An intelligent multi-agent AI business assistant
>>>>>>> e4a178a5e9750cd5cb771a7b75e3a88dbb70a8e8

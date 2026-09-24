# 🤖 Multi-Agent System

A multi-agent AI system built with **LangChain**, **Groq LLM**, and **Streamlit**.

## Features

- Multi-agent pipeline with specialized agents
- Tavily web search integration
- Interactive Streamlit UI
- Powered by Groq (fast LLM inference)

## 🚀 Getting Started

### 1. Clone the repository

\\\ash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
\\\

### 2. Create a virtual environment

\\\ash
python -m venv .venv
.venv\Scripts\activate   # Windows
\\\

### 3. Install dependencies

\\\ash
pip install -r requirements.txt
\\\

### 4. Set up environment variables

\\\ash
copy .env.example .env
\\\

Then edit \.env\ and fill in your real API keys:
- **GROQ_API_KEY** → Get from [console.groq.com](https://console.groq.com/keys)
- **TAVILY_API_KEY** → Get from [app.tavily.com](https://app.tavily.com/)

### 5. Run the app

\\\ash
streamlit run app.py
\\\

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set **Main file**: \pp.py\
4. In **Advanced settings → Secrets**, add:

\\\	oml
TAVILY_API_KEY = "your_key"
GROQ_API_KEY = "your_key"
GROQ_MODEL = "openai/gpt-oss-120b"
\\\

## 📁 Project Structure

\\\
multi_agent_system/
├── app.py           # Streamlit UI
├── agents.py        # Agent definitions
├── pipeline.py      # Agent pipeline logic
├── tools.py         # Custom tools
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md
\\\

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| \GROQ_API_KEY\ | Groq LLM API key |
| \TAVILY_API_KEY\ | Tavily search API key |
| \GROQ_MODEL\ | Model name to use |

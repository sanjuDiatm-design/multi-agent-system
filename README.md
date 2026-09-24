# 🤖 Multi-Agent Research System

An autonomous **AI-powered research pipeline** built with LangChain, Groq LLM, Tavily Search, and Streamlit. Enter any topic and watch four specialized agents collaborate to deliver a structured research report — automatically.

## 🧠 How It Works

The system runs a 4-step agentic pipeline:

1. **🔍 Search Agent** — Queries the web using Tavily to find recent, relevant sources on your topic
2. **📄 Reader Agent** — Picks the most relevant URL and scrapes its full content using BeautifulSoup
3. **✍️ Writer Agent** — Synthesizes the search results and scraped content into a clean, structured report
4. **🧐 Critic Agent** — Reviews and scores the report, highlighting strengths and weaknesses

## ✨ Features

- 🔗 Multi-agent pipeline with clear separation of concerns
- ⚡ Powered by **Groq** for ultra-fast LLM inference
- 🌐 Real-time web search via **Tavily**
- 🕸️ Smart web scraping with BeautifulSoup + Tavily fallback
- 📊 Interactive **Streamlit** UI with live progress tracking
- 🔒 Secure API key handling via .env

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain | Agent orchestration |
| Groq | Fast LLM inference |
| Tavily | Web search & extraction |
| BeautifulSoup | HTML scraping |
| Streamlit | Interactive UI |

## 🚀 Quick Start

`ash
git clone https://github.com/YOUR_USERNAME/multi-agent-system.git
cd multi-agent-system
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # Add your API keys
streamlit run app.py
`

## 🔑 Environment Variables

`env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
GROQ_MODEL=openai/gpt-oss-120b
`

Get keys: [Groq Console](https://console.groq.com/keys) · [Tavily](https://app.tavily.com/)

## 🌐 Deploy on Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → connect repo
3. Add your API keys under **Settings → Secrets**

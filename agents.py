import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import search, scrape_url
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name=None):
    model = model_name or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    if not model or model in ("llama-3.1-70b-versatile", "llama-3.1-8b-instant"):
        model = "openai/gpt-oss-120b"
    return ChatGroq(
        model=model,
        temperature=0,
        max_tokens=512,          # Cap agent response tokens (was unlimited ~4k+)
        api_key=os.getenv("GROQ_API_KEY")
    )

# ── Search Agent ─────────────────────────────────────────────────────────────
def build_search_agent(model=None):
    current_llm = model or get_llm()
    return create_agent(
        model=current_llm,
        tools=[search],
        system_prompt=(
            "You are a research search agent. Call the 'search' tool EXACTLY ONCE with a concise query. "
            "Do NOT call it again. Do NOT pass URLs as queries. "
            "After getting results, output 3-5 bullet points: key facts + source URLs. Keep it brief."
        )
    )

# ── Reader Agent ─────────────────────────────────────────────────────────────
def build_reader_agent(model=None):
    current_llm = model or get_llm()
    return create_agent(
        model=current_llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a reader agent. Pick ONE URL from the search results and call scrape_url EXACTLY ONCE. "
            "Do NOT call any tool again. Output 3-5 bullet points of key insights from the scraped content. Be brief."
        )
    )

# ── Writer Chain ──────────────────────────────────────────────────────────────
# Concise prompt — forces a focused report instead of an essay (saves ~60% tokens)
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research writer. Write concise, factual reports. Be direct and avoid padding."),
    ("human", """Write a research report on: {topic}

Research:
{research}

Format:
## Introduction (2-3 sentences)
## Key Findings (3 bullet points, 1-2 sentences each)
## Conclusion (2 sentences)
## Sources (URLs only)

Keep the total report under 400 words."""),
])

def get_writer_chain(model=None):
    llm = model or get_llm()
    # Override max_tokens for writer to allow a proper report (but still capped)
    if hasattr(llm, 'max_tokens') and llm.max_tokens == 512:
        llm = ChatGroq(
            model=llm.model_name,
            temperature=0,
            max_tokens=800,       # Writer needs a bit more room but still capped
            api_key=os.getenv("GROQ_API_KEY")
        )
    return writer_prompt | llm | StrOutputParser()

# ── Critic Chain ──────────────────────────────────────────────────────────────
# Critic receives only the FIRST 800 chars of the report to save input tokens
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research critic. Be brief and direct."),
    ("human", """Rate this research report excerpt (truncated for brevity):

{report}

Respond ONLY in this format (no extra text):
Score: X/10
Strengths: [one line]
Weakness: [one line]
Verdict: [one line]"""),
])

def get_critic_chain(model=None):
    llm = model or get_llm()
    return critic_prompt | llm | StrOutputParser()
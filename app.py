import streamlit as st
import time
import os
from agents import (
    build_reader_agent,
    build_search_agent,
    get_writer_chain,
    get_critic_chain,
    get_llm
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #e8e4dc; }

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.28em; text-transform: uppercase;
    color: #ff8c32; margin-bottom: 0.9rem; opacity: 0.85;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.6rem, 6vw, 4.5rem);
    font-weight: 800; line-height: 1; letter-spacing: -0.03em;
    color: #f0ebe0; margin: 0 0 0.8rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1rem; font-weight: 300; color: #a09890;
    max-width: 480px; margin: 0 auto; line-height: 1.6;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 1.8rem 0;
}

/* ── Search wrapper ── */
.search-wrapper {
    max-width: 720px;
    margin: 0 auto 0.5rem;
    position: relative;
}
.search-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.22em;
    text-transform: uppercase; color: #ff8c32;
    font-weight: 500; margin-bottom: 0.55rem;
    display: block;
}

/* ── Input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 14px !important; color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.15rem !important;
    padding: 1rem 1.4rem !important;
    transition: border-color 0.25s, box-shadow 0.25s, background 0.25s !important;
    height: 60px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    background: rgba(255,140,50,0.06) !important;
    box-shadow: 0 0 0 4px rgba(255,140,50,0.14) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important; letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important; font-weight: 500 !important;
}

/* ── Topic chips ── */
.chips-row {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-top: 0.85rem; justify-content: center;
}
.chip {
    background: rgba(255,140,50,0.08);
    border: 1px solid rgba(255,140,50,0.22);
    border-radius: 999px;
    padding: 0.32rem 0.9rem;
    font-size: 0.78rem; color: #ffaa66;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: background 0.18s, border-color 0.18s, transform 0.12s;
    white-space: nowrap;
}
.chip:hover {
    background: rgba(255,140,50,0.18);
    border-color: rgba(255,140,50,0.55);
    transform: translateY(-1px);
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    letter-spacing: 0.04em !important; border: none !important;
    border-radius: 10px !important; padding: 0.7rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Clear button (2nd button) ── */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button,
.stButton:nth-child(2) > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #888 !important;
    box-shadow: none !important;
    font-size: 0.85rem !important;
}
.stButton:nth-child(2) > button:hover {
    border-color: rgba(255,80,80,0.4) !important;
    color: #ff6666 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem; position: relative;
    overflow: hidden; transition: border-color 0.3s;
}
.step-card.active { border-color: rgba(255,140,50,0.45); background: rgba(255,140,50,0.04); }
.step-card.done   { border-color: rgba(80,200,120,0.3);  background: rgba(80,200,120,0.03); }
.step-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; border-radius: 12px 0 0 12px;
    background: rgba(255,255,255,0.05); transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }
.step-header { display: flex; align-items: center; gap: 0.7rem; }
.step-num {
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.15em; color: #ff8c32; opacity: 0.65;
}
.step-title {
    font-family: 'Syne', sans-serif; font-size: 0.9rem;
    font-weight: 700; color: #f0ebe0;
}
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; }
.status-waiting { color: #444; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }

/* ── Live status banner ── */
.live-banner {
    background: rgba(255,140,50,0.07);
    border: 1px solid rgba(255,140,50,0.28);
    border-radius: 10px; padding: 0.7rem 1.1rem;
    font-size: 0.82rem; color: #ffaa55;
    font-family: 'DM Mono', monospace; margin-top: 0.6rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px; padding: 2rem 2.2rem; margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px; padding: 1.6rem 2rem; margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    letter-spacing: 0.2em; text-transform: uppercase;
    margin-bottom: 1rem; padding-bottom: 0.6rem;
}
.panel-label.orange { color: #ff8c32; border-bottom: 1px solid rgba(255,140,50,0.15); }
.panel-label.green  { color: #50c878; border-bottom: 1px solid rgba(80,200,120,0.15); }

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    color: #ff8c32 !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important; border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important; letter-spacing: 0.08em !important;
}
.stDownloadButton > button:hover {
    background: rgba(255,140,50,0.08) !important;
    border-color: rgba(255,140,50,0.5) !important;
}

/* ── Footer ── */
.notice {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    color: #383430; text-align: center; margin-top: 3rem; letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

# Fixed model — no dropdown shown to user
FIXED_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


# ── Step card renderer ────────────────────────────────────────────────────────
def step_card_html(num, title, state, icon):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("WAITING", "status-waiting"))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    return f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{icon} {title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
    </div>"""


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">Type a topic. Four AI agents search, read, write and critique — delivering a full report in seconds.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Example chips (click to fill) ───────────────────────────────────────────
EXAMPLE_TOPICS = [
    "🤖 Rise of Agentic AI in 2026",
    "🧬 CRISPR gene editing breakthroughs",
    "🔋 Solid-state battery technology",
    "🌍 Climate change solutions 2025",
    "🚀 SpaceX Starship latest update",
    "💊 GLP-1 drugs and obesity research",
]

# ── Centered search layout ────────────────────────────────────────────────────
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Rise of agentic AI in 2026  —  press Enter or click Run",
    key="topic_input",
)

# Chips row — build without conflicting f-string escapes
def make_chip(label):
    topic_text = label.split(" ", 1)[-1]  # strip emoji prefix
    onclick = f"document.querySelector('input').value='{topic_text}'"
    return f'<span class="chip" onclick="{onclick}">{label}</span>'

chips_html = '<div class="chips-row">' + "".join(make_chip(t) for t in EXAMPLE_TOPICS) + "</div>"
st.markdown(chips_html, unsafe_allow_html=True)

col_run, col_gap2, col_clear = st.columns([4, 0.3, 1.5])
with col_run:
    run_btn = st.button("⚡  Run Research", use_container_width=True, key="run_btn")
with col_clear:
    clear_btn = st.button("✕  Clear", use_container_width=True, key="clear_btn")

st.markdown('</div>', unsafe_allow_html=True)

# Enter key support via JS
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const btns = window.parent.document.querySelectorAll('button');
        for (const b of btns) {
            if (b.innerText.includes('Run Research')) { b.click(); break; }
        }
    }
});
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Pipeline tracker (right side) ────────────────────────────────────────────
_, col_right = st.columns([1, 1])
with col_right:
    pass

pipeline_ph = st.empty()
status_ph   = st.empty()

# Handle clear
if clear_btn:
    st.session_state.results = {}
    st.session_state.running = False
    st.session_state.done    = False
    st.rerun()

STEPS = [
    ("01", "Search Agent",  "search", "🔍"),
    ("02", "Reader Agent",  "reader", "📄"),
    ("03", "Writer Chain",  "writer", "✍️"),
    ("04", "Critic Chain",  "critic", "🧐"),
]

def render_pipeline(active=None, completed=None):
    if completed is None:
        completed = list(st.session_state.results.keys()) if st.session_state.results else []
    cards = []
    for num, title, key, icon in STEPS:
        if key in completed:    state = "done"
        elif key == active:     state = "running"
        else:                   state = "waiting"
        cards.append(step_card_html(num, title, state, icon))
    pipeline_ph.markdown("".join(cards), unsafe_allow_html=True)

def set_status(msg=None):
    if msg:
        status_ph.markdown(
            f'<div class="live-banner"><span>⚡</span><span>{msg}</span></div>',
            unsafe_allow_html=True
        )
    else:
        status_ph.empty()

if not st.session_state.running:
    render_pipeline()


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False


# ── Pipeline execution ────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    topic_val = topic.strip() or st.session_state.get("topic_input", "")
    results   = {}

    try:
        llm = get_llm(model_name=FIXED_MODEL)

        # Step 1 — Search
        render_pipeline(active="search", completed=[])
        set_status("Searching the web…")
        search_agent = build_search_agent(model=llm)
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent reliable information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content or ""
        st.session_state.results = dict(results)

        # Step 2 — Reader
        render_pipeline(active="reader", completed=["search"])
        set_status("Scraping top source…")
        reader_agent = build_reader_agent(model=llm)
        rr = reader_agent.invoke({
            "messages": [("user",
                f"From these search results about '{topic_val}', pick ONE URL and scrape it.\n\n"
                f"{results['search'][:1000]}"
            )]
        })
        scraped = rr["messages"][-1].content or ""
        results["reader"] = scraped if scraped.strip() else results["search"][:800]
        st.session_state.results = dict(results)

        # Step 3 — Writer
        render_pipeline(active="writer", completed=["search", "reader"])
        set_status("Writing report…")
        writer = get_writer_chain(model=llm)
        research = f"SEARCH:\n{results['search'][:750]}\n\nSCRAPED:\n{results['reader'][:750]}"
        results["writer"] = writer.invoke({"topic": topic_val, "research": research})
        st.session_state.results = dict(results)

        # Step 4 — Critic
        render_pipeline(active="critic", completed=["search", "reader", "writer"])
        set_status("Reviewing report…")
        critic = get_critic_chain(model=llm)
        results["critic"] = critic.invoke({"report": results["writer"][:600]})
        st.session_state.results = dict(results)

        # Done
        render_pipeline(active=None, completed=["search", "reader", "writer", "critic"])
        set_status()
        st.session_state.running = False
        st.session_state.done    = True
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.session_state.done    = False
        set_status()
        st.error(f"❌ {e}")


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r and st.session_state.done:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown('<div class="report-panel"><div class="panel-label orange">📝 Research Report</div>',
                    unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic score
    if "critic" in r:
        st.markdown('<div class="feedback-panel"><div class="panel-label green">🧐 Critic Score</div>',
                    unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="notice">ResearchMind · LangChain · Groq · Streamlit</div>',
            unsafe_allow_html=True)
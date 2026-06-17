import streamlit as st
import time
import html
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg-0: #f7f3ea;
    --bg-1: #efe7da;
    --bg-2: #fdfaf4;
    --paper: rgba(255, 253, 247, 0.76);
    --ink: #1f2a37;
    --ink-muted: #4c5b6e;
    --line: rgba(31, 42, 55, 0.12);
    --brand: #0b84a5;
    --brand-2: #f39f5a;
    --ok: #1f9d55;
    --wait: #7b8794;
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(circle at 6% 12%, rgba(11,132,165,0.2) 0%, rgba(11,132,165,0) 30%),
        radial-gradient(circle at 94% 8%, rgba(243,159,90,0.23) 0%, rgba(243,159,90,0) 34%),
        linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 48%, var(--bg-2) 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 1260px;
    padding: 2rem 2.8rem 4rem;
    animation: page-in 560ms ease-out;
}

@keyframes page-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(11,132,165,0.16); }
    50% { box-shadow: 0 0 0 10px rgba(11,132,165,0); }
}

.hero {
    position: relative;
    padding: 2.1rem 2rem 2.4rem;
    margin-bottom: 1.4rem;
    border: 1px solid var(--line);
    border-radius: 24px;
    background: linear-gradient(125deg, rgba(255,255,255,0.78), rgba(255,247,229,0.72));
    backdrop-filter: blur(6px);
    overflow: hidden;
}

.hero::after {
    content: '';
    position: absolute;
    width: 220px;
    height: 220px;
    right: -72px;
    top: -82px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(11,132,165,0.32), rgba(11,132,165,0));
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--brand);
    background: rgba(11,132,165,0.08);
    border: 1px solid rgba(11,132,165,0.24);
    border-radius: 999px;
    padding: 0.3rem 0.75rem;
}

.hero h1 {
    font-family: 'Chakra Petch', sans-serif;
    font-size: clamp(2.3rem, 5vw, 4.2rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 1rem 0 0.7rem;
    color: var(--ink);
}

.hero h1 span {
    color: var(--brand);
}

.hero-sub {
    max-width: 760px;
    margin: 0;
    color: var(--ink-muted);
    font-size: 1.01rem;
    line-height: 1.7;
}

.hero-strip {
    margin-top: 1.2rem;
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}

.hero-pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    color: #284054;
    border: 1px solid rgba(31,42,55,0.14);
    border-radius: 999px;
    padding: 0.42rem 0.75rem;
    background: rgba(255,255,255,0.62);
}

.divider {
    height: 1px;
    margin: 1.9rem 0;
    background: linear-gradient(90deg, transparent, rgba(11,132,165,0.42), transparent);
}

.input-card {
    border-radius: 22px;
    border: 1px solid var(--line);
    background: var(--paper);
    padding: 1.6rem 1.6rem 1.2rem;
    box-shadow: 0 12px 35px rgba(52, 71, 88, 0.1);
}

.stTextInput > label {
    font-family: 'Space Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 0.16em !important;
    font-size: 0.69rem !important;
    color: var(--brand) !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(31,42,55,0.18) !important;
    border-radius: 13px !important;
    font-size: 0.97rem !important;
    color: var(--ink) !important;
    padding: 0.82rem 0.95rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 4px rgba(11,132,165,0.16) !important;
}

.stButton > button {
    background: linear-gradient(130deg, var(--brand), #10738f) !important;
    color: #f8fdfd !important;
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 0.05em !important;
    font-size: 0.94rem !important;
    border: none !important;
    border-radius: 13px !important;
    padding: 0.78rem 1.2rem !important;
    box-shadow: 0 12px 22px rgba(11,132,165,0.25) !important;
    transition: transform 160ms ease, box-shadow 160ms ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 16px 26px rgba(11,132,165,0.34) !important;
}

.stButton > button:focus-visible {
    animation: pulse 1.2s ease infinite;
}

.example-row {
    margin-top: 1rem;
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
    align-items: center;
}

.example-kicker {
    font-family: 'Space Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.13em;
    color: #58687a;
}

.example-chip {
    border: 1px solid rgba(31,42,55,0.14);
    border-radius: 999px;
    padding: 0.38rem 0.78rem;
    font-size: 0.74rem;
    color: #2f4156;
    background: rgba(255,255,255,0.7);
    transition: transform 160ms ease, border-color 160ms ease;
}

.example-chip:hover {
    transform: translateY(-1px);
    border-color: rgba(11,132,165,0.42);
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #163047;
    margin: 0.35rem 0 1rem;
}

.section-heading::before {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(130deg, var(--brand), var(--brand-2));
}

.step-card {
    background: rgba(255,255,255,0.64);
    border: 1px solid rgba(31,42,55,0.12);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    position: relative;
    transition: transform 170ms ease, border-color 170ms ease, box-shadow 170ms ease;
}

.step-card:hover {
    transform: translateY(-2px);
    border-color: rgba(11,132,165,0.3);
    box-shadow: 0 10px 24px rgba(67,88,107,0.11);
}

.step-card.active {
    border-color: rgba(11,132,165,0.55);
    box-shadow: 0 0 0 3px rgba(11,132,165,0.1);
}

.step-card.done {
    border-color: rgba(31,157,85,0.4);
    background: linear-gradient(135deg, rgba(255,255,255,0.75), rgba(225,245,235,0.72));
}

.step-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.67rem;
    color: #516072;
    background: rgba(31,42,55,0.06);
    border-radius: 6px;
    padding: 0.17rem 0.42rem;
}

.step-title {
    font-family: 'Manrope', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #1b2a39;
}

.step-status {
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
}

.status-waiting { color: var(--wait); }
.status-running { color: var(--brand); }
.status-done { color: var(--ok); }

.result-panel,
.report-panel,
.feedback-panel {
    background: rgba(255,255,255,0.9);
    border-radius: 20px;
    border: 1px solid rgba(31,42,55,0.14);
    padding: 1.5rem;
    box-shadow: 0 8px 24px rgba(67,88,107,0.1);
}

.result-panel-title,
.panel-label {
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.66rem;
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(31,42,55,0.14);
}

.result-panel-title,
.panel-label.orange {
    color: var(--brand);
}

.panel-label.green {
    color: var(--ok);
}

.report-panel {
    color: #000000 !important;
    background: rgba(255,255,255,0.96);
    border-left: 4px solid rgba(11,132,165,0.7);
}

.report-body {
    color: #000000 !important;
    line-height: 1.72;
    font-size: 0.95rem;
    white-space: pre-wrap;
}

.feedback-panel {
    color: #000000 !important;
    background: rgba(255,255,255,0.96);
    border-left: 4px solid rgba(31,157,85,0.7);
}

.feedback-body {
    color: #000000 !important;
    line-height: 1.72;
    font-size: 0.95rem;
    white-space: pre-wrap;
}

.feedback-panel h1,
.feedback-panel h2,
.feedback-panel h3,
.feedback-panel h4,
.feedback-panel h5,
.feedback-panel h6,
.feedback-panel p,
.feedback-panel li,
.feedback-panel span,
.feedback-panel strong,
.feedback-panel em,
.feedback-panel code,
.feedback-panel blockquote,
.feedback-panel a {
    color: #000000 !important;
}

.report-panel h1,
.report-panel h2,
.report-panel h3,
.report-panel h4,
.report-panel h5,
.report-panel h6,
.report-panel p,
.report-panel li,
.report-panel span,
.report-panel strong,
.report-panel em,
.report-panel code,
.report-panel blockquote,
.report-panel a {
    color: #000000 !important;
}

.report-panel a {
    text-decoration-color: #000000 !important;
}

.result-content {
    color: #31465b;
    white-space: pre-wrap;
    line-height: 1.72;
    font-size: 0.92rem;
}

.stSpinner > div { color: var(--brand) !important; }

details {
    border: 1px solid rgba(31,42,55,0.14);
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
    padding: 0.25rem 0.8rem;
}

details summary {
    font-family: 'Space Mono', monospace !important;
    color: #516072 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
}

.notice {
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    color: #67788c;
    text-align: center;
    margin-top: 2.5rem;
    letter-spacing: 0.08em;
}

@media (max-width: 1024px) {
    .block-container { padding: 1.4rem 1.1rem 3rem; }
    .hero { padding: 1.4rem 1rem 1.6rem; }
    .hero-sub { font-size: 0.95rem; }
}

@media (max-width: 680px) {
    .hero h1 { font-size: 2rem; }
    .input-card,
    .result-panel,
    .report-panel,
    .feedback-panel { padding: 1rem; }
    .example-chip { font-size: 0.69rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#94a3b8;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Studio</span></h1>
    <p class="hero-sub">
        Four specialized agents collaborate in a single orchestrated workflow:
        search, deep read, write, then critique. Enter a topic and get a
        structured report with transparent intermediate outputs.
    </p>
    <div class="hero-strip">
        <span class="hero-pill">4 Agent Pipeline</span>
        <span class="hero-pill">Traceable Raw Outputs</span>
        <span class="hero-pill">Downloadable Markdown Report</span>
    </div>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button(
        "⚡ Run Research Pipeline",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown('<div class="example-row"><span class="example-kicker">TRY:</span>', unsafe_allow_html=True)

    examples = [
        "Future of LLM in Tech Industry",
        "All Lastest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]

    for ex in examples:
        st.markdown(f"""
        <span class="example-chip">{ex}</span>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:

    st.markdown(
        '<div class="section-heading">Pipeline</div>',
        unsafe_allow_html=True
    )

    r = st.session_state.results
    done = st.session_state.done

    def s(step):

        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"

        return "waiting"

    step_card(
        "01",
        "Search Agent",
        s("search"),
        "Gathers recent web information"
    )

    step_card(
        "02",
        "Reader Agent",
        s("reader"),
        "Scrapes & extracts deep content"
    )

    step_card(
        "03",
        "Writer Chain",
        s("writer"),
        "Drafts the full research report"
    )

    step_card(
        "04",
        "Critic Chain",
        s("critic"),
        "Reviews & scores the report"
    )


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍 Search Agent is working…"):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄 Reader Agent is scraping top resources…"):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️ Writer is drafting the report…"):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })

        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐 Critic is reviewing the report…"):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Results</div>',
        unsafe_allow_html=True
    )

    # Raw outputs
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Search Agent Output
                    </div>

                    <div class="result-content">
                        {r["search"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Reader Agent Output
                    </div>

                    <div class="result-content">
                        {r["reader"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:
        report_html = html.escape(r["writer"]).replace("\n", "<br>")

        st.markdown(
            f'''
            <div class="report-panel">
                <div class="panel-label orange">
                    📝 Final Research Report
                </div>
                <div class="report-body">{report_html}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Download button
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        critic_html = html.escape(r["critic"]).replace("\n", "<br>")

        st.markdown(
            f'''
            <div class="feedback-panel">
                <div class="panel-label green">
                    🧐 Critic Feedback
                </div>
                <div class="feedback-body">{critic_html}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchAgent · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
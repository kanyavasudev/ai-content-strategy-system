import streamlit as st

st.set_page_config(
    page_title="AI Content Strategy System",
    page_icon="🧠",
    layout="centered"
)

# ── HERO SECTION ──
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='font-size: 2.8rem; font-weight: 800;'>AI Content Strategy System</h1>
    <p style='font-size: 1.2rem; color: gray;'>
        AI-powered tools for SEO keyword research and daily marketing updates
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── BUILT BY ──
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h3>Built by <a href='https://www.linkedin.com/in/kanya-v' target='_blank'>Kanya V</a></h3>
        <p style='color: gray;'>Content Strategist · Data-Driven Growth · AI + Marketing</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── WHY I BUILT THIS ──
st.markdown("### 💡 Why I Built This")
st.markdown("""
I built this because content research used to take me hours.

Finding the right keywords, understanding what's already out there,
figuring out why some posts work and others don't —
it all took time that could have gone into actually creating.

So I built a system that does the heavy research for you.

You bring your raw idea — even a half-formed thought.
The tools help you understand it better, find the right angle,
and turn it into something worth reading.

No jargon. No overwhelm. Just clear, useful output
that helps you create content that actually connects.

Built for myself first. Sharing it because it might help you too.
""")
st.markdown("---")

# ── TOOL CARDS ──
st.markdown("### 🛠️ The Tools")
st.markdown(" ")


def card(emoji, title, text, c1, c2, page, icon):
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {c1}, {c2});
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        min-height: 220px;
    '>
        <div style='font-size: 2.5rem;'>{emoji}</div>
        <h3 style='color: white; margin: 0.5rem 0;'>{title}</h3>
        <p style='font-size: 0.9rem; opacity: 0.9;'>{text}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(" ")
    st.page_link(page, label="Open Tool →", icon=icon)


row1 = st.columns(2)
with row1[0]:
    card("🔍", "Keyword Research",
         "Enter a domain and pick Blog or On-page. Get a keyword set built for that goal, "
         "with intent, funnel stage, difficulty and titles.",
         "#7209b7", "#b5179e", "pages/keyword_research.py", "🔍")
with row1[1]:
    card("📰", "Daily Updates",
         "One click for today's Google AI, Google SEO and social media news, "
         "with what it means for you and what to do.",
         "#e76f51", "#f4a261", "pages/daily_news.py", "📰")

st.markdown("---")

# ── WHAT MAKES THIS DIFFERENT ──
st.markdown("### 🎯 What Makes This Different")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **❌ How most people use AI:**
    - Open ChatGPT
    - Ask for content ideas
    - Get generic output
    - Sound like everyone else
    - Wonder why it doesn't work
    """)

with col2:
    st.markdown("""
    **✅ How this system works:**
    - You bring your raw thinking
    - AI researches and expands it
    - Output is built around YOUR context
    - Sounds like your brand
    - Backed by data and strategy
    """)

st.markdown("---")

# ── TECH STACK ──
st.markdown("### ⚙️ Built With")

col1, col2, col3, col4, col5 = st.columns(5)
for col, (emoji, name) in zip(
    [col1, col2, col3, col4, col5],
    [("🐍", "Python"), ("🎈", "Streamlit"), ("🤖", "Gemini AI"), ("📊", "Plotly"), ("🐼", "Pandas")],
):
    with col:
        st.markdown(f"""
        <div style='text-align:center'>
            <div style='font-size:2rem'>{emoji}</div>
            <p><b>{name}</b></p>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── FOOTER ──
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem 0;'>
    <p>Built by <a href='https://www.linkedin.com/in/kanya-v' target='_blank'>Kanya V</a>
    · Content Strategist ·
    <a href='https://github.com/kanyavasudev' target='_blank'>GitHub</a></p>
    <p style='font-size: 0.8rem;'>
        This tool was built to demonstrate how AI and data analytics
        can work together to power smarter content strategy decisions.
    </p>
</div>
""", unsafe_allow_html=True)

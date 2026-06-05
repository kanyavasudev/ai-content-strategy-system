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
        AI-powered tools for content strategy, SEO research, and social media analysis
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

# ── 3 MODULE CARDS ──
st.markdown("### 🛠️ The Tools")
st.markdown(" ")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #0077b6, #00b4d8);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        min-height: 220px;
    '>
        <div style='font-size: 2.5rem;'>📝</div>
        <h3 style='color: white; margin: 0.5rem 0;'>Content Brief Generator</h3>
        <p style='font-size: 0.9rem; opacity: 0.9;'>
            Turn your raw idea into a full content brief — with competitor gaps, 
            platform recommendations, hooks, and SEO keywords.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(" ")
    st.page_link("pages/content_brief.py", label="Open Tool →", icon="📝")

with col2:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #7209b7, #b5179e);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        min-height: 220px;
    '>
        <div style='font-size: 2.5rem;'>🔍</div>
        <h3 style='color: white; margin: 0.5rem 0;'>SEO Research Tool</h3>
        <p style='font-size: 0.9rem; opacity: 0.9;'>
            Enter a seed keyword and get similar keywords, difficulty ratings, 
            TOFU/MOFU/BOFU mapping, competitor content, and blog titles.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(" ")
    st.page_link("pages/seo_research.py", label="Open Tool →", icon="🔍")

with col3:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #2d6a4f, #52b788);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        min-height: 220px;
    '>
        <div style='font-size: 2.5rem;'>📊</div>
        <h3 style='color: white; margin: 0.5rem 0;'>Social Media Analyser</h3>
        <p style='font-size: 0.9rem; opacity: 0.9;'>
            Upload your LinkedIn analytics and get graphs, content diagnostics, 
            deep insights, and an executive-ready report.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(" ")
    st.page_link("pages/social_analysis.py", label="Open Tool →", icon="📊")

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
with col1:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:2rem'>🐍</div>
        <p><b>Python</b></p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:2rem'>🎈</div>
        <p><b>Streamlit</b></p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:2rem'>🤖</div>
        <p><b>Gemini AI</b></p>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:2rem'>📊</div>
        <p><b>Plotly</b></p>
    </div>""", unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:2rem'>🐼</div>
        <p><b>Pandas</b></p>
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

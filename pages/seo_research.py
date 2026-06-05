import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="SEO Research Tool",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 SEO Research Tool")
st.caption("Built by Kanya V · Content Strategist")
st.markdown("---")

# ── SECTION 1 — KEYWORD INPUTS ──
st.markdown("### 🌱 Your Seed Keyword")

seed_keyword = st.text_input(
    "What is your main keyword?",
    placeholder="e.g. content strategy for startups"
)

brand_context = st.text_input(
    "What is your brand/website about?",
    placeholder="e.g. B2B cybersecurity company targeting IT managers"
)

st.markdown("---")

# ── SECTION 2 — TARGETING ──
st.markdown("### 🎯 Your Targeting")

col1, col2 = st.columns(2)

with col1:
    funnel_stage = st.selectbox(
        "Funnel Stage",
        [
            "TOFU — Awareness (broad audience)",
            "MOFU — Consideration (solution seekers)",
            "BOFU — Decision (ready to act)"
        ]
    )

with col2:
    target_location = st.selectbox(
        "Target Location",
        [
            "Global",
            "India",
            "United States",
            "United Kingdom",
            "Southeast Asia"
        ]
    )

st.markdown("---")

if st.button("🔍 Research My Keywords", type="primary"):
    if not seed_keyword or not brand_context:
        st.warning("Please fill in all fields!")
    else:
        with st.spinner("Researching keywords, analysing competitors, building your SEO brief..."):

            prompt = f"""
You are a friendly SEO consultant — like that smart friend who knows everything about Google 
and explains it in plain English without making you feel stupid.

No jargon. No complicated words. Talk like a real person.
Avoid words like: leverage, utilise, robust, synergy, paradigm.

The person you're helping has shared this:

SEED KEYWORD: {seed_keyword}
BRAND CONTEXT: {brand_context}
FUNNEL STAGE: {funnel_stage}
TARGET LOCATION: {target_location}

Help them understand their keyword opportunity and what to do with it.
Keep each section short and clear.
Use bullet points and tables where possible.
Write like you're explaining this over coffee — not writing a textbook.

---

## 🌱 IS THIS KEYWORD WORTH IT?
Give them a straight answer first — yes or no, and why.
Then break it down simply:
- What people mean when they search this: one plain English sentence
- How hard is it to rank: Easy / Medium / Hard — and why in one line
- Does it match {funnel_stage}: yes/no and why in one line

---

## 🔑 SIMILAR KEYWORDS TO EXPLORE
10 related keywords they could also target.
Keep the table simple and readable:
| Keyword | Difficulty | What people want | Funnel Stage | Go for it? |

Go for it = Yes / Maybe / Skip

---

## 📊 WHICH STAGE ARE THESE KEYWORDS FOR?
Group the keywords simply:
- Top of Funnel (people just discovering): (list)
- Middle of Funnel (people comparing options): (list)
- Bottom of Funnel (people ready to act): (list)
Then tell them: where's the biggest opportunity right now? One sentence.

---

## 🏆 START WITH THESE 3
Which 3 keywords should they go after first?
Be direct. Tell them exactly why.
Format:
1. [keyword] — go here first because — difficulty level
2. [keyword] — go here next because — difficulty level
3. [keyword] — go here after because — difficulty level

---

## 🔍 WHAT'S ALREADY RANKING
4 pieces of content already showing up for this keyword.
Help them understand WHY those pieces rank — in plain English.
Format:
- [Title] — [Website] — [Why Google likes it — one simple line]

---

## ✍️ HOW TO MAKE YOUR CONTENT STAND OUT
5 practical tips to make content on "{seed_keyword}" actually interesting to read.
No generic advice like "write quality content."
Be specific. One line each. Plain English.

---

## 📝 BLOG TITLE IDEAS
3 title options they can use right now.
Each title should:
- Feel like something a real person would click on
- Include the keyword naturally — not forced
- Match the vibe of {funnel_stage}

---

## 🔗 META DESCRIPTION
One ready to use meta description.
Max 155 characters.
Should make someone want to click — not just describe the article.
Include the keyword naturally.

---

## 🔗 WHAT TO LINK TO INSIDE THIS ARTICLE
3 topics this article should link to — and why linking there helps the reader.
Format:
- [Topic] — why this link helps the reader — one line

---
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                brief = response.text  # or research/analysis
            except Exception:
                st.error("⚠️ AI analysis is temporarily busy. Please try again in a few minutes.")
                st.stop()

        # ── OUTPUT ──
        st.markdown("---")
        st.markdown("### 📋 Your SEO Research Report")
        st.markdown(research)

        # Save
        with open("seo_research_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Seed Keyword: {seed_keyword}\n\n")
            f.write(f"Brand: {brand_context}\n\n")
            f.write(f"Funnel Stage: {funnel_stage}\n\n")
            f.write(f"Location: {target_location}\n\n")
            f.write("--- SEO REPORT ---\n\n")
            f.write(research)

        st.success("✅ SEO Report saved to seo_research_output.txt")

import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Content Brief Generator",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Content Brief Generator")
st.caption("Built by Kanya V · Content Strategist")
st.markdown("---")

# ── SECTION 1 — CONTENT INPUTS ──
st.markdown("### 📌 About Your Content")

topic = st.text_input(
    "What is your topic?",
    placeholder="e.g. how data helps content strategy"
)

why_searching = st.text_area(
    "Why are people really searching this right now?",
    placeholder="e.g. everyone is using AI blindly without measuring results...",
    height=100
)

reader_feeling = st.text_area(
    "What should the reader DO or FEEL after reading?",
    placeholder="e.g. feel confident they can use data without being a data scientist...",
    height=100
)

st.markdown("---")

# ── SECTION 2 — BRAND INPUTS ──
st.markdown("### 🏷️ About Your Brand")

brand_context = st.text_input(
    "Who is this content for?",
    placeholder="e.g. My personal brand — I'm a content strategist in marketing / "
                "Company brand — B2B cybersecurity company targeting IT managers"
)

st.caption("💡 AI will automatically detect the right tone from your brand context.")

st.markdown("---")

# ── SECTION 3 — AUDIENCE & GOAL ──
st.markdown("### 🎯 Audience & Goal")

col1, col2 = st.columns(2)

with col1:
    audience_level = st.selectbox(
        "Audience Knowledge Level",
        [
            "Complete Beginner",
            "Knows the Basics",
            "Advanced Professional"
        ]
    )

with col2:
    primary_goal = st.selectbox(
        "Primary Goal",
        [
            "Drive Traffic",
            "Get Shares & Virality",
            "Generate Leads",
            "Build Authority"
        ]
    )

content_length = st.selectbox(
    "Content Length",
    [
        "Quick Read (300–500 words)",
        "Medium (800–1200 words)",
        "Deep Dive (2000+ words)"
    ]
)

st.markdown("---")

# ── GENERATE BUTTON ──
if st.button("🚀 Generate My Content Brief", type="primary"):
    if not topic or not why_searching or not reader_feeling or not brand_context:
        st.warning("Please fill in all text fields!")
    else:
        with st.spinner("Researching competitors, analysing platform trends, building your brief..."):

            prompt = f"""
You are a friendly, experienced content consultant — like a smart friend who happens to be great at marketing.

You talk like a real person. No corporate jargon. No complicated words.
Write like you're sitting across from someone at a coffee shop, helping them plan their next piece of content.

The person you're helping has shared this:

TOPIC: {topic}
WHY PEOPLE ARE SEARCHING THIS: {why_searching}
WHAT READER SHOULD FEEL/DO: {reader_feeling}
BRAND CONTEXT: {brand_context}
AUDIENCE KNOWLEDGE LEVEL: {audience_level}
PRIMARY GOAL: {primary_goal}
CONTENT LENGTH: {content_length}

First figure out:
- Is this a personal brand or a company?
- What industry are they in?
- What tone suits them? Think about how they'd naturally talk to their audience.

Then help them with EXACTLY these sections.
Keep each section short — 4 to 5 lines max.
Use bullet points. Keep the language simple and warm.
Avoid words like: leverage, utilise, synergy, robust, paradigm, streamline.
Write like a smart human — not a robot.

---

## 🎨 BRAND & TONE
- Brand Type:
- Industry:
- Tone that fits them:
- Why this tone works: one simple sentence

---

## 🔍 WHAT'S ALREADY OUT THERE
Here's what others have already written on this topic — so you know what to avoid:
- [Title] — [Website] — [what angle they took, in plain English]
(list 4 examples)

---

## 🎯 YOUR ANGLE — WHAT NOBODY ELSE IS SAYING
This is the gap in the market. This is what YOU can own.
Be very specific. 2-3 lines. Plain language.

---

## 📱 WHERE TO POST THIS
Pick exactly 2 platforms. For each one say:
- Platform:
- Format: (video / carousel / article / post)
- Why this works here right now: one line in plain English

---

## 🔑 KEYWORDS TO USE
6 keywords people are actually searching for right now.
Format:
- keyword — why people search this (3 words max)

---

## 👥 WHO'S READING THIS
3 types of people who will read this, based on: {audience_level}
Format:
- Who they are — what's frustrating them right now

---

## 🪝 OPENING HOOKS
2 options for opening lines that make someone stop scrolling.
Keep them punchy. Max 2 lines each.
Should sound like: {brand_context}

---

## 💡 WHY WILL PEOPLE SHARE THIS?
3 real reasons someone would forward this to a friend or colleague.
Keep it honest and specific.
Tied to goal: {primary_goal}

---

## 📊 WHERE THIS FITS IN THE FUNNEL
Is this Awareness / Consideration / Decision content?
One sentence explaining why — in plain English.

---

## 📢 WHAT SHOULD THE READER DO NEXT?
2 options — one gentle, one more direct.
Should match the goal: {primary_goal}
- Soft nudge:
- Direct ask:

---

## 💬 SIMPLE EXAMPLE TO EXPLAIN THIS TOPIC
One analogy that anyone — even your grandma — would understand.
Max 3 lines. Keep it fun and relatable.
Match the knowledge level: {audience_level}

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
        st.markdown("### 📋 Your Content Brief")
        st.markdown(brief)

        # Save to file
        with open("content_brief_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Topic: {topic}\n\n")
            f.write(f"Brand: {brand_context}\n\n")
            f.write(f"Why searching: {why_searching}\n\n")
            f.write(f"Reader feeling: {reader_feeling}\n\n")
            f.write(f"Audience level: {audience_level}\n\n")
            f.write(f"Primary goal: {primary_goal}\n\n")
            f.write(f"Content length: {content_length}\n\n")
            f.write("--- BRIEF ---\n\n")
            f.write(brief)

        st.success("✅ Brief saved to content_brief_output.txt")

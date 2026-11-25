import sys
from datetime import date
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from gemini_helper import ask_gemini, sidebar_settings  # noqa: E402

st.set_page_config(page_title="Daily Marketing Updates", page_icon="📰", layout="wide")
api_key, model = sidebar_settings()

st.title("📰 Daily Updates for Marketers")
st.caption(f"Today: {date.today():%A, %d %B %Y} · Live from Google Search, summarised by Gemini")

TOPICS = {
    "🤖 Google + AI": "Google's AI announcements that affect marketers: Gemini, AI Overviews, AI Mode, "
                      "Google Ads/Performance Max AI features, Search Console or Analytics AI features.",
    "🔎 Google + SEO": "Google Search and SEO news: core/spam/helpful-content updates, ranking changes, "
                       "Search Console changes, Search Central announcements, statements from Google "
                       "(Search Liaison, John Mueller), changes to SERP features.",
    "📱 Social media": "Social platform updates that affect marketers: YouTube (Google-owned), Instagram, "
                       "Facebook, LinkedIn, X, Threads, TikTok, Pinterest: new features, algorithm changes, "
                       "ad product changes, policy changes.",
}

PROMPT = """Today is {today}. Use Google Search to find the most recent news on: {topic}

Rules:
- Only include real items you found. Prefer the last 24-48 hours; if there is little, widen to the last 7 days
  and label each item with its date.
- Prefer primary sources (Google blogs, platform announcements) and reputable trade press
  (Search Engine Land, Search Engine Journal, Social Media Today, The Verge).
- Do not invent anything. If nothing notable happened, say so plainly.

Give 4-6 items, newest first. For each item use exactly this format:

### <headline>
**Date:** <date> · **Source:** <publication>
**What happened:** <2 plain sentences>
**Why it matters to a marketer:** <1-2 sentences>
**What to do:** <one concrete action, or "Nothing yet, just watch">

End with a section "## TL;DR" of 3 bullets."""


@st.cache_data(ttl=3600, show_spinner=False)
def fetch(topic_key, day, key, model_name):
    # `day` is part of the cache key so the digest refreshes daily; ttl refreshes hourly.
    return ask_gemini(key, model_name, PROMPT.format(today=day, topic=TOPICS[topic_key]),
                      grounded=True, temperature=0.2)


if not api_key:
    st.info("Add your Gemini API key in the sidebar to start.")
    st.stop()

b1, b2 = st.columns([1, 1])
get_all = b1.button("⚡ Get today's updates (all 3)", type="primary")
refresh = b2.button("🔄 Force refresh")
if refresh:
    fetch.clear()

tabs = st.tabs(list(TOPICS.keys()))
if get_all or refresh:
    st.session_state["news_loaded"] = True

for tab, name in zip(tabs, TOPICS):
    with tab:
        if st.session_state.get("news_loaded"):
            with st.spinner(f"Fetching {name}..."):
                try:
                    text, sources = fetch(name, str(date.today()), api_key, model)
                    st.markdown(text)
                    if sources:
                        with st.expander("🔗 Sources"):
                            for s in sources:
                                st.markdown(f"- [{s['title']}]({s['url']})")
                except Exception as e:
                    st.error(f"Could not fetch: {e}")
        else:
            if st.button(f"Load {name} only", key=f"one_{name}"):
                st.session_state["news_loaded"] = True
                st.rerun()
            st.write("Click **Get today's updates** above.")

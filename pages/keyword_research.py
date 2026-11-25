import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from gemini_helper import ask_gemini, parse_json, sidebar_settings  # noqa: E402

st.set_page_config(page_title="Keyword Research", page_icon="🔍", layout="wide")
api_key, model = sidebar_settings()

st.title("🔍 Keyword Research")
st.caption("Give a domain. Get a keyword set built for what you're actually doing with it.")

# ── INPUTS ──
c1, c2 = st.columns([2, 1])
with c1:
    domain = st.text_input("Domain", placeholder="example.com")
    topic = st.text_input("Seed topic / product (optional)",
                          placeholder="e.g. project management software for agencies")
with c2:
    mode = st.radio("What is this for?", ["📝 Blog content", "🎯 On-page (a specific page)"])
    country = st.text_input("Target country", value="India")

page_type, page_url = None, None
if mode.startswith("🎯"):
    p1, p2 = st.columns(2)
    with p1:
        page_type = st.selectbox("Page type", ["Homepage", "Service page", "Product page",
                                               "Category page", "Landing page", "Pricing page"])
    with p2:
        page_url = st.text_input("Page URL or what the page is about (optional)")

count = st.slider("How many keywords?", 10, 40, 20)
use_search = st.checkbox("Look at the live site + SERPs with Google Search (slower, better)", value=True)

# ── PROMPTS ──
BLOG_PROMPT = """You are a senior SEO strategist. Domain: {domain}. Seed topic: {topic}. Country: {country}.
{research}
Build a BLOG keyword set of {count} keywords. Focus on informational and early-commercial intent,
long-tail phrases and questions this domain can realistically rank for. Group into 3-5 topic clusters.
Return ONLY JSON:
{{"summary": "2 sentences on the opportunity",
 "keywords": [{{"keyword": "", "cluster": "", "intent": "Informational|Commercial|Transactional|Navigational",
   "funnel": "TOFU|MOFU|BOFU", "difficulty": "Low|Medium|High", "volume_estimate": "Low|Medium|High",
   "blog_title": "", "angle": "one line on how to make it different from what ranks"}}]}}"""

ONPAGE_PROMPT = """You are a senior on-page SEO specialist. Domain: {domain}. Page type: {page_type}.
Page URL / description: {page_url}. Seed topic: {topic}. Country: {country}.
{research}
Build an ON-PAGE keyword plan for this single page: 1 primary keyword, then {count} supporting keywords
(secondary, semantic/LSI, and modifiers) with commercial or transactional intent. Return ONLY JSON:
{{"summary": "2 sentences on the strategy",
 "primary": {{"keyword": "", "why": ""}},
 "title_tag": "max 60 chars", "meta_description": "max 155 chars", "h1": "",
 "h2_ideas": ["", ""],
 "keywords": [{{"keyword": "", "role": "Secondary|Semantic|Modifier|Question/FAQ", "intent": "",
   "difficulty": "Low|Medium|High", "volume_estimate": "Low|Medium|High",
   "placement": "Title|H1|H2|Body|FAQ|Alt text|URL"}}]}}"""

RESEARCH = ("First research the domain with Google Search: what it sells/publishes and who ranks "
            "for its likely topics. Base keywords on that.")

# ── RUN ──
if st.button("Generate keywords", type="primary", disabled=not (domain and api_key)):
    is_blog = mode.startswith("📝")
    tmpl = BLOG_PROMPT if is_blog else ONPAGE_PROMPT
    prompt = tmpl.format(domain=domain, topic=topic or "infer from the domain", country=country,
                         count=count, page_type=page_type, page_url=page_url or "infer from the domain",
                         research=RESEARCH if use_search else "")
    with st.spinner("Researching..."):
        try:
            text, sources = ask_gemini(api_key, model, prompt, grounded=use_search)
            st.session_state["kw_result"] = (is_blog, parse_json(text), sources)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
if not api_key:
    st.info("Add your Gemini API key in the sidebar to start.")

# ── OUTPUT ──
if "kw_result" in st.session_state:
    is_blog, data, sources = st.session_state["kw_result"]
    st.markdown("---")
    st.markdown(f"**{data.get('summary', '')}**")

    if not is_blog:
        pr = data.get("primary", {})
        st.success(f"🎯 Primary keyword: **{pr.get('keyword', '')}** — {pr.get('why', '')}")
        a, b = st.columns(2)
        a.markdown(f"**Title tag**\n\n{data.get('title_tag', '')}")
        b.markdown(f"**Meta description**\n\n{data.get('meta_description', '')}")
        st.markdown(f"**H1:** {data.get('h1', '')}")
        st.markdown("**H2 ideas:** " + " · ".join(data.get("h2_ideas", [])))

    df = pd.DataFrame(data.get("keywords", []))
    if not df.empty:
        if is_blog and "cluster" in df:
            for cluster, grp in df.groupby("cluster"):
                with st.expander(f"📂 {cluster} ({len(grp)})", expanded=True):
                    st.dataframe(grp.drop(columns=["cluster"]), use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name=f"keywords_{'blog' if is_blog else 'onpage'}.csv", mime="text/csv")

    st.caption("⚠️ Difficulty and volume are AI estimates, not real data. Validate your shortlist in "
               "Google Search Console, Keyword Planner, Ahrefs or Semrush before committing.")
    if sources:
        with st.expander("Sources Gemini looked at"):
            for s in sources:
                st.markdown(f"- [{s['title']}]({s['url']})")

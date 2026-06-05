import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Social Media Performance Analyser",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Social Media Performance Analyser")
st.caption("Built by Kanya V · Content Strategist")
st.markdown("---")

# ── GOAL METRIC MAPPING ──
goal_config = {
    "Brand Awareness": {
        "primary_metric": "Impressions",
        "secondary_metric": "Views",
        "focus": "reach and visibility",
        "tip": "High impressions = LinkedIn pushed your content wide. Focus on what topics got pushed."
    },
    "Audience Engagement": {
        "primary_metric": "Engagement rate",
        "secondary_metric": "Likes",
        "focus": "reactions and interactions",
        "tip": "High engagement rate = audience found it worth reacting to. Focus on emotional or opinion topics."
    },
    "Drive Traffic to Website": {
        "primary_metric": "Clicks",
        "secondary_metric": "Click through rate (CTR)",
        "focus": "clicks and CTR",
        "tip": "High CTR = your hook compelled people to click. Focus on curiosity-gap headlines."
    },
    "Generate Leads": {
        "primary_metric": "Follows",
        "secondary_metric": "Clicks",
        "focus": "follows and conversions",
        "tip": "Follows = people trusted you enough to want more. Focus on credibility and value posts."
    },
    "Build Authority": {
        "primary_metric": "Reposts",
        "secondary_metric": "Comments",
        "focus": "shares and discussions",
        "tip": "Reposts = audience trusted your content enough to share. Focus on bold opinions and insights."
    }
}

# ── SECTION 1 — CONTEXT ──
st.markdown("### 🏷️ About Your Page")

col1, col2 = st.columns(2)
with col1:
    brand_context = st.text_input(
        "What is your brand/page about?",
        placeholder="e.g. Personal brand — Content Strategist posting about AI and marketing"
    )
with col2:
    content_goal = st.selectbox(
        "What was your content goal?",
        list(goal_config.keys())
    )

# Show goal tip
config = goal_config[content_goal]
st.info(f"**Your goal: {content_goal}** — Primary metric: **{config['primary_metric']}** | {config['tip']}")

st.markdown("---")

# ── SECTION 2 — FILE UPLOAD ──
st.markdown("### 📂 Upload Your LinkedIn Analytics")

uploaded_file = st.file_uploader(
    "Upload your LinkedIn Analytics file",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, skiprows=1)
    elif uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, skiprows=1, engine="xlrd")
    else:
        df = pd.read_excel(uploaded_file, skiprows=1, engine="openpyxl")

    # Clean
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["Post title"])

    # Parse dates
    df["Created date"] = pd.to_datetime(df["Created date"], errors="coerce")

    # Flag recent posts
    today = datetime.now()
    df["Is Recent"] = df["Created date"].apply(
        lambda x: (today - x).days < 7 if pd.notnull(x) else False
    )

    # Clean numeric columns
    for col in ["Impressions", "Views", "Clicks", "Likes",
                "Comments", "Reposts", "Follows", "Engagement rate",
                "Click through rate (CTR)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Short titles
    df["Short Title"] = df["Post title"].str[:35] + "..."

    # ── DYNAMIC CATEGORY BASED ON GOAL ──
    primary = config["primary_metric"]
    
    # Use Impressions + primary metric for categorisation
    imp_median = df["Impressions"].median()
    
    # Handle missing primary metric
    if primary not in df.columns:
        primary = "Engagement rate"
    
    primary_median = df[primary].median()

    def categorise(row):
        high_imp = row["Impressions"] >= imp_median
        high_primary = row[primary] >= primary_median
        if high_imp and high_primary:
            return "🎯 Sweet Spot"
        elif high_imp and not high_primary:
            return "⚠️ Reach but No Connect"
        elif not high_imp and high_primary:
            return "💎 Hidden Gem"
        else:
            return "💀 Invisible"

    df["Category"] = df.apply(categorise, axis=1)

    # Recent posts warning
    recent_posts = df[df["Is Recent"] == True]
    if len(recent_posts) > 0:
        st.warning(f"⚠️ **{len(recent_posts)} post(s) were created in the last 7 days.** Low engagement on these is completely normal — LinkedIn takes time to distribute new content.")

    st.markdown("---")

    # Metric explanation
    with st.expander("📖 What do these metrics mean?"):
        st.markdown(f"""
        | Metric | What it means | Important for your goal? |
        |---|---|---|
        | **Impressions** | How many times post appeared in feed | {'⭐ Primary' if primary == 'Impressions' else '✅ Always relevant'} |
        | **Views** | How many people stopped and looked | {'⭐ Primary' if primary == 'Views' else '—'} |
        | **Clicks** | How many people clicked your link | {'⭐ Primary' if primary == 'Clicks' else '—'} |
        | **Likes** | Direct appreciation | {'⭐ Primary' if primary == 'Likes' else '—'} |
        | **Comments** | Worth responding to | {'⭐ Primary' if primary == 'Comments' else '—'} |
        | **Reposts** | Worth sharing — highest trust signal | {'⭐ Primary' if primary == 'Reposts' else '—'} |
        | **Follows** | Trusted you enough to follow | {'⭐ Primary' if primary == 'Follows' else '—'} |
        | **Engagement Rate** | Overall performance score | {'⭐ Primary' if primary == 'Engagement rate' else '✅ Always relevant'} |
        | **CTR** | Hook compelled people to click | {'⭐ Primary' if primary == 'Click through rate (CTR)' else '—'} |
        
        ⭐ = Most important for your goal: **{content_goal}**
        """)

    st.markdown("---")

    # ════════════════════════════════
    # GRAPH 1 — PRIMARY METRIC BY GOAL
    # ════════════════════════════════
    st.markdown(f"### 📊 {primary} by Post — Your Goal: {content_goal}")

    fig1 = px.bar(
        df.sort_values(primary, ascending=False),
        x="Short Title",
        y=primary,
        color=primary,
        color_continuous_scale="Teal",
        hover_name="Post title",
        labels={"Short Title": "Post", primary: primary},
    )
    fig1.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig1, use_container_width=True)

    # Graph 1 Insights
    top_post = df.loc[df[primary].idxmax()]
    bottom_post = df.loc[df[primary].idxmin()]
    avg_primary = df[primary].mean()

    st.markdown(f"#### 💡 {primary} Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"""
        **🏆 Best for {content_goal}**
        {top_post['Post title'][:50]}...
        {primary}: **{top_post[primary]:.2f}**
        """)
    with col2:
        st.error(f"""
        **⚠️ Lowest {primary}**
        {bottom_post['Post title'][:50]}...
        {primary}: **{bottom_post[primary]:.2f}**
        """)
    with col3:
        st.info(f"""
        **📊 Average {primary}**
        Across all {len(df)} posts
        Average: **{avg_primary:.2f}**
        """)

    st.markdown("---")

    # ════════════════════════════════
    # GRAPH 2 — IMPRESSIONS OVER TIME
    # ════════════════════════════════
    st.markdown("### 📈 Impressions Over Time")

    df_sorted = df.sort_values("Created date")
    fig2 = px.line(
        df_sorted,
        x="Created date",
        y="Impressions",
        markers=True,
        hover_name="Post title",
        labels={"Created date": "Date", "Impressions": "Impressions"},
        color_discrete_sequence=["#00b4d8"]
    )
    fig2.update_layout(height=350)
    st.plotly_chart(fig2, use_container_width=True)

    # Graph 2 Insights
    best_imp_post = df.loc[df["Impressions"].idxmax()]
    worst_imp_post = df.loc[df["Impressions"].idxmin()]

    first_half = df_sorted.head(len(df_sorted)//2)["Impressions"].mean()
    second_half = df_sorted.tail(len(df_sorted)//2)["Impressions"].mean()

    if second_half > first_half * 1.1:
        trend = "📈 Growing — your reach is improving over time"
        trend_color = "success"
    elif second_half < first_half * 0.9:
        trend = "📉 Declining — your reach has dropped recently"
        trend_color = "error"
    else:
        trend = "➡️ Inconsistent — no clear growth pattern yet"
        trend_color = "info"

    st.markdown("#### 💡 Impression Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"""
        **📈 Most Reached Post**
        {best_imp_post['Post title'][:50]}...
        Impressions: **{int(best_imp_post['Impressions'])}**
        Date: {best_imp_post['Created date'].strftime('%d %b %Y')}
        """)
    with col2:
        st.error(f"""
        **📉 Least Reached Post**
        {worst_imp_post['Post title'][:50]}...
        Impressions: **{int(worst_imp_post['Impressions'])}**
        Date: {worst_imp_post['Created date'].strftime('%d %b %Y')}
        """)
    with col3:
        if trend_color == "success":
            st.success(f"**📊 Overall Trend**\n{trend}")
        elif trend_color == "error":
            st.error(f"**📊 Overall Trend**\n{trend}")
        else:
            st.info(f"**📊 Overall Trend**\n{trend}")

    st.markdown("---")

    # ════════════════════════════════
    # GRAPH 3 — CONTENT DIAGNOSTIC
    # ════════════════════════════════
    st.markdown(f"### 🎯 Content Diagnostic — Impressions vs {primary}")

    color_map = {
        "🎯 Sweet Spot": "#00b4d8",
        "⚠️ Reach but No Connect": "#f77f00",
        "💎 Hidden Gem": "#06d6a0",
        "💀 Invisible": "#ef233c"
    }

    fig3 = px.scatter(
        df,
        x="Impressions",
        y=primary,
        color="Category",
        color_discrete_map=color_map,
        hover_name="Post title",
        size="Clicks" if "Clicks" in df.columns else None,
        size_max=30,
        labels={
            "Impressions": "Impressions",
            primary: primary,
            "Category": "Post Category"
        }
    )

    fig3.add_hline(
        y=primary_median,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg {primary}"
    )
    fig3.add_vline(
        x=imp_median,
        line_dash="dash",
        line_color="gray",
        annotation_text="Avg Impressions"
    )
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)

    # Graph 3 Category Insights
    sweet_spot = df[df["Category"] == "🎯 Sweet Spot"]
    reach_no_connect = df[df["Category"] == "⚠️ Reach but No Connect"]
    hidden_gems = df[df["Category"] == "💎 Hidden Gem"]
    invisible = df[df["Category"] == "💀 Invisible"]

    st.markdown("#### 💡 Content Category Insights")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success(f"""
        **🎯 Sweet Spot**
        {len(sweet_spot)} posts
        High reach + High {primary}
        Your best performing content
        """)
        for _, row in sweet_spot.iterrows():
            st.markdown(f"• {row['Post title'][:35]}...")

    with col2:
        st.warning(f"""
        **⚠️ Reach but No Connect**
        {len(reach_no_connect)} posts
        People saw it — didn't act
        Wrong hook or audience fit
        """)
        for _, row in reach_no_connect.iterrows():
            st.markdown(f"• {row['Post title'][:35]}...")

    with col3:
        st.info(f"""
        **💎 Hidden Gems**
        {len(hidden_gems)} posts
        Low reach but high {primary}
        Boost these — they work!
        """)
        for _, row in hidden_gems.iterrows():
            st.markdown(f"• {row['Post title'][:35]}...")

    with col4:
        st.error(f"""
        **💀 Invisible**
        {len(invisible)} posts
        Low reach + Low {primary}
        Rethink topic or format
        """)
        for _, row in invisible.iterrows():
            st.markdown(f"• {row['Post title'][:35]}...")

    st.markdown("---")

    # ════════════════════════════════
    # SEPARATE INSIGHTS SECTION
    # ════════════════════════════════
    st.markdown("### 🔍 Deep Insights")

    # Insight 1 — High Impressions Low Engagement
    st.markdown("#### ⚠️ High Reach, Low Connection — What Went Wrong?")

    if len(reach_no_connect) > 0:
        for _, row in reach_no_connect.iterrows():
            with st.expander(f"⚠️ {row['Post title'][:60]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Impressions", int(row["Impressions"]))
                with col2:
                    st.metric(primary, f"{row[primary]:.2f}")
                with col3:
                    st.metric("Clicks", int(row.get("Clicks", 0)))

                st.markdown(f"""
                **📅 Posted:** {row['Created date'].strftime('%d %b %Y')}

                **🔍 What this means:**
                LinkedIn pushed this post to many people — but they scrolled past.

                **Possible reasons:**
                - Hook didn't stop the scroll
                - Topic felt mismatched with your audience
                - Content format didn't suit the platform
                - No clear reason to engage (no question, no CTA)

                **✅ What to try next time:**
                - Rewrite the opening line — make it provocative or surprising
                - Check if this topic fits YOUR LinkedIn audience
                - Add a direct question at the end to invite comments
                """)
    else:
        st.success("✅ No high reach + low engagement posts found. Great job!")

    st.markdown("---")

    # Insight 2 — Hidden Gems
    st.markdown("#### 💎 Hidden Gems — Underrated Posts Worth Boosting")

    if len(hidden_gems) > 0:
        for _, row in hidden_gems.iterrows():
            with st.expander(f"💎 {row['Post title'][:60]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Impressions", int(row["Impressions"]))
                with col2:
                    st.metric(primary, f"{row[primary]:.2f}")
                with col3:
                    st.metric("Clicks", int(row.get("Clicks", 0)))

                st.markdown(f"""
                **📅 Posted:** {row['Created date'].strftime('%d %b %Y')}

                **🔍 What this means:**
                This post resonated strongly with the people who saw it —
                but not enough people saw it.

                **Why this happens:**
                - Posted at a low traffic time
                - Not enough early engagement to trigger LinkedIn algorithm
                - Topic is niche but highly relevant to your core audience

                **✅ How to amplify this:**
                - Repost this with a new angle or updated hook
                - Turn it into a carousel for better reach
                - Write a longer version as a LinkedIn article
                - This topic clearly works — create a series around it
                """)
    else:
        st.info("No hidden gems found in this data set.")

    st.markdown("---")

    # Insight 3 — Recent Posts Flag
    if len(recent_posts) > 0:
        st.markdown("#### 🆕 Recently Posted — Too Early to Judge")
        for _, row in recent_posts.iterrows():
            with st.expander(f"🆕 {row['Post title'][:60]}..."):
                st.markdown(f"""
                **📅 Posted:** {row['Created date'].strftime('%d %b %Y')}

                **🔍 What this means:**
                This post is less than 7 days old.
                LinkedIn typically takes 3–7 days to fully distribute content.
                Low numbers now do NOT mean this post failed.

                **✅ What to do:**
                - Check back in 7 days
                - Respond to any comments quickly — it signals LinkedIn to push further
                - Do not repost yet — give it time
                """)

    st.markdown("---")

    # ── FULL TABLE ──
    st.markdown("### 📋 Full Performance Table")

    display_df = df[[
        "Post title", "Created date", "Impressions",
        "Views", "Clicks", "Likes", "Comments",
        "Reposts", "Engagement rate", "Category", "Is Recent"
    ]].copy()

    display_df["Created date"] = display_df["Created date"].dt.strftime("%d %b %Y")
    display_df["Is Recent"] = display_df["Is Recent"].apply(
        lambda x: "🆕 Too new" if x else ""
    )
    display_df = display_df.sort_values(primary, ascending=False)

    st.dataframe(display_df, use_container_width=True)

    st.markdown("---")

    # ── AI ANALYSIS ──
    if st.button("🤖 Generate AI Analysis & Recommendations", type="primary"):
        if not brand_context:
            st.warning("Please fill in your brand context first!")
        else:
            with st.spinner("Generating your personalised analysis..."):

                top5 = df.nlargest(5, primary)[
                    ["Post title", "Created date", "Impressions",
                     "Engagement rate", "Clicks", primary, "Category"]
                ].to_string(index=False)

                bottom5 = df[df["Is Recent"] == False].nsmallest(5, primary)[
                    ["Post title", "Created date", "Impressions",
                     "Engagement rate", "Clicks", primary, "Category"]
                ].to_string(index=False)

                reach_no_connect_titles = reach_no_connect["Post title"].tolist()
                hidden_gem_titles = hidden_gems["Post title"].tolist()

                prompt = f"""
You are a friendly social media consultant — like a smart friend who has spent years 
analysing content performance and knows how to explain data simply.

You talk like a real person. No corporate jargon. No complicated words.
Write like you're sitting with a marketer, going through their data together over coffee.
Be honest. Be specific. Be helpful.

Avoid words like: leverage, utilise, robust, synergy, paradigm, actionable insights.
Use less emojis — only where they genuinely help, not everywhere.
Keep sentences short. One idea per line.

This marketer's goal is: {content_goal}
The metric that matters most for this goal is: {primary}
Their brand: {brand_context}

Here's their top performing content:
{top5}

Here's their weakest content (excluding posts less than 7 days old):
{bottom5}

Posts that got seen but nobody engaged with:
{reach_no_connect_titles}

Posts that didn't get much reach but people loved when they saw it:
{hidden_gem_titles}

Now help them understand what's working, what's not, and what to do next.
Keep each section to 4 points maximum.
Each point maximum one line.
Always reference actual post titles — don't be vague.
Frame everything around their goal: {content_goal}

---

WHY YOUR BEST POSTS WORKED

For each top post — one clear reason why it served the goal: {content_goal}
Be specific. Name the post. Explain in plain English.

---

WHY YOUR WEAKEST POSTS MISSED

For each weak post — one honest reason why it didn't work for the goal.
Be direct but kind. Name the post.

---

POSTS PEOPLE SAW BUT DIDN'T ENGAGE WITH — WHAT HAPPENED?

For each post in the "reached but no connect" list:
- What likely went wrong in one sentence
- One simple fix they can try next time

---

HIDDEN GEMS — POSTS WORTH BRINGING BACK

For each hidden gem post:
- Why it resonated with people who saw it
- One idea for how to give it more reach

---

WHAT'S CONSISTENTLY WORKING

4 patterns you can see across the data.
Be specific — what topics, formats, or styles keep performing?

---

STOP DOING THIS

3 things the data clearly shows are not working.
Be honest. One line each. No fluff.

---

DO MORE OF THIS

3 specific things they should do more of.
Tied directly to the goal: {content_goal}
One line each.

---

IDEAS FOR FUTURE CONTENT

4 content ideas based on what's working.
Format:
- Idea — why this will work based on the data

---

SUMMARY FOR YOUR CEO OR MANAGER

5 lines maximum. 
Professional but plain English.
Cover: what worked, what didn't, and the one most important thing to change.
Ready to copy and paste into a report.

---
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                analysis = response.text  # or research/analysis
            except Exception:
                st.error("⚠️ AI analysis is temporarily busy. Please try again in a few minutes.")
                st.stop()
                
            st.markdown("---")
            st.markdown("### 🤖 AI Analysis & Recommendations")
            st.markdown(analysis)

            with open("social_analysis_report.txt", "w", encoding="utf-8") as f:
                f.write(f"Brand: {brand_context}\n\n")
                f.write(f"Goal: {content_goal}\n\n")
                f.write(f"Primary Metric: {primary}\n\n")
                f.write("--- REPORT ---\n\n")
                f.write(analysis)

            st.success("✅ Report saved to social_analysis_report.txt")

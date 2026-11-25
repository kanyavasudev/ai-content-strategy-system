import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from gemini_helper import ask_gemini, sidebar_settings  # noqa: E402
from meta_logic import DESC_MAX, TITLE_MAX, fetch_page, generate_meta  # noqa: E402

st.set_page_config(page_title="Bulk Meta Generator", page_icon="🏷️", layout="wide")
api_key, model = sidebar_settings()

st.title("🏷️ Bulk Meta Title & Description Generator")
st.caption(f"Upload a CSV of URLs. Get titles (≤{TITLE_MAX} chars) and descriptions (≤{DESC_MAX} chars) back as a CSV.")

TEMPLATE = "url,keyword\nhttps://example.com/blog/seo-tips,seo tips for beginners\nhttps://example.com/services,content marketing services\n"
st.download_button("⬇️ Download CSV template", TEMPLATE, file_name="meta_template.csv", mime="text/csv")

up = st.file_uploader("Your CSV", type=["csv"])

if up:
    df = pd.read_csv(up)
    cols = list(df.columns)
    guess = next((c for c in cols if c.strip().lower() in ("url", "address", "page", "landing page", "urls")), cols[0])

    c1, c2, c3 = st.columns(3)
    url_col = c1.selectbox("Which column has the URLs?", cols, index=cols.index(guess))
    kw_col = c2.selectbox("Target keyword column (optional)", ["(none)"] + cols,
                          index=(cols.index("keyword") + 1) if "keyword" in cols else 0)
    max_rows = c3.number_input("Rows to process", 1, 300, min(len(df), 50),
                               help="Start small to check quality, then run more.")

    d1, d2, d3 = st.columns(3)
    brand = d1.text_input("Brand name to add to titles (optional)", placeholder="e.g. Acme")
    tone = d2.selectbox("Tone", ["clear and helpful", "professional", "friendly", "persuasive", "playful"])
    language = d3.text_input("Language", value="English")
    read_pages = st.checkbox("Read each live page first (better results, slower)", value=True)

    st.caption(f"{len(df)} rows found. Preview:")
    st.dataframe(df.head(5), use_container_width=True, hide_index=True)

    if st.button("Generate", type="primary", disabled=not api_key):
        sub = df.head(int(max_rows))
        rows = []
        bar = st.progress(0.0, text="Reading pages...")
        for n, (_, r) in enumerate(sub.iterrows()):
            url = str(r[url_col]).strip()
            info = fetch_page(url) if read_pages else {"fetched": False}
            rows.append({"url": url, "keyword": "" if kw_col == "(none)" or pd.isna(r[kw_col]) else str(r[kw_col]),
                         **info})
            bar.progress((n + 1) / len(sub) * 0.3, text=f"Reading pages... {n + 1}/{len(sub)}")

        def ask(prompt):
            return ask_gemini(api_key, model, prompt, grounded=False, temperature=0.5)[0]

        def progress(p):
            bar.progress(0.3 + p * 0.7, text="Writing meta tags...")

        try:
            st.session_state["meta_out"] = pd.DataFrame(
                generate_meta(rows, ask, brand=brand, tone=tone, language=language, progress=progress))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
        bar.empty()

if not api_key:
    st.info("Add your Gemini API key in the sidebar to start.")

if "meta_out" in st.session_state:
    out = st.session_state["meta_out"]
    ok = (out["status"] == "OK").sum()
    st.markdown("---")
    st.success(f"{ok} of {len(out)} rows passed all length checks.")
    st.dataframe(out, use_container_width=True, hide_index=True,
                 column_config={"description": st.column_config.TextColumn(width="large")})
    st.download_button("⬇️ Download results CSV", out.to_csv(index=False).encode("utf-8"),
                       file_name="meta_results.csv", mime="text/csv")
    st.caption("Lengths are counted in characters. Google actually cuts by pixel width, so wide letters "
               "(W, M) can truncate slightly earlier. Rows marked 'URL only' were written from the web "
               "address alone because the page could not be read, so check those first.")

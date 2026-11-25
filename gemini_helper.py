"""Shared Gemini helpers for all pages.

API key lookup order:
1. st.secrets["GEMINI_API_KEY"]  (.streamlit/secrets.toml or Streamlit Cloud secrets)
2. GEMINI_API_KEY environment variable
3. The key typed in the sidebar
"""
import json
import os
import re

import streamlit as st
from google import genai
from google.genai import types

try:  # lets the app read GEMINI_API_KEY from your existing .env file
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DEFAULT_MODEL = "gemini-2.5-flash"


def sidebar_settings():
    """Render the sidebar (API key + model). Returns (api_key, model)."""
    with st.sidebar:
        st.markdown("### ⚙️ Gemini settings")
        key = ""
        try:
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
        key = key or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            key = st.text_input("Gemini API key", type="password",
                                help="Get one free at aistudio.google.com")
        else:
            st.success("API key loaded ✅")
        model = st.text_input("Model", value=DEFAULT_MODEL)
    return key, model


def ask_gemini(api_key, model, prompt, grounded=False, temperature=0.4):
    """Call Gemini. If grounded=True it uses live Google Search.

    Returns (text, sources) where sources is a list of {"title", "url"}.
    """
    client = genai.Client(api_key=api_key)
    tools = [types.Tool(google_search=types.GoogleSearch())] if grounded else None
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(tools=tools, temperature=temperature),
    )
    text = resp.text or ""

    sources, seen = [], set()
    try:
        meta = resp.candidates[0].grounding_metadata
        for chunk in (meta.grounding_chunks or []):
            web = chunk.web
            if web and web.uri not in seen:
                seen.add(web.uri)
                sources.append({"title": web.title or web.uri, "url": web.uri})
    except Exception:
        pass
    return text, sources


def parse_json(text):
    """Pull the first JSON object/array out of a model reply."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    starts = [i for i in (text.find("{"), text.find("[")) if i != -1]
    if not starts:
        raise ValueError("No JSON found in model reply")
    start = min(starts)
    end = max(text.rfind("}"), text.rfind("]"))
    return json.loads(text[start:end + 1])

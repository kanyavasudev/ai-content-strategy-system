"""Logic for the bulk meta generator (no Streamlit in here, so it is easy to test).

Rule: Gemini WRITES the text, Python COUNTS the characters.
"""
import json
import re

import requests
from bs4 import BeautifulSoup

TITLE_MAX = 60
DESC_MIN, DESC_MAX = 120, 155
UA = {"User-Agent": "Mozilla/5.0 (compatible; MetaGeneratorBot/1.0)"}


def fetch_page(url, timeout=8):
    """Read the live page: current title, meta description, H1 and some body text."""
    out = {"current_title": "", "current_description": "", "h1": "", "snippet": "", "fetched": False}
    try:
        r = requests.get(url, headers=UA, timeout=timeout)
        if r.status_code != 200:
            return out
        soup = BeautifulSoup(r.text, "html.parser")
        out["current_title"] = (soup.title.string or "").strip() if soup.title else ""
        md = soup.find("meta", attrs={"name": "description"})
        out["current_description"] = (md.get("content") or "").strip() if md else ""
        h1 = soup.find("h1")
        out["h1"] = h1.get_text(" ", strip=True) if h1 else ""
        paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        out["snippet"] = " ".join(p for p in paras if len(p) > 40)[:700]
        out["fetched"] = bool(out["h1"] or out["current_title"] or out["snippet"])
    except Exception:
        pass
    return out


def _parse_json(text):
    text = re.sub(r"```(?:json)?", "", text).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list in reply")
    return json.loads(text[start:end + 1])


def issues(title, desc, title_max):
    problems = []
    if not title:
        problems.append("missing title")
    elif len(title) > title_max:
        problems.append(f"title {len(title)} chars (max {title_max})")
    if not desc:
        problems.append("missing description")
    elif len(desc) > DESC_MAX:
        problems.append(f"description {len(desc)} chars (max {DESC_MAX})")
    elif len(desc) < DESC_MIN:
        problems.append(f"description {len(desc)} chars (min {DESC_MIN})")
    return problems


def _prompt(items, title_max, tone, language, feedback=None):
    fb = ""
    if feedback:
        fb = ("\nThese were REJECTED for length. Rewrite them to fit. Previous attempts and problems:\n"
              + json.dumps(feedback, ensure_ascii=False))
    return f"""You are an SEO copywriter. Write a unique meta title and meta description for each page below.
Language: {language}. Tone: {tone}.

HARD RULES (count characters carefully):
- title: at most {title_max} characters. Put the target keyword near the start. No clickbait, no ALL CAPS.
- description: between {DESC_MIN} and {DESC_MAX} characters. Include the keyword naturally, say what the
  reader gets, end with a soft call to action. Do not repeat the title word for word.
- Use ONLY facts found in the page info. Never invent prices, awards, stats or claims.
- Every page must get different wording.
{fb}
Pages (JSON):
{json.dumps(items, ensure_ascii=False)}

Return ONLY a JSON list, one object per page: [{{"id": <id>, "title": "...", "description": "..."}}]"""


def _call(ask, items, title_max, tone, language, feedback=None):
    text = ask(_prompt(items, title_max, tone, language, feedback))
    return {int(o["id"]): o for o in _parse_json(text)}


def generate_meta(rows, ask, brand="", tone="clear and helpful", language="English",
                  batch_size=10, progress=None):
    """rows: list of dicts with url, keyword, current_title, h1, snippet, fetched.
    ask: function(prompt) -> text. Returns a list of result dicts, same order as rows."""
    suffix = f" | {brand.strip()}" if brand.strip() else ""
    title_max = TITLE_MAX - len(suffix)
    if title_max < 25:  # brand too long, skip it
        suffix, title_max = "", TITLE_MAX

    results = [None] * len(rows)

    def to_item(i):
        r = rows[i]
        return {"id": i, "url": r["url"], "target_keyword": r.get("keyword", ""),
                "current_title": r.get("current_title", ""), "h1": r.get("h1", ""),
                "page_text": r.get("snippet", "")}

    def store(i, o):
        t = (o.get("title") or "").strip()
        d = (o.get("description") or "").strip()
        results[i] = {"title_raw": t, "description": d}

    # pass 1
    for start in range(0, len(rows), batch_size):
        idx = list(range(start, min(start + batch_size, len(rows))))
        try:
            got = _call(ask, [to_item(i) for i in idx], title_max, tone, language)
            for i in idx:
                if i in got:
                    store(i, got[i])
        except Exception:
            pass
        if progress:
            progress(min(start + batch_size, len(rows)) / (len(rows) * 1.0) * 0.85)

    # pass 2: retry only the rows that break the limits
    bad = [i for i in range(len(rows))
           if results[i] is None or issues(results[i]["title_raw"], results[i]["description"], title_max)]
    for start in range(0, len(bad), batch_size):
        idx = bad[start:start + batch_size]
        fb = [{"id": i, "problems": issues(results[i]["title_raw"], results[i]["description"], title_max)
               if results[i] else ["no result"],
               "previous": results[i]} for i in idx]
        try:
            got = _call(ask, [to_item(i) for i in idx], title_max, tone, language, feedback=fb)
            for i in idx:
                if i in got:
                    store(i, got[i])
        except Exception:
            pass
    if progress:
        progress(1.0)

    final = []
    for i, r in enumerate(rows):
        res = results[i]
        if res is None:
            final.append({"url": r["url"], "keyword": r.get("keyword", ""), "title": "", "title_chars": 0,
                          "description": "", "description_chars": 0, "status": "Failed, try again",
                          "based_on": "Live page" if r.get("fetched") else "URL only"})
            continue
        title = res["title_raw"] + (suffix if res["title_raw"] and
                                    len(res["title_raw"]) <= title_max else "")
        probs = issues(title, res["description"], TITLE_MAX)
        final.append({"url": r["url"], "keyword": r.get("keyword", ""),
                      "title": title, "title_chars": len(title),
                      "description": res["description"], "description_chars": len(res["description"]),
                      "status": "OK" if not probs else "Check: " + "; ".join(probs),
                      "based_on": "Live page" if r.get("fetched") else "URL only"})
    return final

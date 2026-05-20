#!/usr/bin/env python3
import sys
import json
import re

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

for line in sys.stdin:
    try:
        post = json.loads(line)
        title = post.get("title", "")
        body = post.get("selftext", "")
        full_text = f"{title} {body}".strip()
        cleaned = clean_text(full_text)

        if len(cleaned) > 20:
            result = {
                "keyword": post.get("keyword"),
                "text": cleaned,
                "subreddit": post.get("subreddit"),
                "score": post.get("score"),
                "num_comments": post.get("num_comments"),
                "created_utc": post.get("created_utc")
            }
            print(json.dumps(result))
    except:
        continue


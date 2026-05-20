import json
import csv

with open("cleaned_reddit_data.json", "r") as f:
    data = [json.loads(line) for line in f if line.strip()]

with open("cleaned_full_data.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "keyword", "text", "subreddit", "score", "num_comments", "created_utc"])
    for i, post in enumerate(data):
        writer.writerow([
            i,
            post.get("keyword", ""),
            post.get("text", ""),
            post.get("subreddit", ""),
            post.get("score", 0),
            post.get("num_comments", 0),
            post.get("created_utc", 0)
        ])

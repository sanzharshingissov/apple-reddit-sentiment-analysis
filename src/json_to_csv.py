import json
import csv

# Load cleaned data
with open("cleaned_reddit_data.json", "r") as f:
    data = [json.loads(line) for line in f if line.strip()]

# Write to CSV (id + text only, for sentiment analysis)
with open("cleaned_data_for_sql.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text"])
    for i, post in enumerate(data):
        writer.writerow([i, post["text"]])

import json

with open("raw_reddit_data.json", "r") as f:
    data = json.load(f)

with open("raw_reddit_data_fixed.json", "w") as f:
    for post in data:
        f.write(json.dumps(post) + "\n")

import praw
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
print("Scraper started...")

# Reddit API credentials 
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# List of Apple-related keywords to search for
keywords = [
    "iPhone 16", "iPhone 16 Pro", "iPhone 16 Pro Max", "iPhone 16 Plus",
    "MacBook M3", "MacBook Air M3", "MacBook Pro M3",
    "AirPods Pro 2", "AirPods Pro", "AirPods 3", "AirPods Max",
    "Apple Vision Pro", "Vision Pro",
    "Apple Watch Series 9", "Apple Watch Ultra 2",
    "iOS 18", "macOS Sequoia", "Apple Intelligence",
    "Apple M4", "M4 chip", "Apple event 2024", "Apple software updates"
]

# List of relevant subreddits to collect posts from
subreddits = [
    "apple", "iphone", "mac", "macbook", "applewatch",
    "airpods", "ipad", "iOSBeta", "AppleWatch", "iOS", "VisionPro"
]

# Minimum date to include (e.g., May 1, 2024)
min_date = datetime(2024, 5, 1)
min_timestamp = time.mktime(min_date.timetuple())

# Prepare result list
all_results = []

# Loop through each subreddit and keyword
for subreddit_name in subreddits:
    print(f"\nSearching subreddit: r/{subreddit_name}")
    for keyword in keywords:
        print(f"  Keyword: {keyword}")
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.search(keyword, sort="new", time_filter="all", limit=10):
                if post.created_utc < min_timestamp:
                    print("    Skipped (too old)")
                    continue

                print(f"    Collected post: {post.title[:60]}")

                result = {
                    "keyword": keyword,
                    "title": post.title,
                    "selftext": post.selftext,
                    "subreddit": post.subreddit.display_name,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "created_utc": post.created_utc
                }
                all_results.append(result)
        except Exception as e:
            print(f"  Error in r/{subreddit_name} with keyword '{keyword}': {e}")

print(f"\nTotal collected posts: {len(all_results)}")

# Save results to JSON file
with open("reddit_apple_data.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("Saved to reddit_apple_data.json")


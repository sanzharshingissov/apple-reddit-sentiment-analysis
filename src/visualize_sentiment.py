import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the PostgreSQL database using credentials
conn = psycopg2.connect(
    dbname="reddit_apple",
    user="postgres",
    password="yourpassword",  
    host="localhost"
)

# Load keyword, subreddit, timestamp, and sentiment data for visualization
query = """
SELECT r.keyword, r.subreddit, r.created_utc, s.sentiment_score, s.sentiment_label
FROM reddit_full r
JOIN reddit_sentiment s ON r.id = s.id
"""
df = pd.read_sql(query, conn)
conn.close()

# Convert Unix timestamp to datetime for time-series operations
df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")

# ------------------------ 1. Pie Chart ------------------------
# Display sentiment distribution across all posts
sentiment_counts = df["sentiment_label"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=140)
plt.title("Sentiment Distribution (Pie Chart)")
plt.tight_layout()
plt.savefig("sentiment_pie_chart.png")
plt.close()

# ------------------------ 2. Bar Chart by Product ------------------------
# Show average sentiment score for each Apple product
avg_scores = df.groupby("keyword")["sentiment_score"].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_scores.values, y=avg_scores.index, palette="coolwarm")
plt.xlabel("Average Sentiment Score")
plt.title("Average Sentiment per Apple Product")
plt.tight_layout()
plt.savefig("avg_sentiment_by_product.png")
plt.close()

# ------------------------ 3. Countplot by Sentiment & Product ------------------------
# Filter only top 10 mentioned Apple keywords
top_keywords = df["keyword"].value_counts().head(10).index
filtered = df[df["keyword"].isin(top_keywords)]
plt.figure(figsize=(10, 6))
sns.countplot(data=filtered, y="keyword", hue="sentiment_label", palette="Set2")
plt.title("Sentiment Distribution by Top Apple Products")
plt.xlabel("Number of Posts")
plt.tight_layout()
plt.savefig("sentiment_by_keyword.png")
plt.close()

# ------------------------ 4. Line Plot — Sentiment Trend Over Time ------------------------
# Group posts weekly to avoid noisy daily fluctuations
df["week"] = df["created_utc"].dt.to_period("W").apply(lambda r: r.start_time)
weekly_avg = df.groupby("week")["sentiment_score"].mean()

# Smooth the line using centered rolling average (3 weeks)
smoothed = weekly_avg.rolling(window=3, center=True).mean()

plt.figure(figsize=(12, 6))
plt.plot(weekly_avg.index, weekly_avg.values, label="Weekly Avg Sentiment", linewidth=1.5, color="steelblue")
plt.plot(smoothed.index, smoothed.values, label="Smoothed (3-week Rolling Avg)", linewidth=2.5, color="crimson")
plt.title("Weekly Sentiment Trend Over Time")
plt.xlabel("Week")
plt.ylabel("Average Sentiment Score")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("smoothed_sentiment_trend.png")
plt.close()

# ------------------------ 5. Bar Chart — Sentiment by Subreddit ------------------------
# Subreddit can act as a proxy for platform/community differences
avg_by_subreddit = df.groupby("subreddit")["sentiment_score"].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_by_subreddit.values, y=avg_by_subreddit.index, palette="viridis")
plt.xlabel("Average Sentiment Score")
plt.title("Average Sentiment by Subreddit (Platform Proxy)")
plt.tight_layout()
plt.savefig("sentiment_by_subreddit.png")
plt.close()

print("All sentiment visualizations saved successfully.")


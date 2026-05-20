import psycopg2
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="reddit_apple",
    user="postgres",
    password="yourpassword",
    host="localhost"
)


# Load data from the full reddit table
df = pd.read_sql("SELECT id, text FROM reddit_full", conn)

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Compute sentiment score and label
df["sentiment_score"] = df["text"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
df["sentiment_label"] = df["sentiment_score"].apply(
    lambda score: "positive" if score > 0.2 else "negative" if score < -0.2 else "neutral"
)

# Create a new table to store sentiment results
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS reddit_sentiment;")
    cur.execute("""
        CREATE TABLE reddit_sentiment (
            id INTEGER PRIMARY KEY,
            sentiment_score REAL,
            sentiment_label TEXT
        );
    """)
    conn.commit()

# Insert sentiment results into the database
for _, row in df.iterrows():
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO reddit_sentiment (id, sentiment_score, sentiment_label) VALUES (%s, %s, %s)",
            (int(row["id"]), row["sentiment_score"], row["sentiment_label"])
        )
    conn.commit()

conn.close()
print("Sentiment analysis completed and saved to reddit_sentiment table.")

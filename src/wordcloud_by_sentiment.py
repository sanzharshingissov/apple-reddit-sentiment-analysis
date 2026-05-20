import psycopg2
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Connecting to the PostgreSQL db
conn = psycopg2.connect(
    dbname="reddit_apple",
    user="postgres",
    password="yourpassword",  
    host="localhost"
)

#joining the reddit_full and reddit_sentiment tables to get both the text and the sentiment label
query = """
SELECT r.text, s.sentiment_label
FROM reddit_full r
JOIN reddit_sentiment s ON r.id = s.id
"""
df = pd.read_sql(query, conn)
conn.close()

#directory to save all word clouds by sentiment category
output_dir = "wordclouds_by_sentiment"
os.makedirs(output_dir, exist_ok=True)

#separate word clouds for positive and negative posts only
for label in ["positive", "negative"]:
    # Filter all the texts that match the current sentiment label
    texts = df[df["sentiment_label"] == label]["text"].dropna().tolist()

    # If there are no posts for a label, skip it
    if not texts:
        continue

    # Combine all post texts into one string for word cloud generation
    combined_text = " ".join(texts)

    # Generate the word cloud using the combined text
    wc = WordCloud(width=1000, height=500, background_color="white").generate(combined_text)

    # Create a plot and export it as an image
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Word Cloud — {label.capitalize()} Posts", fontsize=14)
    plt.tight_layout()

    # Save the word cloud image to the folder
    filepath = os.path.join(output_dir, f"{label}_posts_wordcloud.png")
    plt.savefig(filepath)
    plt.close()

# Final confirmation message when word clouds are successfully generated
print(f"Word clouds for positive and negative posts saved to ./{output_dir}/")


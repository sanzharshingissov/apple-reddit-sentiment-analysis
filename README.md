# Apple Reddit Sentiment Analysis

This project analyzes Reddit discussions about Apple products using NLP-based sentiment analysis.

The pipeline collects Apple-related Reddit posts, cleans the text data, stores the results in CSV/PostgreSQL, applies sentiment analysis using VADER, and generates visualizations to compare public opinion across products, subreddits, and time.

## Features

- Reddit post collection using PRAW
- Text cleaning and preprocessing
- JSON to CSV conversion
- PostgreSQL data storage
- Sentiment analysis using NLTK VADER
- Product-level sentiment comparison
- Sentiment distribution analysis
- Weekly sentiment trend visualization
- Positive and negative word clouds

## Technologies Used

- Python
- PRAW
- pandas
- PostgreSQL
- psycopg2
- NLTK VADER
- matplotlib
- seaborn
- wordcloud
- python-dotenv

## Project Structure

```text
apple-reddit-sentiment-analysis/
│
├── data/
├── outputs/
├── src/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

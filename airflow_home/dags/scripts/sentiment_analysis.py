from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import duckdb

# Load the model and tokenizer
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define sentiment analysis function
def analyse_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment = torch.argmax(scores).item()  # 0: Negative, 1: Neutral, 2: Positive
    return sentiment

# Task 4: Perform sentiment analysis
def sentiment_analysis_task():
    
    # Connect to DuckDB
    conn = duckdb.connect('nyt_warehouse.db')
    # Fetch article headlines
    query = "SELECT article_id, headline FROM nyt_articles;"
    df = conn.execute(query).fetchdf()

    # Map sentiment categories
    def map_sentiment(sentiment):
        return {0: "Negative", 1: "Neutral", 2: "Positive"}[sentiment]

    # Apply sentiment analysis
    df['sentiment'] = df['headline'].apply(lambda x: map_sentiment(analyse_sentiment(x)))

    # Update database with sentiment
    for _, row in df.iterrows():
        conn.execute("""
            UPDATE nyt_articles
            SET sentiment = ?
            WHERE article_id = ?;
        """, [row['sentiment'], row['article_id']])
    # Commit and close connection
    conn.close()
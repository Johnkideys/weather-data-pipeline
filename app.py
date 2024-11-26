import streamlit as st
import duckdb

# Connect to DuckDB
conn = duckdb.connect('nyt_warehouse.db')

# Query the total number of articles
total_articles_query = "SELECT COUNT(*) AS total_articles FROM nyt_articles;"
total_articles_result = conn.execute(total_articles_query).fetchdf()

# Query sentiment counts
sentiment_query = """
    SELECT sentiment, COUNT(*) AS count
    FROM nyt_articles
    GROUP BY sentiment
    ORDER BY sentiment;
"""
sentiment_result = conn.execute(sentiment_query).fetchdf()

# Query recent articles
recent_articles_query = "SELECT headline, pub_date, section, sentiment \
    FROM nyt_articles ORDER BY pub_date DESC LIMIT 10;"
recent_articles = conn.execute(recent_articles_query).fetchdf()

# Streamlit app
st.title("NYT Climate Change Articles Dashboard")

# Display total articles
st.subheader(f"Total Articles: {total_articles_result['total_articles'][0]}")

# Display sentiment analysis results
st.subheader("Sentiment Analysis Overview")
st.bar_chart(sentiment_result.set_index("sentiment"))

# Display recent articles
st.subheader("Recent Articles")
st.dataframe(recent_articles)

# Close the database connection
conn.close()

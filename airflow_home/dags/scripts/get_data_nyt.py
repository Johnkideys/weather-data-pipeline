import requests
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import pandas as pd

#import duckdb


# Load environment variables from .env
load_dotenv()  

# Access the environment variables
api_key = os.getenv("API_KEY")
bucket_name = os.getenv("BUCKET_NAME")

def get_news_call():
    # Calculate the dates for the api call
    end_date = datetime.today()
    begin_date = end_date - timedelta(days=2)  # Roughly 3 months ago

    # Format the dates in the required YYYYMMDD format for NYT API
    begin_date_str = begin_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    # Define the base URL for the NYT Article Search API
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    # Define parameters for the API request
    params = {
        "q": "climate change",  # Search query for "climate change"
        "api-key": api_key,  # Replace with your actual API key
        "begin_date": begin_date_str,  # Start date (3 months ago)
        "end_date": end_date_str,  # End date (today)
        "sort": "newest",  # Sort results by newest first
    }

    # Make the GET request to the API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json()['response']['docs']
        # orig = response.json()
        # # Convert to DataFrame
        # df = pd.json_normalize(articles)
        #return df, orig
        rows = []
        for article in articles:
            rows.append({
                'article_id': article['_id'],
                'pub_date': article['pub_date'],
                'headline': article['headline']['main'],
                'lead_paragraph': article.get('lead_paragraph', ''),
                'section': article.get('section_name', ''),
                'subsection': article.get('subsection_name', ''),
                'web_url': article['web_url'],
                'keywords': ', '.join([kw['value'] for kw in article.get('keywords', [])]),
                'word_count': article.get('word_count', 0)
            })
        return pd.DataFrame(rows)
    
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

# Test the fetch function
# df, orig = get_news_call()
# df = get_news_call()

# #print(df.head())
# # Print all column names for easier inspection
# print("\nColumn Names:")
# print(df.columns.tolist())
# # Print the original JSON response
# print("Top-level keys in the JSON response:")
# print(json.dumps(orig, indent=4))  # Nicely formatted JSON

# # # Save the DataFrame to a CSV file for easier viewing
# output_path = 'nyt_articles_info.csv'
# df.to_csv(output_path, index=False)
#print(f"Data has been saved to {output_path}.")



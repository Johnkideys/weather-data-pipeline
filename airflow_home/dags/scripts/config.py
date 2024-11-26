import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Weather and News Sentiment Correlation

## Real Aim: 
Learn data engineering skills, especially using the Google Cloud Platform.

## Aim: 
Check the sentiment of articles (positive, negative) and analyze their correlation with weather.

## Possible Tech Stack:
- Apache Airflow
- Docker
- Terraform
- PostgreSQL
- Streamlit or Flask

## High-Level Workflow:
1. Get weather data for the next 8 days and store it in a data warehouse.
2. Fetch historical weather data.
3. Get NYT API articles (or other news sources) and analyze their sentiment.
4. Join the weather data and article sentiment based on the date.
5. Analyze the correlation between weather and sentiment.

## Step 1: Setting Up the Tech Stack

### 1.1. Installing Apache Airflow Locally
Airflow is the orchestration tool that will help manage the workflow between data collection, sentiment analysis, and storage.

```bash
# Install Apache Airflow with Google support
pip install apache-airflow[google]

# Initialize the Airflow Database
airflow db init
```

At this point I've decided to use Docker as its beneficial:
for isolating the environment for airflow configuration
and easy to then run this project from any laptop for other developers

After creating the docker-compose.yml file (that ChaGPT gave) I ran:
```
docker-compose up --build
```
Many problems occured in these steps, needed to produce a fernet key for the 
AIRFLOW__CORE__FERNET_KEY in the   airflow-webserver: of docker-compose.yml

Decided to leave docker for now and come back to it. Its time consuming to run 
build docker each time after making chnage to the code, so Ill just set up 
airflow in my project folder and get that running. And do the docker later as 
its more of a package manager thing anyway. 

So with airflow:
Get data via api - some intermediate transformation? - then upload to bucket -
use spark for another transformation,nlp? - output to streamlit dahsboard or 
flask or bigquery ?

export AIRFLOW_HOME=/Users/johnkideys/Desktop/learning/DataEngineering/projects/weather_project/airflow_home
Need to set this each time in terminal so thta airflow knows to look at the correct airflow home driectory and not the one in users-home!
 echo $AIRFLOW_HOME:
 with this can check if its looking ta correct path
 Also cant aseem to opne postgres app, couyld be bec home directory airflow is using postgres(?)

 To activate the venv: pyenv activate nyt_articles_pyenv




Ive decided to use postgres rather than the default airflkow databasse sqlite,
so download postgres from terminal:
- brew install postgresql
- brew services start postgresql
- psql -U postgres # postgres interactive terminal
- CREATE DATABASE airflow;
- CREATE USER airflow WITH PASSWORD 'airflow';
- GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
Update the sql_alchemy_conn parameter under the [core] section to use PostgreSQL:
[core]
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
Make sure the PostgreSQL driver is installed for Python
- pip install psycopg2-binary





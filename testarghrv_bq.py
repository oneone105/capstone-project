import os
from pymongo import MongoClient
from google.cloud import bigquery

# from dotenv import load_dotenv
# import pandas as pd
# import json

client = MongoClient('localhost', 27017)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./tecky-capstone-project-15a2a04d016f.json"
bq_client = bigquery.Client()

db = client.worldcup

# load_dotenv()


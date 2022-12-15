import tweepy
from dotenv import load_dotenv
import os
import pandas as pd
from pymongo import MongoClient
from google.cloud import bigquery
import json

client = MongoClient('localhost', 27017)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./tecky-capstone-project-15a2a04d016f.json"
bq_client = bigquery.Client()

db = client.worldcup

load_dotenv()
# jpn_vs_hrv = bq_client.get_table('tecky-capstone-project.worldcup.jpn_hrv')
eng_fra = bq_client.get_table('tecky-capstone-project.worldcup.eng_fra')

engfra2 = db.engfra2.find() # Use Pymongo access collection "jh"
for row in engfra2:
    # row['_id'] = str(row['_id']) # "_id" is default obeject and not json serializable, need to stringify it first
    # row['Date_Created'] = (row['created_at']) # "Date_Created" is default datetime format, need to change it (should use datetime format instead)
    bq_client.insert_rows_json(eng_fra,[row]) # insert to BQ


# jh = db.jh.find() # Use Pymongo access collection "jh"
# for row in jh:
#     row['_id'] = str(row['_id']) # "_id" is default obeject and not json serializable, need to stringify it first
#     row['Date_Created'] = str(row['Date_Created']) # "Date_Created" is default datetime format, need to change it (should use datetime format instead)
#     bq_client.insert_rows_json(jpn_vs_hrv,[row]) # insert to BQ
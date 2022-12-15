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

tweepy_client = tweepy.Client(os.getenv('BEARER_TOKEN'), wait_on_rate_limit=True)

query = '#ENG OR #FRA -is:retweet'

paginator = tweepy.Paginator(tweepy_client.search_recent_tweets, 
                        query=query,
                        tweet_fields = ['author_id', 'created_at', 'source', 'lang', 'geo', 'public_metrics', 'entities', 'context_annotations', 'attachments'], 
                        media_fields = ['preview_image_url', 'media_key', 'type', 'url'],
                        expansions = ['author_id', 'attachments.media_keys'], 
                        start_time = '2022-12-10T00:00:00.000Z',
                        end_time = '2022-12-12T00:00:00.000Z',
                        max_results = 100
                        )

for page in paginator:
    
    users = {u["id"]: u for u in page.includes['users']}
    media = {m["media_key"]: m for m in page.includes['media']}

    for tweet in page.data:

        if users[tweet.author_id]:
            user = users[tweet.author_id]
        
        tweet_content = {
            "tweet_id": tweet.id,
            "author": user,
            "created_at": tweet.created_at,
            "source": tweet.source,
            "lang": tweet.lang,
            "geo": tweet.geo,
            "retweet": tweet.public_metrics,
            "entites": tweet.entities,
            "text": tweet.text
        }
        
        db.engfra2.insert_one(tweet_content)

eng_vs_fra = bq_client.get_table('tecky-capstone-project.worldcup.eng_fra')

engfra2 = db.engfra2.find() # Use Pymongo access collection "jh"

for row in engfra2:
    row['_id'] = str(row['_id']) # "_id" is default object and not json serializable, need to stringify it first
    row['Date_Created'] = str(row['created_at']) # "Date_Created" is default datetime format, need to change it (should use datetime format instead)
    bq_client.insert_rows_json(eng_fra,[row]) # insert to BQ
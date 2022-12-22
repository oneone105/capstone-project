import tweepy
from dotenv import load_dotenv
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.worldcup

load_dotenv()

tweepy_client = tweepy.Client(os.getenv('BEARER_TOKEN'), wait_on_rate_limit=True)

# query = '#ARG OR #FRA'
query = '#ARGFRA OR #FRAARG'


paginator = tweepy.Paginator(tweepy_client.search_recent_tweets, 
                        query=query,
                        tweet_fields = ['author_id', 'created_at', 'source', 'lang', 'geo', 'public_metrics', 'entities', 'context_annotations', 'attachments'], 
                        expansions = ['author_id'],
                        start_time = '2022-12-18T13:00:00.000Z',
                        end_time = '2022-12-18T20:00:00.000Z',
                        max_results = 100
                        )

for page in paginator:
    
    users = {u["id"]: u for u in page.includes['users']}

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
            "public_metrics": tweet.public_metrics,
            "entities": tweet.entities,
            "text": tweet.text
        }
        
        db.favf.insert_one(tweet_content)

print("db import completed")
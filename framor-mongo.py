import tweepy
from dotenv import load_dotenv
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.worldcup

load_dotenv()

tweepy_client = tweepy.Client(os.getenv('BEARER_TOKEN'), wait_on_rate_limit=True)

query = '#FRA OR #MAR OR France OR Morocco OR #FRAMAR OR #MARFRA'





paginator = tweepy.Paginator(tweepy_client.search_recent_tweets, 
                        query=query,
                        tweet_fields = ['author_id', 'created_at', 'source', 'lang', 'geo', 'public_metrics', 'entities', 'context_annotations', 'attachments'], 
                        expansions = ['author_id'],
                        start_time = '2022-12-14T17:00:00.000Z',
                        end_time = '2022-12-14T23:00:00.000Z',
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
            "entites": tweet.entities,
            "text": tweet.text
        }
        
        db.fravsmar.insert_one(tweet_content)

# engfra2 = bq_client.get_table('tecky-capstone-project.worldcup.eng_fra')

# engfra2 = db.engfra2.find() # Use Pymongo access collection "jh"

# for row in engfra2:
#     row['_id'] = str(row['_id']) # "_id" is default object and not json serializable, need to stringify it first
#     row['created_at'] = str(row['created_at']) # "Date_Created" is default datetime format, need to change it (should use datetime format instead)
#     bq_client.insert_rows_json(engfra2,[row]) # insert to BQ
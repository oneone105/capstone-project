from pymongo import MongoClient
import os
from google.cloud import bigquery
import unicodedata

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./tecky-capstone-project-15a2a04d016f.json"
bq_client = bigquery.Client()

client = MongoClient('localhost', 27017)
db = client.worldcup

tweets_db = db.fravsmar.find()

# arghrv_name = bq_client.get_table('tecky-capstone-project.worldcup.arghrv_name')
framor_name = bq_client.get_table('tecky-capstone-project.worldcup.framor_name')

# -----------------------------------------------------------------------


for tweet in tweets_db:
    try:
        if tweet.get('entities'):
            if tweet['entities'].get('annotations'):
                for anno in tweet['entities']['annotations']:
                    if anno['type'] == "Person":
                        person = anno['normalized_text']
                        names = person.split(" ")
                        if len(names) == 1:
                            name = names[0]
                        else:
                            name = names[len(names)-1]
                        
                        name = name.lower()
                        name = name.capitalize()
                        name = unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode()
                        content = {
                            "tweet_id": tweet['tweet_id'],
                            "name": name
                        }
                        bq_client.insert_rows_json(framor_name,[content])
                    

    except ValueError as e:
        print(e)

print("framor_name upload success!")
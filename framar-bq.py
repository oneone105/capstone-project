from dotenv import load_dotenv
import os
from pymongo import MongoClient
from google.cloud import bigquery

client = MongoClient('localhost', 27017)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./tecky-capstone-project-15a2a04d016f.json"
bq_client = bigquery.Client()
load_dotenv()
db = client.worldcup
# tweets_db = db.engvsfra.find()
tweets_db = db.fravsmar.find()
# eng_vs_fra = bq_client.get_table('tecky-capstone-project.worldcup.eng_vs_fra')
sf-framar = bq_client.get_table('tecky-capstone-project.worldcup.sf-framar')

for tweet in tweets_db:
    # print(tweet)
    # isRetweet
    try:
        isRetweet = False
        if ("RT" in tweet['text']):
            isRetweet = True

        hashtags = []
        annotations = []
        annotations_person = []
        url = "None"
        xurl = "None"
        durl = "None"
        media_key = "None"

        # entities
        if tweet.get('entities'):    

            # hashtags
            if tweet['entities'].get['hashtags']:
                for hashtag in tweet['entities']['hashtags']:
                    hashtags.append(hashtag['tag'])

            # #annotations
            if tweet['entities'].get['annotations']:
                for anno in tweet['entities']['annotations']:
                    if anno['type'] == "Person":
                        annotations_person.append(anno['normalized_text'])
                    else:
                        annotations.append(f'({anno["type"]}) {anno["normalized_text"]}')
            
            if tweet['entities'].get['url']:
                url = tweet['entities']['urls'][0]['url']
                xurl = tweet['entities']['urls'][0]['expanded_url']
                durl = tweet['entities']['urls'][0]['display_url']
                media_key = tweet['entities']['urls'][0].get['media_key']

        content = {
            "tweet_id": tweet['tweet_id'],
            "author_id": tweet['author']['id'],
            "author_name": tweet['author']['name'],
            "author_username": tweet['author']['username'],
            "created_at": str(tweet['created_at']),
            "source": tweet['source'],
            "lang": tweet['lang'],
            "geo": tweet['geo'],
            "is_retweet": isRetweet,
            "num_retweet": tweet['public_metrics']['retweet_count'],
            "num_reply": tweet['public_metrics']['reply_count'],
            "num_like": tweet['public_metrics']['like_count'],
            "num_quote": tweet['public_metrics']['quote_count'],
            "hashtags": ",".join(hashtags),
            "annotations": ", ".join(annotations),
            "annotations_person": ", ".join(annotations_person),
            "url": url,
            "expanded_url": xurl,
            "display_url": durl,
            "media_key": media_key,
            "text": tweet['text']
        }
        # bq_client.insert_rows_json(eng_vs_fra,[content])
        bq_client.insert_rows_json(sf-framar,[content])

    except ValueError as e:
        print(e)

print("sucess")

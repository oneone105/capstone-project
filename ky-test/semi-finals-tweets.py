import tweepy

import json
import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from timeit import default_timer as timer


import pymongo
from pymongo import MongoClient



# Variables that contains the credentials to access Twitter API
# credentials
ACCESS_TOKEN = 'XXXXX'
ACCESS_SECRET = 'XXXXX'
CONSUMER_KEY = 'XXXX'
CONSUMER_SECRET = 'XXXX'


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api


# Create API object
api = connect_to_twitter_OAuth()

hashtag = "#semi-finals"
limit =300

tweets = tweepy.Cursor(api.search_tweets, q=hashtag,
                      count=100, tweet_mode='extended').items(limit)


#Pulling Some attributes from the tweet
attributes_container = [[tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.source,  tweet.full_text] for tweet in tweets]

#Creation of column list to rename the columns in the dataframe
columns = ["Date_Created", "Number_of_Likes", 'retweets_count', "Source_of_Tweet", "Tweet"]

#Creation of Dataframe
tweets_df = pd.DataFrame(attributes_container, columns=columns)


tweets_df


# ### Text cleaning with NLTK
### Set Stopwords
#stopwords = set(stopwords.words('english'))


#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

def clean_tweets(tweet):
 
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
#after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
#replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
#remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
#filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
#looping through conditions
    for w in word_tokens:
#check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)return tweet



tweets_df['clean_tweet'] = tweets_df['Tweet'].apply(clean_tweets)


tweets_df.head()


tweets_df.to_csv('semi_finals_tweets.csv', index=False)


# ### Store data in a mongodb
# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017/")
# database
db = client["tweets_database"]
# collection
tweets = db["semi_finals_tweets"]


## convert data to dictionary

data_dict = tweets_df.to_dict("records")

tweets.insert_one({"index":"semi-finals-tweets", "data" :data_dict})


# ### Load data from mongoDB


data_from_db = tweets.find_one({"index":"semi-finals-tweets"})
df = pd.DataFrame(data_from_db["data"])
df.head()

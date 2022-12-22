#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#installing modules
get_ipython().system('pip install tweepy')
get_ipython().system('pip install textblob')
nltk.download('vader_lexicon')
get_ipython().system('pip install wordcloud')


# In[ ]:


#Importing modules
import pandas as pd
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import re
import nltk
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# Scraping tweets

# In[ ]:


client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAGe%2BkQEAAAAA5T6U0eMNYZKzypB%2FALTy3C6tId0%3DJXqwPg3V48Xh0S1owFVWMzgRsbzeWWxeB1QxRG88SaUNqdms1U')


# In[ ]:


#Scraping Argentina
query = '#Argentina lang:en'


# In[ ]:


#Scraping France
query = '#France lang:en'


# In[ ]:


#Scraping Croatia
query = '#Croatia lang:en'


# In[ ]:


#Scraping Morocco
query = '#Morocco lang:en'


# In[ ]:


paginator = tweepy.Paginator(
client.search_recent_tweets,   
query=query,                   
max_results=100,               
limit=10                       
)


# In[ ]:


tweet_list = []
for tweet in paginator.flatten(): 
    tweet_list.append(tweet)
    print(tweet)


# In[ ]:


tweet_list_df = pd.DataFrame(tweet_list)
tweet_list_df = pd.DataFrame(tweet_list_df['text'])
tweet_list_df.head(5)


# In[ ]:


def preprocess_tweet(sen):
    '''Cleans text data up, leaving only 2 or more char long non-stepwords composed of A-Z & a-z only in lowercase'''
    sentence = sen.lower()
    # Remove RT
    sentence = re.sub('RT @\w+: '," ", sentence)
    # Remove punctuations and numbers
    sentence = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", sentence)
    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    # Remove multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence) 
    return sentence


# In[ ]:


cleaned_tweets = []
for tweet in tweet_list_df['text']:
    cleaned_tweet = preprocess_tweet(tweet)
    cleaned_tweets.append(cleaned_tweet)
tweet_list_df['cleaned'] = pd.DataFrame(cleaned_tweets)
tweet_list_df.head(5)


# In[ ]:


#Calculating Negative, Positive, Neutral and Compound values
tweet_list_df[['polarity', 'subjectivity']] = tweet_list_df['cleaned'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tweet_list_df['cleaned'].iteritems():
    # Should use on English only
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    if comp <= -0.05:
        tweet_list_df.loc[index, 'sentiment'] = "negative"
    elif comp >= 0.05:
        tweet_list_df.loc[index, 'sentiment'] = "positive"
    else:
        tweet_list_df.loc[index, 'sentiment'] = "neutral"
    
    tweet_list_df.loc[index, 'neg'] = neg
    tweet_list_df.loc[index, 'neu'] = neu
    tweet_list_df.loc[index, 'pos'] = pos
    tweet_list_df.loc[index, 'compound'] = comp
tweet_list_df.head(5)


# In[ ]:


#Creating new dataframes for all sentiments (positive, negative and neutral)
tweet_list_df_negative = tweet_list_df[tweet_list_df["sentiment"]=="negative"]
tweet_list_df_positive = tweet_list_df[tweet_list_df["sentiment"]=="positive"]
tweet_list_df_neutral = tweet_list_df[tweet_list_df["sentiment"]=="neutral"]


# In[ ]:


#Function for count_values_in single columns
def count_values_in_column(data,feature):
    total = data.loc[:,feature].value_counts(dropna=False)
    percentage = round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])
#Count_values for sentiment
count_values_in_column(tweet_list_df,"sentiment")


# In[ ]:


#Calculating tweet's lenght and word count
tweet_list_df['text_len'] = tweet_list_df['cleaned'].astype(str).apply(len)
tweet_list_df['text_word_count'] = tweet_list_df['cleaned'].apply(lambda x: len(str(x).split()))

round(pd.DataFrame(tweet_list_df.groupby("sentiment").text_len.mean()),2)
round(pd.DataFrame(tweet_list_df.groupby("sentiment").text_word_count.mean()),2)


# In[ ]:


#Saving to CSV
tweet_list_df.to_csv('Argentina')


# In[ ]:


#Saving to CSV
tweet_list_df.to_csv('France')


# In[ ]:


#Saving to CSV
tweet_list_df.to_csv('Croatia')


# In[ ]:


#Saving to CSV
tweet_list_df.to_csv('Morocco')


# In[ ]:


def load_table_to_bigquery(df,
                           table_name,
                           dataset_id):

    dataset_id = dataset_id 

    dataset_ref = bigquery_client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.write_disposition = "WRITE_TRUNCATE"

    upload_table_name = f"{dataset_id}.{table_name}"
    
    load_job = bigquery_client.load_table_from_dataframe(df,
                                                         upload_table_name,
                                                         job_config = job_config)
        
    print(f"completed job {load_job}")


# In[ ]:


load_table_to_bigquery(df=tweet_list_df.astype(str), 
                       table_name="tweet_list_df", 
                       dataset_id=dataset_id)


# In[ ]:





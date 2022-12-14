import tweepy
# import config

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHpVkAEAAAAAoz0I1wJvxqkJ7%2FC5Xq%2BwNEjkxL0%3D5sGjIl1aeKe4CpipNCH6E6PjUUPESDHzxPIOQsWntRMq7cZ3pZ"

client = tweepy.Client(BEARER_TOKEN)

query = '#FifaWorldCup -is:retweet'

# file_name='tweeetsJPN.csv'

# response = client.search_recent_tweets(query=query,max_results=10, tweet_fields=['created_at', 'lang'],expansion=['author_id'])

# users= for u in response.includes 
# print(response)

counts = client.get_recent_tweets_count(query=query, granularity='day')

for count in counts.data:
    print(count)
import tweepy
# import config

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHpVkAEAAAAAoz0I1wJvxqkJ7%2FC5Xq%2BwNEjkxL0%3D5sGjIl1aeKe4CpipNCH6E6PjUUPESDHzxPIOQsWntRMq7cZ3pZ"

client = tweepy.Client(BEARER_TOKEN)

query = '#FifaWorldCup -is:retweet'

counts = client.get_recent_tweets_count(query=query, granularity='day')

for count in counts.data:
    print(count)
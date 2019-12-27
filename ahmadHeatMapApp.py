import os
import tweepy as tw
import pandas as pd

#Keys set as envinronment variables for security purposes
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")

#OAuth authetication/configuration
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Post a tweet from Python (commented out)
# api.update_status("Look, I'm tweeting from #Python using the twitter API!")

#Define search term and date since as variables
search_word = "#wildfires"
date_since = "2018-11-10"

#Defining most_recent_count (number of mmost recent tweets to display)
most_recent_count = 10

#Collecting tweets, using .Cursor(), that contain the specified search terms 
tweets = tw.Cursor(api.search,
              q=search_word,
              lang="en",
              since=date_since).items(most_recent_count)
              
#Iterate over and print tweets 
for tweet in tweets:
    print(tweet.text)
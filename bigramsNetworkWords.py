import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re

import warnings
warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

#Keys set as envinronment variables for security purposes
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")

#OAuth authetication/configuration
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#Define search term and date since as variables
search_word = "#climate+change"
filtered_search_word = search_word + " -filter:retweets"
date_since = "2018-11-10"

#Defining most_recent_count (number of most recent tweets to collect)
#and most common words number
most_recent_count = 1000
most_common_words = 15
def main():
    #Collecting tweets, using .Cursor(), that contain the specified search terms 
    tweets = tw.Cursor(api.search,
                q=filtered_search_word,
                lang="en",
                since=date_since).items(most_recent_count)

    #Remove URL's from tweets
    tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in tweets_no_urls]

    #Downloading stopwords for additional cleanup
    nltk.download('stopwords')
    
    #Stop words are words that do not add meaningful information
    #to the text being analyzed
    stop_words = set(stopwords.words('english'))

    # Remove stop words from each tweet list of words
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                for tweet_words in words_in_tweet]
    
    #Putting the collection words in a list
    collection_words = ['climatechange', 'climate', 'change']

    #Removing collection words from words in tweets
    #Words should have no stop words and no collection words in them after
    tweets_nsw_nc = [[w for w in word if not w in collection_words]
                    for word in tweets_nsw]

def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


if __name__ == '__main__':
    main()
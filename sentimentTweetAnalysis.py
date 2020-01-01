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
import networkx
from textblob import TextBlob

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
most_common_bigrams = 30
def main():
    #Collecting tweets, using .Cursor(), that contain the specified search terms 
    tweets = tw.Cursor(api.search,
                q=filtered_search_word,
                lang="en",
                since=date_since).items(most_recent_count)

    #Remove URL's from tweets
    tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]

    # Create textblob objects of the tweets
    sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]

    print(sentiment_objects[0].polarity)
    print(sentiment_objects[0])

    # Create list of polarity valuesx and tweet text
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

    print(sentiment_values[0])

    # Create dataframe containing the polarity value and tweet text
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

    print(sentiment_df)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot histogram of the polarity values
    sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
                ax=ax,
                color="blue")

    plt.title("Sentiments from Tweets on Climate Change")
    plt.show()

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
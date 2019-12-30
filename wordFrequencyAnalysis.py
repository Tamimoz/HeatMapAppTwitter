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
search_word = "climate+change"
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

    all_tweets = [tweet.text for tweet in tweets]

    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

    # List of all words across tweets, flatten the original list
    # to put all the words into one list
    all_words_no_urls = list(itertools.chain(*words_in_tweet))

    # Create counter
    counts_no_urls = collections.Counter(all_words_no_urls)

    print(counts_no_urls.most_common(most_common_words))

    # Creating a dataframe for analysis and plotting
    clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(most_common_words), columns=['words', 'count'])
    print(clean_tweets_no_urls)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot horizontal bar graph
    clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
                        y='count',
                        ax=ax,
                        color="purple")

    ax.set_title("Common Words Found in Tweets (Including All Words)")

    plt.show()

    #Downloading stopwords for additional cleanup
    nltk.download('stopwords')
    
    #Stop words are words that do not add meaningful information
    #to the text being analyzed
    stop_words = set(stopwords.words('english'))

    # Remove stop words from each tweet list of words
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                for tweet_words in words_in_tweet]
    
    #flattening the list and creating a counter for most common words
    all_words_nsw = list(itertools.chain(*tweets_nsw))

    counts_nsw = collections.Counter(all_words_nsw)

    print(counts_nsw.most_common(most_common_words))

    # Creating a dataframe for analysis and plotting
    clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(most_common_words), columns=['words', 'count'])
    print(clean_tweets_nsw)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot horizontal bar graph
    clean_tweets_nsw.sort_values(by='count').plot.barh(x='words',
                        y='count',
                        ax=ax,
                        color="blue")

    ax.set_title("Common Words Found in Tweets (Without Stop Words)")

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
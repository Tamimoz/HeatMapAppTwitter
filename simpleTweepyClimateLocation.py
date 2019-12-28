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
search_word = "climate+change"
date_since = "2018-11-10"

#Defining most_recent_count (number of mmost recent tweets to display)
most_recent_count = 10

#Collecting tweets, using .Cursor(), that contain the specified search terms 
tweets = tw.Cursor(api.search,
              q=search_word,
              lang="en",
              since=date_since).items(most_recent_count)
              

print("Before the retweet filter:\n")

user_locations= []
#Iterate over and print tweets and append locations to a list
for tweet in tweets:
    print(tweet.text +" tweeted on: " + str(tweet.created_at))
    if tweet.user.location != '':
        user_locations.append(tweet.user.location)

print("Locations of user tweets: \n" + str(user_locations))

#putting all of the location data (unfiltered) in a data frame and then printing it
tweet_text_location_table = pd.DataFrame(data=user_locations, columns=["Location"])
print(tweet_text_location_table)

#Editing the search word with a retweet filter
filtered_search = search_word + " -filter:retweets"

#Collecting tweets with a specified search term with a retweet filter
filtered_tweets = tw.Cursor(api.search, 
                        q=filtered_search,
                        lang="en",
                        since_date=date_since).items(most_recent_count)

print("\n\nAfter the retweet filter:\n")

filtered_user_locations = []
#Iterate over and print tweets 
for tweet in filtered_tweets:
    print(tweet.text+" tweeted on: " + str(tweet.created_at))
    if tweet.user.location != '':
        filtered_user_locations.append(tweet.user.location)
print("Locations of filtered user tweets: \n" + str(filtered_user_locations))

#putting all of the location data (filtered) in a data frame and then printing it
filtered_tweet_text_location_table = pd.DataFrame(data=filtered_user_locations, columns=["Location"])
print(filtered_tweet_text_location_table)



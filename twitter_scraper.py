import snscrape.modules.twitter as sntwitter
import snscrape.modules.facebook as snfacebook
import pandas as pd
import numpy as np
import pickle
from pandas import json_normalize

def getNamedTweets(keyword, start_date, end_date):
    tweets_list1 = []
    text_filter = keyword + ' since:' + start_date + ' until:' + end_date
    print(text_filter)

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(text_filter).get_items()

):
        
        tweets_list1.append([tweet.date, tweet.username, tweet.id, tweet.content, tweet.url, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.quotedTweet, tweet.mentionedUsers, tweet.outlinks]) #declare the attributes to be returned

    # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Username', 'Tweet Id', 'Text', 'URL', 'replyCount', 'retweetCount', 'likeCount', 'quoteCount', 'isQuoted', 'Mentioned Users', 'Links']

)
    
    return tweets_df1
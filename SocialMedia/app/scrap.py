#imports
from pymongo import MongoClient
import tweepy
import pytumblr

#assets from twitter API
class Twitter:
    consumer_key = "Oz0zSQ533RXS9jRhynoDBCBBl"
    consumer_secret = "HXtH1LK6MtdpFkqarx2xH6b7WXRO73e7dhm4Z0oZBOu0PYGdMT"
    access_token = "843562751284920320-mVmbSATnTSv6ux8hCBjFzS7rS2NNuHM"
    access_token_secret = "IGHs5vRgaJp5DIDm05i52P8sdx7aCthDUDquCgZXcUweR"

#Twitter API Connections
twitterAuth = tweepy.OAuthHandler(Twitter.consumer_key, Twitter.consumer_secret)
twitterAuth.set_access_token(Twitter.access_token, Twitter.access_token_secret)
twitterAPI = tweepy.API(twitterAuth, wait_on_rate_limit=True)

#assets from tumblr API
class Tumblr:
    consumer_key = '02FFArOJvDRSXGZJDoRDKWCeyfywQSvm7TvuJpxJisB0W6kSgH'
    consumer_secret = 'MEh913kIRpE8gPQEEQ0BDewuqlC8C8Cb5ukjW8ehVQDEYRWucB'
    oauth_token = 'YQJmYuf21U1xbLLIjB5UU2M6zmopoH1F2hUrulEToWvNyNvNnP'
    oauth_token_secret = 'csjvvWtF0MCvl5m6GopSqmhns9hHttWeUjUK62WVA54VjNArQK'

#Tumblr API Connections
tumblrClient = pytumblr.TumblrRestClient(
    Tumblr.consumer_key,
    Tumblr.consumer_secret,
    Tumblr.oauth_token,
    Tumblr.oauth_token_secret
)


#MongoDB Connections
conn_string = 'mongodb+srv://Sigy:hello123@cluster0.bitcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
db_name = 'TEST'
twitter_col= 'twitter_data'
tumblr_col= 'tumblr_data'

client = MongoClient(conn_string)
db = client.get_database(db_name)
twitterCol = db[twitter_col]
tumblrCol = db[tumblr_col]


username = 'JYPETWICE'

# Fetch Twitter Data
def get_Twitter_Data():
    twitterCol.drop() # Drop the existing collection in MongoDB
    i = 1
    for status in twitterAPI.user_timeline(username):
        tweetData = {
            "status_num": i,
            "status_text": status.text,
            "status_name": status.user.name,
            "status_createdAt": status.created_at,
            "status_favouriteCount": status.favorite_count,
            "status_lang": status.lang
        }  # Data Model for twitter data
        twitterCol.insert_one(tweetData)  # Insert data to MongoDB
        i+=1

blog_name = 'fyeah-twice'

# Fetch Tumblr data
def get_Tumblr_Data():
    tumblrCol.drop() # Drop the existing collection in MongoDB
    data = tumblrClient.posts(blog_name) #Get data of posts on a blog
    postData = []
    p = data['posts']
    i = 1
    for element in p:
        trailData = element['trail']
        blogContent = ""
        for blog in trailData:
            blogContent = blog['content']
        data = {
            "post_number": i,
            "post_type": element['type'],
            "post_url": element['post_url'],
            "post_createdAt": element['date'],
            "post_title": element['summary'],
            "post_content": blogContent,
        } #Data Model for tumblr data
        postData.append(data)
        i+=1
    tumblrCol.insert_many(postData) #Insert Data to MongoDB

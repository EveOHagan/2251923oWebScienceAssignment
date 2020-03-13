import pymongo
from pymongo import Connection
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import sklearn
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Creation of MongoDB Connection
connection = Connection('localhost', 27017)

# Naming the Data Base Collection 
db = connection.WebScienceAEeve
db.brexitCollection.ensure_index("id", unique=True, dropDups=True)
collection = db.brexitCollection   

# Keywords to track 
keywords = ['brexit', 'boris', '#brexit']

# Only language gathered is English
language = ['en']

# Values obtained when created Twitter App.
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Tweets from the stream and only storing important fields to dataBase
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Loading the Tweet
        loadedtweet = json.loads(data)

        # Pull important data from the tweet to store in the database - including username,follower, author, hashtag
        try:
            tweet_id = loadedtweet['id_str']  # The Tweet ID from Twitter in string format
            username = loadedtweet['user']['screen_name']  # The username of the Tweet author
            followers = loadedtweet['user']['followers_count']  # The number of followers the Tweet author has
            text = loadedtweet['text']  # The entire body of the Tweet
            hashtags = loadedtweet['entities']['hashtags']  # Any hashtags used in the Tweet
            dateTime = loadedtweet['created_at']  # The timestamp of when the Tweet was created
            language = loadedtweet['lang']  # The language of the Tweet

        # Convert the timestamp given by Twitter to a date object called "created" ensuring simpler manipulation in MongoDB.
            created = datetime.datetime.strptime(dateTime, '%a %b %d %H:%M:%S +0000 %Y')

            # Initialise the REST API
            # Write to file the followers of each user
            list_of_followers = []

            file = open("/Users/eveohagan/followers.txt","a+")
            current_cursor = tweepy.Cursor(api.followers_ids, screen_name=username, count=10)
            current_followers = current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor

            while(next_cursor_id!=0):
                current_cursor = tweepy.Cursor(self.api.followers_ids, screen_name=username, count=10,cursor=next_cursor_id)
                current_followers=current_cursor.iterator.next()
                list_of_followers.extend(current_followers)
                next_cursor_id = current_cursor.iterator.next_cursor
               
            file.write(list_of_followers)
            file.close()  


        # Load extracted Tweet data into the variable that will be stored into the DB
            tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}

        # Save the refined Tweet data to MongoDB
            collection.save(tweet)




        # Print the username / text to your console in realtime as they are pulled from stream
            print (username + ':' + ' ' + text)
            return True
        except:
            print(loadedtweet)

    # Prints error of code 
    def on_error(self, status):
        print (status)

# Pulls from variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)





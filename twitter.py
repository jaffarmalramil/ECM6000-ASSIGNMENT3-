import tweepy
import time
import csv


# Twitter API credentials. Get yours from apps.twitter.com. Twitter acct rquired
# If you need help, visit https://dev.twitter.com/oauth/overview
consumer_key = "8Q6PWScKXMIaLiS8yLiuU4pbR"
consumer_secret = "nhq4lPEWjYhYrvR6Bf081VDedobFPVdhr4e6lSDdR1GbiwJ8r2"
access_key = "86878702-UVeOKaQskvlv0dTLxbPCreAgmHjIPpAXWKOYCQvIY"
access_secret = "S8X1jup5fZuxOoPRnUIWenuHdUwu87eAZS2aSaxTgNVHR"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

CITRONRESEARCH_PROFILE = "CitronResearch"
SHOPIFY_PROFILE = "Shopify"


# this function collects a twitter profile request and returns a Twitter object
def getProfile(handle):
    try:
        #https://dev.twitter.com/rest/reference/get/users/show describes get_user
        profile = api.get_user(handle)
    except:
        profile = None

    return profile


# this function collects twitter profile tweets and returns Tweet objects
def getTweets(handle):
    try:
        #https://developer.twitter.com/en/docs/tweets/timelines/overview describes user_timeline
        tweets = api.user_timeline(handle)
    except:
        tweets = None

    return tweets

# this function returns the tweet that has been most retweeted
def getMostRetweeted(tweets):
    retweet = None
    most = 0;
    for tweet in tweets:
        retweets = api.retweets(tweet.id)
        count = len(retweets)
        if count > most:
            most = count
            retweet = tweet
            print (str(most) + " ")

    return retweet

# this function searches for text in tweets and returns matching tweets
def getMentions(tweets, text):
    mentions = []
    for tweet in tweets:
        if text in tweet.text:
             mentions.append(tweet)
    return mentions


# main()
profile = None
while profile == None:
    handle = input("Enter a valid twitter handle: ")
    profile = getProfile(handle)

print ("       Name: " + profile.name)
print ("Description: " + profile.description)
print ("   Location: " + profile.location)

totalTweets = []

print ("\n-[ Determing most popular retweet from @" + CITRONRESEARCH_PROFILE + " ]-")

tweets = getTweets(CITRONRESEARCH_PROFILE)
retweet = getMostRetweeted(tweets)

print (retweet.text)
totalTweets.append(retweet)

print ("\n-[ Searching for \"FTC\" mentions by @" + CITRONRESEARCH_PROFILE + " ]-")
mentions = getMentions(tweets, "FTC")

for mention in mentions:
    print (mention.text)
    totalTweets.append(mention)

if len(mentions) == 0:
	print ("None");

print ("\n-[ Searching for \"Citron\" mentions by @" + SHOPIFY_PROFILE + " ]-")

tweets = getTweets(SHOPIFY_PROFILE)
mentions = getMentions(tweets, "Citron")

for mention in mentions:
    print (mention.text)
    totalTweets.append(mention)

if len(mentions) == 0:
	print ("None");

with open ('tweets.csv', 'w') as filename:
    writer = csv.writer(filename)
    writer.writerow(["name", "created_at", "text"])
    for tweet in totalTweets:
        writer.writerow([tweet.user.name, tweet.created_at, tweet.text])

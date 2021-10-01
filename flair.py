from os import remove
from re import split
import praw
import time
from praw.models import MoreComments
from praw.models import user
from praw.reddit import Submission, Subreddit

import os
from twilio.rest import Client


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

### Reads private information from text files to be input into praw ###
with open('PrivateInfo/pw.txt', 'r') as f:
    pw = f.read()
with open('PrivateInfo/clientID.txt', 'r') as f:
    cID = f.read()
with open('PrivateInfo/clientSecret.txt', 'r') as f:
    cSecret = f.read()

### basic praw login ###
reddit = praw.Reddit(
    client_id=cID,
    client_secret=cSecret,
    password=pw,
    user_agent="testscript by YOUR USERNAME",
    username="YOUR BOT NAME",
)

# Increases user flair by one and applies it.


def increaseFlair(user, flairNum, rank):
    flairNumIncrease = flairNum + 1
    flairNumStr = str(flairNumIncrease)
    newFlair = flairNumStr + " " + rank
    reddit.subreddit("YourSubredditHere").flair.set(
        "{}".format(user), "{}".format(newFlair), flair_template_id=None)


# Adds flair to specified user.
def addFlairToUser(user):
    # Pulls flair from YourSubredditHere for specific user.
    flair = next(reddit.subreddit(
        "YourSubredditHere").flair("{}".format(user)))
    flair = flair.get("flair_text")
    # If user does not have flair, set their flair to 1.
    if flair is None:
        print(flair)
        print(user)
        reddit.subreddit("YourSubredditHere").flair.set(
            "{}".format(user), "{}".format('1 Beginner'), flair_template_id=None)
    elif flair == '':
        print(flair)
        print(user)
        reddit.subreddit("YourSubredditHere").flair.set(
            "{}".format(user), "{}".format('1 Beginner'), flair_template_id=None)
    else:
        print(flair)
        print(user)
        flair = flair.split(" ")
        flairNum = int(flair[0])
        if flairNum < 15:
            increaseFlair(user, flairNum, "Beginner")
        elif flairNum >= 15 and flairNum < 25:
            increaseFlair(user, flairNum, "Advanced")
        elif flairNum >= 25 and flairNum < 50:
            increaseFlair(user, flairNum, "Expert")
        elif flairNum >= 50:
            increaseFlair(user, flairNum, "Master")

# Replies to users comment and shows them how much flair they should have.


def replyToUser(user, commentID):
    flair = next(reddit.subreddit(
        "YourSubredditHere").flair("{}".format(user)))
    flair = flair.get("flair_text")
    comment = reddit.comment(commentID)
    comment.reply(
        "Your flair should be: {}. If there are issues, please contact /u/Forest_Nerd or the moderation team".format(flair))


YourSubredditHere = reddit.subreddit("YourSubredditHere")

# Basic loop the bot goes through. Access a stream all new comments and performs checks before applying the flair. Sleeps for a short time before responding in order to accurately reflect updated flair through Reddit.
while True:
    try:
        for comment in YourSubredditHere.stream.comments(skip_existing=True):
            commentBody = str((comment.body).lower())
            if "YOUR BOT NAME verification reply" in commentBody and "/u/" in commentBody:
                childName = str(comment.author)
                childID = comment.id
                parentID = comment.parent_id
                parentComment = reddit.comment(parentID)
                parentName = parentComment.author
                if childName in parentComment.body:
                    print("YOUR BOT NAME was originally called by:" +
                          str(parentName))
                    print("YOUR BOT NAME picked up a reply by:" + str(childName))
                    addFlairToUser(childName)
                    addFlairToUser(parentName)
                    time.sleep(30)
                    replyToUser(parentName, parentID)
                    time.sleep(30)
                    replyToUser(childName, childID)
    except Exception as e:
        print("ERROR: {}".format(e))
        message = client.messages \
            .create(
                body="ERROR: {}".format(e),
                from_='+YOUR TWILIO PHONE NUMBER',
                to='+YOUR PERSONAL PHONE NUMBER'
            )

import praw
import time
from praw.models import MoreComments
from praw.models import user
from praw.reddit import Submission, Subreddit

### Reads private information from text files to be input into praw ###
with open('pw.txt', 'r') as f:
    pw = f.read()
with open('clientID.txt', 'r') as f:
    cID = f.read()
with open('clientSecret.txt', 'r') as f:
    cSecret = f.read()

### basic praw login ###
reddit = praw.Reddit(
    client_id=cID,
    client_secret=cSecret,
    password=pw,
    user_agent="testscript by YOUR USER NAME",
    username="YOUR BOT NAME",
)

# Declares different subreddit variables for use/testing


YourSubredditHere = reddit.subreddit("YourSubredditHere")

# Creates an array of contributors and titles to be compared to.


contributorArr = []
titleArr = []

# Sets stream of all non-existing comments and submissions.


comment_stream = YourSubredditHere.stream.comments(
    skip_existing=True, pause_after=-1)
submission_stream = YourSubredditHere.stream.submissions(
    skip_existing=True, pause_after=-1)

# Appends all contributors to the contributor array unless they are already in said array.


def contributorListGenerator():
    for contributor in reddit.subreddit('YourSubredditHere').contributor():
        if contributor not in contributorArr:
            contributorArr.append(contributor.name)

# Checks if an account has been responded to by automoderator about our New Account Rules. If so, messages the user.


def isNewAccount(commentParentName):
    if "Your comment was removed because your account is either under 30 days old" in commentBody or "Your post was removed because your account is either under 30 days old" in commentBody:
        reddit.redditor(commentParentName).message("New Account Rules",
                                                   "**I am a bot and will not reply to this message. If you believed this message was received in error, please message /u/Forest_Nerd.**\
            Your post or comment has been removed because you fall under our 'New Account' rules. \
            Accounts under 30 days of age and/or undser a undisclosed karma level will not be allowed to post. \
            If you have sales references or flair from other selling forums or subreddits, please feel free to PM the mods with proof to be \
            considered for being placed on our approved users list.")

# Checks if post was duplicated in the last 72 hours.


def duplicatePostIn72Hours():
    if submission.title in titleArr and (time.time() - submission.created_utc) < 259200:
        reddit.subreddit("YourSubredditHere").message("Duplicate Post Detected",
                                                      "I AM A BOT. I detected a duplicate post in the last 72 hours from {}.".format(submission.author))
    else:
        titleArr.append(str(submission.title))


while True:
    # Creates a variable to determine loops, and sets a report array to be cycled through.
    loops = 0
    reportArr = []
    # Start of code for comment stream.
    for comment in comment_stream:
        # Breaks if new comment is not available.
        if comment is None:
            break
        # Sets variables to be read.
        commentBody = comment.body
        commentParentID = comment.parent_id
        commentParentName = str(reddit.comment(commentParentID).author)
        # Detects if Automoderator replied to a comment or post. Sends message to author stating they are in our New Account rules.
        isNewAccount(commentParentName)

    # Start of code for submission stream.
    for submission in submission_stream:
        # Breaks if new comment is not available.
        if submission is None:
            break
        # Finds duplicate posts in the past 72 hours and messages mods.
        duplicatePostIn72Hours()

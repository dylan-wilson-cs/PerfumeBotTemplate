# Reddit Bot (PerfumeBot)

## Introduction

A Python bot made using the Reddit PRAW API and Twilio Messaging API. This bot was designed to make moderating of transaction based subreddits more streamlined. The primary feature of PerfumeBot is an automated flairing system which replies on a call/response to automatically flair members when they have a positive transaction. The bot also provides other utilities such as handling the report system, new user interactions, and duplicate post detection.

## Setup

PerfumeBot can be used in any transaction community to automate the flairing system with a few simple changes.

-   PerfumeBot relies on the PRAW API as it's only means of detecting posts. You will need to [create your own bot here](https://ssl.reddit.com/prefs/apps/) and transfer your Client ID, Client Secret, and password to either the PrivateInfo folder, environment variables, or in the code itself.
    -   Lines 18-23 in flair.py and lines 9-13 in AltFunctions.py are your Twilio private information variables.
-   PerfumeBot also use Twilio Messaging to warn the creator when an error is thrown. You can create a [Twilio Messanger account here](https://www.twilio.com/messaging) and you will enter your private data in a similar fashion.
    -   Lines 13-15 and 111-112 in flair.py are your Twilio private information variables.
    -   Twilio can be removed completely if you do not want to text yourself errors.
-   You will need to change some local varianbles:
    -   Change all instances of "YOUR BOT NAME" to your bot's username.
    -   Change all instances of YourSubredditHere to your the subreddit name to be watched.

After setting up your local variables you are ready to run! You can edit your flair values and amount starting on line 65 of flair.py.

## Sample Functions

**def isNewAccount(commentParentName):**
Checks if an account has been responded to by automoderator about our New Account Rules. If so, messages the user.

**def duplicatePostIn72Hours():**
Checks if post was duplicated in the last 72 hours.

**def increaseFlair(user, flairNum, rank):**
Increases user flair by one and applies it.

from sys import argv
import webbrowser
import praw
import yaml
import datetime
import time # Not necessary with python3, change when upgrading

# grab subreddit and days requested from commandline
script, subreddit, daysaftercreated = argv

# convert daysaftercreated to an integer blurts error if doesn't . 
try:
    daysaftercreated = int(daysaftercreated)
except Exception:
    print("Error: could not convert date.")
    exit()

# Load reddit config
yamlfile = yaml.load(open('config.yml', 'r'))

# Reddit login info from yaml 
reddit = praw.Reddit(client_id = yamlfile['client_id'],
    client_secret = yamlfile['client_secret'],
    user_agent = yamlfile['user_agent'])

# Create subreddit instance 
subreddit_instance = reddit.subreddit(subreddit)

error = """
Error: Could not retrieve date from Reddit API. Check connection and Reddit
status. Subreddit may be mispelled or credentials are incorrect.
"""

# Retrives date created from instance
try:
    sub_createdate_unix = int(subreddit_instance.created_utc)
except Exception:
    print(error)
    exit()

# convert to dt, add requested time, convert back to unix
sub_createdate_dt = datetime.datetime.fromtimestamp(sub_createdate_unix) 
new_time_dt = (sub_createdate_dt + datetime.timedelta(days=daysaftercreated)) 
new_time_unix = time.mktime(new_time_dt.timetuple())

url = "https://reddit.com/r/%s/search?sort=new&q=timestamp%%3A%d..%d&restrict_sr=on&syntax=cloudsearch" % (
        subreddit, sub_createdate_unix, new_time_unix)
webbrowser.open(url)

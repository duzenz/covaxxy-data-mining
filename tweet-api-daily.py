from time import sleep
from requests_oauthlib import OAuth1Session
import os
import json

DATASET_FOLDER = "dataset/"
PROGRESS_FOLDER = "reporting"
DOWNLOADS_FOLDER = "downloads/"

consumer_key = 'LuxyopoKhXzikhPKvTTiL15rS'
consumer_secret = 'm0hY9nI9JdUdS854QDMi01YbBE9ZlQGkIu5PzATirdOdNTdeZ4'

params = {"ids": "1483952390000857088",
          "tweet.fields": "author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
          "expansions": "author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
          "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
          "user.fields": "created_at,description,id,entities,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}

request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

access_token = '1516510333673820160-wDQprSTj7bHny74GAXJc4iri9tgbwF'
access_token_secret = 'pidGhL504ok5QnakSqKJOBUndF4CTKZRG7enjAgNdugsO'

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

tweetIds = ""

FILENAME_LIST = [
    "tweet_ids--2021-03-02.txt",
    "tweet_ids--2021-03-03.txt",
    "tweet_ids--2021-03-04.txt",
    "tweet_ids--2021-03-05.txt",
    "tweet_ids--2021-03-06.txt",
    "tweet_ids--2021-03-07.txt",
    "tweet_ids--2021-03-08.txt",
    "tweet_ids--2021-03-09.txt",
    "tweet_ids--2021-03-10.txt",
    "tweet_ids--2021-03-11.txt",
    "tweet_ids--2021-03-12.txt",
    "tweet_ids--2021-03-13.txt",
    "tweet_ids--2021-03-14.txt",
    "tweet_ids--2021-03-15.txt",
    "tweet_ids--2021-03-16.txt",
    "tweet_ids--2021-03-17.txt",
    "tweet_ids--2021-03-18.txt",
]

for filename in FILENAME_LIST:
    FOLDER_NAME = DOWNLOADS_FOLDER + str(filename).removesuffix(".txt")
    isFolderExists = os.path.isdir(FOLDER_NAME)
    startFrom = 0
    if not isFolderExists:
        os.makedirs(FOLDER_NAME)
    else:
        requestedCount = len([entry for entry in os.listdir(FOLDER_NAME) if
                              os.path.isfile(os.path.join(FOLDER_NAME, entry))
                              ])
        startFrom = requestedCount

    startFrom = startFrom * 100
    print("startFrom: " + str(startFrom))

    tweet_id_file = open(DATASET_FOLDER + filename, 'r')
    tweet_id_file_lines = tweet_id_file.readlines()[startFrom:]
    index = startFrom

    for line in tweet_id_file_lines:
        tweetIds += line.strip() + ","
        index += 1
        if index % 100 == 0:
            print("tweet id list {}".format(tweetIds.rstrip(',')))

            params["ids"] = tweetIds.rstrip(',')
            response = oauth.get(
                "https://api.twitter.com/2/tweets", params=params
            )
            if response.status_code != 200:
                if response.status_code == 429:
                    sleep(901)
                    print("Too many requests need to wait 15  minutes")
                else:
                    print("Problem {}".format(response.status_code))

            print("Response code: {}".format(response.status_code))

            json_response = response.json()
            with open(FOLDER_NAME + "/" + str(index) + '.json', 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, sort_keys=True, indent=4)

            tweetIds = ""

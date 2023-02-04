from time import sleep
from requests_oauthlib import OAuth1Session
import os
import json

DATASET_FOLDER = "dataset"
PROGRESS_FOLDER = "reporting"
PROGRESS_FILE_NAME = "progress.xlsx"
DOWNLOADS_FOLDER = "downloads"

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

# Get authorization
# base_authorization_url = "https://api.twitter.com/oauth/authorize"
# authorization_url = oauth.authorization_url(base_authorization_url)
# print("Please go here and authorize: %s" % authorization_url)
# verifier = input("Paste the PIN here: ")


access_token = '1516510333673820160-wDQprSTj7bHny74GAXJc4iri9tgbwF'
access_token_secret = 'pidGhL504ok5QnakSqKJOBUndF4CTKZRG7enjAgNdugsO'
# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

tweetIds = ""

for (root, dirs, file) in os.walk("../../Desktop/pythonProject/dataset/test"):
    for filename in file:
        print(filename)

        isFolderExists = os.path.isdir("downloads/" + str(filename).removesuffix(".txt"))
        startFrom = 0
        if not isFolderExists:
            os.makedirs("downloads/" + str(filename).removesuffix(".txt"))
        else:
            requestedCount = len(
                [entry for entry in os.listdir(DOWNLOADS_FOLDER + "/" + str(filename).removesuffix(".txt")) if
                 os.path.isfile(
                     os.path.join(DOWNLOADS_FOLDER + "/" + str(filename).removesuffix(".txt"), entry))])
            startFrom = requestedCount

        startFrom = startFrom * 100
        print("startFrom: " + str(startFrom))
        file1 = open(root + "/" + filename, 'r')
        lines = file1.readlines()[startFrom:]
        requestCount = 0
        index = startFrom
        for line in lines:
            tweetIds += line.strip() + ","
            index += 1
            if index % 100 == 0:
                print("Line{}: {}".format(requestCount, tweetIds.rstrip(',')))
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
                with open('downloads/' + str(filename).removesuffix(".txt") + "/" + str(index) + '.json', 'w',
                          encoding='utf-8') as f:
                    json.dump(response.json(), f, ensure_ascii=False, sort_keys=True, indent=4)

                requestCount += 1
                if requestCount == 900:
                    requestCount = 0
                    break

                tweetIds = ""
                continue




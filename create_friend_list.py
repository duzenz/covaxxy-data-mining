import csv
from operator import itemgetter
from time import sleep

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from requests_oauthlib import OAuth1Session
from scipy import stats


def get_oauth():
    consumer_key = 'LuxyopoKhXzikhPKvTTiL15rS'
    consumer_secret = 'm0hY9nI9JdUdS854QDMi01YbBE9ZlQGkIu5PzATirdOdNTdeZ4'

    params = {}

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
    return oauth


def create_friend_list():
    user_set = set()

    df = pd.read_csv('reporting/visualize/tweet_ids--2021-01-11.csv')
    for index, tweet in df.iterrows():
        user_set.add(tuple([tweet.author_id, tweet.username]))

    authObj = get_oauth()

    header = ['user_id', 'user_name', 'friend_id', 'friend_name', 'friend_username']
    f = open('reporting/visualize/tweet_ids--2021-01-11-friends.csv', 'w+', encoding="utf-8", newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    for item in user_set:
        url = "https://api.twitter.com/2/users/" + str(
            item[0]) + "/followers?max_results=1000&user.fields=username&tweet.fields=author_id"
        print(url)
        response = authObj.get(url)

        if response.status_code != 200:
            if response.status_code == 429:
                sleep(901)
                print("Too many requests need to wait 15  minutes")
                print("request again")
                response = authObj.get(url)
            else:
                print("Problem {}".format(response.status_code))

        print("Response code: {}".format(response.status_code))

        json_response = response.json()
        if "data" in json_response:
            for friend in json_response["data"]:
                writer.writerow([item[0], item[1], friend["id"], friend["name"], friend["username"]])

    f.close()


def main():
    create_friend_list()


if __name__ == '__main__':
    main()

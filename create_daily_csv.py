import csv
import json
import os
from urllib.parse import urlparse

DOWNLOADS_FOLDER = "C:/Users/test.test/Desktop/covaxxy/downloads/"


def create_csv_for_day():
    lines = read_non_credible_sources()
    header = ['id', 'created_at', 'tweet_id', 'credible', 'author_id',
              'text', 'urls', 'name', 'username', 'verified', 'location',
              'followers_count', 'following_count', 'tweet_count',
              'like_count', 'quote_count', 'reply_count', 'retweet_count',
              'retweet_author_id', 'retweet_id', 'retweeted_screen_name',
              'user_mentions_id', 'user_mentions_screen_name',
              'in_reply_to_user_id', 'in_reply_to_tweet_id', 'in_reply_to_username']

    for (root, dirs, file) in os.walk(DOWNLOADS_FOLDER):
        for directory in dirs:
            print("operation for " + directory)
            if os.path.isfile('reporting/' + directory + '.csv'):
                print('reporting/' + directory + '.csv already created. skipping it')
                continue
            f = open('reporting/' + directory + '.csv', 'w', encoding="utf-8", newline='')
            writer = csv.writer(f)
            writer.writerow(header)
            for (rootSub, dirsSub, fileSub) in os.walk(DOWNLOADS_FOLDER + directory):
                for filename in fileSub:
                    f = open(DOWNLOADS_FOLDER + directory + "/" + filename, encoding="utf8")
                    print("adding result for " + filename)
                    data = json.load(f)
                    counter = 0
                    if "data" in data:
                        for tweet in data["data"]:
                            writer.writerow(
                                get_row(tweet, counter, data["includes"]["users"], data["includes"]["tweets"], lines))
                            counter = counter + 1
            f.close()


def set_user_information(tweet, users, row):
    user_info = list(filter(lambda user: user['id'] == tweet["author_id"], users))
    if len(user_info) > 0:
        row.append(user_info[0]["name"])
        row.append(user_info[0]["username"])
        row.append(user_info[0]["verified"])
        row.append(user_info[0]["location"] if "location" in user_info[0] else "#")
        row.append(user_info[0]["public_metrics"]["followers_count"])
        row.append(user_info[0]["public_metrics"]["following_count"])
        row.append(user_info[0]["public_metrics"]["tweet_count"])
    else:
        row.append("#")
        row.append("#")
        row.append("#")
        row.append("#")
        row.append("#")
        row.append("#")
        row.append("#")


def retweeted(referenced_tweets):
    if referenced_tweets[0]["type"] == "retweeted":
        return True
    return False


def replied_to(referenced_tweets):
    if referenced_tweets[0]["type"] == "replied_to":
        return True
    return False


def set_retweet_information(tweet, users, tweets, row):
    if "referenced_tweets" in tweet and retweeted(tweet["referenced_tweets"]):
        retweet = list(filter(lambda tag: tag['id'] == tweet["referenced_tweets"][0]["id"], tweets))
        if len(retweet) > 0:
            row.append(retweet[0]["author_id"])
            row.append(tweet["referenced_tweets"][0]["id"])
            retweet_user = list(filter(lambda tag: tag['id'] == retweet[0]["author_id"], users))
            if len(retweet_user) > 0:
                row.append(retweet_user[0]["username"])
            else:
                row.append("#")
        else:
            row.append("#")
            row.append("#")
    else:
        row.append("#")
        row.append("#")
        row.append("#")


def set_mention_information(tweet, row):
    if "entities" in tweet and "mentions" in tweet["entities"]:
        if len(tweet["entities"]["mentions"]) > 0:
            row.append(tweet["entities"]["mentions"][0]["id"])
            row.append(tweet["entities"]["mentions"][0]["username"])
    else:
        row.append("#")
        row.append("#")


def set_replied_to_information(tweet, users, row):
    if "referenced_tweets" in tweet and replied_to(tweet["referenced_tweets"]) and "in_reply_to_user_id" in tweet:
        row.append(tweet["in_reply_to_user_id"])
        row.append(tweet["referenced_tweets"][0]["id"])
        reply_user = list(filter(lambda tag: tag['id'] == tweet["in_reply_to_user_id"], users))
        if len(reply_user) > 0:
            row.append(reply_user[0]["username"])
        else:
            row.append("#")
    else:
        row.append("#")
        row.append("#")
        row.append("#")


def set_reaction_information(tweet, row):
    row.append(tweet["public_metrics"]["like_count"])
    row.append(tweet["public_metrics"]["quote_count"])
    row.append(tweet["public_metrics"]["reply_count"])
    row.append(tweet["public_metrics"]["retweet_count"])


def get_row(tweet, counter, users, tweets, lines):
    row = []
    row.append(counter)
    row.append(tweet["created_at"])
    row.append(tweet["id"])
    row.append(get_label(tweet, lines))
    row.append(tweet["author_id"])
    row.append(tweet["text"])
    set_url_information(tweet, row)
    set_user_information(tweet, users, row)
    set_reaction_information(tweet, row)
    set_retweet_information(tweet, users, tweets, row)
    set_mention_information(tweet, row)
    set_replied_to_information(tweet, users, row)
    return row


def set_url_information(tweet, row):
    if "entities" in tweet and "urls" in tweet["entities"]:
        display_url = ""
        for item in tweet["entities"]['urls']:
            display_url += urlparse(item['expanded_url']).netloc + ","
        row.append(display_url)
    else:
        row.append("#")


def get_label(tweet, lines):
    display_url = ""
    if "entities" in tweet and "urls" in tweet["entities"]:
        for item in tweet["entities"]['urls']:
            display_url += urlparse(item['expanded_url']).netloc + ","

    res = [ele for ele in lines if (ele in tweet["text"] or ele in display_url)]
    if bool(res):
        return 0
    else:
        return 1


def read_non_credible_sources():
    with open('dataset/iffy.txt', encoding="utf8") as f:
        return [line.rstrip() for line in f]


def main():
    create_csv_for_day()


if __name__ == '__main__':
    main()

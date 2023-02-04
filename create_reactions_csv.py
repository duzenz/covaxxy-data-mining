import csv
import json
import os

DATA_LIST = ["tweet_ids--2021-01-11", "tweet_ids--2021-02-01", "tweet_ids--2021-03-01", "tweet_ids--2021-04-01",
             "tweet_ids--2021-05-01",
             "tweet_ids--2021-06-01", "tweet_ids--2021-07-01", "tweet_ids--2021-08-01", "tweet_ids--2021-09-01",
             "tweet_ids--2021-10-01", "tweet_ids--2021-11-01", "tweet_ids--2021-03-19", "tweet_ids--2021-03-20",
             "tweet_ids--2021-03-21", "tweet_ids--2021-03-22", "tweet_ids--2021-03-23", "tweet_ids--2021-03-24",
             "tweet_ids--2021-03-25", "tweet_ids--2021-03-26", "tweet_ids--2021-03-27", "tweet_ids--2021-03-28",
             "tweet_ids--2021-12-01"]


def create_csv_for_day():
    lines = read_uncredible_sources()
    header = ['tweet_id', 'created_at', 'credible', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
              'reference_type', 'reference_id']

    for folder_name in DATA_LIST:
        f = open('reporting/' + 'reactions-' + folder_name + '.csv', 'w', encoding="utf-8", newline='')
        writer = csv.writer(f)
        writer.writerow(header)
        for (root, dirs, file) in os.walk("C:/Users/test.test/Desktop/covaxxy/downloads/" + folder_name):
            for filename in file:
                f = open("C:/Users/test.test/Desktop/covaxxy/downloads/" + folder_name + "/" + filename,
                         encoding="utf8")
                print("adding result for " + filename)
                data = json.load(f)
                if "data" in data:
                    for tweet in data["data"]:
                        writer.writerow(get_row(tweet, lines))
        f.close()


def get_row(tweet, lines):
    row = []
    row.append(tweet["id"])
    row.append(tweet["created_at"])
    row.append(get_label(tweet, lines))
    if "public_metrics" in tweet:
        row.append(tweet["public_metrics"]["like_count"])
        row.append(tweet["public_metrics"]["quote_count"])
        row.append(tweet["public_metrics"]["reply_count"])
        row.append(tweet["public_metrics"]["retweet_count"])
    if "referenced_tweets" in tweet:
        row.append(tweet["referenced_tweets"][0]["type"])
        row.append(tweet["referenced_tweets"][0]["id"])
    return row


def get_label(tweet, lines):
    res = [ele for ele in lines if (ele in tweet["text"])]
    if bool(res):
        return 0
    else:
        return 1


def read_uncredible_sources():
    with open('dataset/iffy.txt', encoding="utf8") as f:
        return [line.rstrip() for line in f]


def main():
    create_csv_for_day()


if __name__ == '__main__':
    main()

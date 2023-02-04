import csv
import json
import os

DOWNLOADS_FOLDER = "downloads/tweet_ids--2021-03-27"
OUTPUT_FILE = "reporting/tweet_ids--2021-03-27.csv"


def label_tweets_for_a_day():
    with open('dataset/iffy.txt', encoding="utf8") as f:
        lines = [line.rstrip() for line in f]

    header = ['tweet_id', 'created_at', 'credible']
    f = open(OUTPUT_FILE, 'w', encoding="utf-8", newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    for (rootSub, dirsSub, fileSub) in os.walk(DOWNLOADS_FOLDER):
        for filename in fileSub:
            f = open(DOWNLOADS_FOLDER + "/" + filename, encoding="utf8")
            data = json.load(f)
            print(filename)
            for tweet in data["data"]:
                row = [tweet["id"], tweet["created_at"]]
                res = [ele for ele in lines if (ele in tweet["text"])]
                if bool(res):
                    row.append(0)
                else:
                    row.append(1)
                print(row)
                writer.writerow(row)


def main():
    label_tweets_for_a_day()


if __name__ == '__main__':
    main()

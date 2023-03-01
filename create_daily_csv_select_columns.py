import pandas as pd
from pathlib import Path

FILE_NAMES = ["tweet_ids--2021-03-01.csv", "tweet_ids--2021-03-02.csv", "tweet_ids--2021-03-03.csv",
              "tweet_ids--2021-03-04.csv", "tweet_ids--2021-03-05.csv"]
REPORTS_FOLDER = "reporting/"
HEADERS = ['id', 'created_at', 'tweet_id', 'credible', 'author_id',
           'text', 'urls', 'name', 'username', 'verified', 'location',
           'followers_count', 'following_count', 'tweet_count',
           'like_count', 'quote_count', 'reply_count', 'retweet_count',
           'retweet_author_id', 'retweet_id', 'retweeted_screen_name',
           'user_mentions_id', 'user_mentions_screen_name',
           'in_reply_to_user_id', 'in_reply_to_tweet_id', 'in_reply_to_username']


def create_csv_for_columns(filename, headers):
    # read_csv function which is used to read the required CSV file
    data = pd.read_csv(REPORTS_FOLDER + filename)

    # drop function which is used in removing or deleting rows or columns from the CSV files
    data.drop(headers, axis=1, inplace=True)

    filepath = Path('reporting/columnar/' + filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(filepath)


def main():
    columns_selected = ["tweet_id", "created_at", "author_id", 'text', 'followers_count', 'following_count']
    for val in columns_selected:
        HEADERS.remove(val)

    for filename in FILE_NAMES:
        create_csv_for_columns(filename, HEADERS)


if __name__ == '__main__':
    main()

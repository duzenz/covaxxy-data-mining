import pandas as pd
from pathlib import Path
from datetime import date, timedelta

DAYS = []
REPORTS_FOLDER = "reporting/"
HEADERS = ['id', 'created_at', 'tweet_id', 'credible', 'author_id',
           'text', 'urls', 'name', 'username', 'verified', 'location',
           'followers_count', 'following_count', 'tweet_count',
           'like_count', 'quote_count', 'reply_count', 'retweet_count',
           'retweet_author_id', 'retweet_id', 'retweeted_screen_name',
           'user_mentions_id', 'user_mentions_screen_name',
           'in_reply_to_user_id', 'in_reply_to_tweet_id', 'in_reply_to_username',
           'reference_type', 'reference_id']


def create_csv_for_columns(filename, headers):
    # read_csv function which is used to read the required CSV file
    data = pd.read_csv(REPORTS_FOLDER + 'tweet_ids--' + filename + '.csv')

    # drop function which is used in removing or deleting rows or columns from the CSV files
    data.drop(headers, axis=1, inplace=True)

    filepath = Path('reporting/columnar/reactions-report-' + filename + '.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(filepath)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def main():
    columns_selected = ['tweet_id', 'created_at', 'credible', 'like_count', 'quote_count', 'reply_count',
                        'retweet_count', 'reference_type', 'reference_id']
    for val in columns_selected:
        HEADERS.remove(val)

    start_date = date(2021, 3, 29)
    end_date = date(2021, 4, 1)
    for single_date in daterange(start_date, end_date):
        print("file creation for " + single_date.strftime("%Y-%m-%d"))
        create_csv_for_columns(single_date.strftime("%Y-%m-%d"), HEADERS)


if __name__ == '__main__':
    main()

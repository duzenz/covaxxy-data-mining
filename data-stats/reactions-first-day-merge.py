import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series


def save_figure(title, dataframe):
    fig, axs = plt.subplots(figsize=(20, 10))
    dataframe.plot(rot=0, ax=axs, xlabel='hour', ylabel='tweet-count')
    plt.xticks(range(0, 24))
    plt.title(title, fontsize=30)
    plt.savefig(title + ".png")


def test(filename):
    df_tweets = pd.read_csv('../reporting/reactions-tweet_ids--' + filename + '.csv')
    df_tweets = df_tweets.drop_duplicates(subset=['reference_id'])
    df_tweets['created_at'] = pd.to_datetime(df_tweets['created_at'])
    df_tweets = df_tweets.set_index(['created_at'])
    df_tweets_retweet_count = df_tweets.sort_values(by=['retweet_count'], ascending=False).head(100)
    df_tweets_reply_count = df_tweets.sort_values(by=['reply_count'], ascending=False).head(100)
    df_tweets_quote_count = df_tweets.sort_values(by=['quote_count'], ascending=False).head(100)
    df_tweets_like_count = df_tweets.sort_values(by=['like_count'], ascending=False).head(100)
    hourly_count_retweet_count = df_tweets_retweet_count.groupby(df_tweets_retweet_count.index.hour).apply(f)
    hourly_count_reply_count = df_tweets_reply_count.groupby(df_tweets_reply_count.index.hour).apply(f)
    hourly_count_quote_count = df_tweets_quote_count.groupby(df_tweets_quote_count.index.hour).apply(f)
    hourly_count_like_count = df_tweets_like_count.groupby(df_tweets_like_count.index.hour).apply(f)
    return hourly_count_retweet_count, hourly_count_quote_count, hourly_count_reply_count, hourly_count_like_count


def draw_graph():
    hourly_count_retweet_count_01, hourly_count_quote_count_01, hourly_count_reply_count_01, hourly_count_like_count_01 = test("2021-01-11")
    hourly_count_retweet_count_02, hourly_count_quote_count_02, hourly_count_reply_count_02, hourly_count_like_count_02 = test("2021-02-01")
    hourly_count_retweet_count_03, hourly_count_quote_count_03, hourly_count_reply_count_03, hourly_count_like_count_03 = test("2021-02-01")
    hourly_count_retweet_count_04, hourly_count_quote_count_04, hourly_count_reply_count_04, hourly_count_like_count_04 = test("2021-03-01")
    hourly_count_retweet_count_05, hourly_count_quote_count_05, hourly_count_reply_count_05, hourly_count_like_count_05 = test("2021-04-01")
    hourly_count_retweet_count_06, hourly_count_quote_count_06, hourly_count_reply_count_06, hourly_count_like_count_06 = test("2021-05-01")
    hourly_count_retweet_count_07, hourly_count_quote_count_07, hourly_count_reply_count_07, hourly_count_like_count_07 = test("2021-06-01")
    hourly_count_retweet_count_08, hourly_count_quote_count_08, hourly_count_reply_count_08, hourly_count_like_count_08 = test("2021-07-01")
    hourly_count_retweet_count_09, hourly_count_quote_count_09, hourly_count_reply_count_09, hourly_count_like_count_09 = test("2021-08-01")
    hourly_count_retweet_count_10, hourly_count_quote_count_10, hourly_count_reply_count_10, hourly_count_like_count_10 = test("2021-09-01")
    hourly_count_retweet_count_11, hourly_count_quote_count_11, hourly_count_reply_count_11, hourly_count_like_count_11 = test("2021-10-01")
    hourly_count_retweet_count_12, hourly_count_quote_count_12, hourly_count_reply_count_12, hourly_count_like_count_12 = test("2021-11-01")

    df = pd.DataFrame({'2021_01_11': hourly_count_retweet_count_01['Number_of_tweets'],
                       '2021_02_01': hourly_count_retweet_count_02['Number_of_tweets'],
                       '2021_03_01': hourly_count_retweet_count_03['Number_of_tweets'],
                       '2021_04_01': hourly_count_retweet_count_04['Number_of_tweets'],
                       '2021_05_01': hourly_count_retweet_count_05['Number_of_tweets'],
                       '2021_06_01': hourly_count_retweet_count_06['Number_of_tweets'],
                       '2021_07_01': hourly_count_retweet_count_07['Number_of_tweets'],
                       '2021_08_01': hourly_count_retweet_count_08['Number_of_tweets'],
                       '2021_09_01': hourly_count_retweet_count_09['Number_of_tweets'],
                       '2021_10_01': hourly_count_retweet_count_10['Number_of_tweets'],
                       '2021_11_01': hourly_count_retweet_count_11['Number_of_tweets'],
                       '2021_12_01': hourly_count_retweet_count_12['Number_of_tweets'],
                       })
    save_figure("First-Day-Of-Months-Retweets", df)

    df = pd.DataFrame({'2021_01_11': hourly_count_quote_count_01['Number_of_tweets'],
                       '2021_02_01': hourly_count_quote_count_02['Number_of_tweets'],
                       '2021_03_01': hourly_count_quote_count_03['Number_of_tweets'],
                       '2021_04_01': hourly_count_quote_count_04['Number_of_tweets'],
                       '2021_05_01': hourly_count_quote_count_05['Number_of_tweets'],
                       '2021_06_01': hourly_count_quote_count_06['Number_of_tweets'],
                       '2021_07_01': hourly_count_quote_count_07['Number_of_tweets'],
                       '2021_08_01': hourly_count_quote_count_08['Number_of_tweets'],
                       '2021_09_01': hourly_count_quote_count_09['Number_of_tweets'],
                       '2021_10_01': hourly_count_quote_count_10['Number_of_tweets'],
                       '2021_11_01': hourly_count_quote_count_11['Number_of_tweets'],
                       '2021_12_01': hourly_count_quote_count_12['Number_of_tweets'],
                       })
    save_figure("First-Day-Of-Months-Quotes", df)

    df = pd.DataFrame({'2021_01_11': hourly_count_reply_count_01['Number_of_tweets'],
                       '2021_02_01': hourly_count_reply_count_02['Number_of_tweets'],
                       '2021_03_01': hourly_count_reply_count_03['Number_of_tweets'],
                       '2021_04_01': hourly_count_reply_count_04['Number_of_tweets'],
                       '2021_05_01': hourly_count_reply_count_05['Number_of_tweets'],
                       '2021_06_01': hourly_count_reply_count_06['Number_of_tweets'],
                       '2021_07_01': hourly_count_reply_count_07['Number_of_tweets'],
                       '2021_08_01': hourly_count_reply_count_08['Number_of_tweets'],
                       '2021_09_01': hourly_count_reply_count_09['Number_of_tweets'],
                       '2021_10_01': hourly_count_reply_count_10['Number_of_tweets'],
                       '2021_11_01': hourly_count_reply_count_11['Number_of_tweets'],
                       '2021_12_01': hourly_count_reply_count_12['Number_of_tweets'],
                       })
    save_figure("First-Day-Of-Months-Replies", df)

    df = pd.DataFrame({'2021_01_11': hourly_count_like_count_01['Number_of_tweets'],
                       '2021_02_01': hourly_count_like_count_02['Number_of_tweets'],
                       '2021_03_01': hourly_count_like_count_03['Number_of_tweets'],
                       '2021_04_01': hourly_count_like_count_04['Number_of_tweets'],
                       '2021_05_01': hourly_count_like_count_05['Number_of_tweets'],
                       '2021_06_01': hourly_count_like_count_06['Number_of_tweets'],
                       '2021_07_01': hourly_count_like_count_07['Number_of_tweets'],
                       '2021_08_01': hourly_count_like_count_08['Number_of_tweets'],
                       '2021_09_01': hourly_count_like_count_09['Number_of_tweets'],
                       '2021_10_01': hourly_count_like_count_10['Number_of_tweets'],
                       '2021_11_01': hourly_count_like_count_11['Number_of_tweets'],
                       '2021_12_01': hourly_count_like_count_12['Number_of_tweets'],
                       })
    save_figure("First-Day-Of-Months-Likes", df)


def main():
    draw_graph()


def f(x):
    return Series(dict(Number_of_tweets=x['tweet_id'].count(), ))


if __name__ == '__main__':
    main()

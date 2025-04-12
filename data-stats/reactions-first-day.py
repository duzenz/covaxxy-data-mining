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
    save_figure("reactions-" + filename + "_retweet", hourly_count_retweet_count)
    save_figure("reactions-" + filename + "_reply", hourly_count_reply_count)
    save_figure("reactions-" + filename + "_quote", hourly_count_quote_count)
    save_figure("reactions-" + filename + "_like", hourly_count_like_count)


def draw_graph():
    test("2021-01-11")
    test("2021-02-01")
    test("2021-03-01")
    test("2021-04-01")
    test("2021-05-01")
    test("2021-06-01")
    test("2021-07-01")
    test("2021-08-01")
    test("2021-09-01")
    test("2021-10-01")
    test("2021-11-01")
    test("2021-12-01")


def main():
    draw_graph()


def f(x):
    return Series(dict(Number_of_tweets=x['tweet_id'].count(), ))


if __name__ == '__main__':
    main()

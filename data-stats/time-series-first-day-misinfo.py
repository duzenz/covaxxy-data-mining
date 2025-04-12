import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series


# def save_figure(title, dataframe):
#     fig, axs = plt.subplots(figsize=(20, 10))
#     dataframe.plot(rot=0, ax=axs, xlabel='Hour in day', ylabel='Tweet count')
#     plt.xticks(range(0, 24))
#     plt.title("", fontsize=30)
#     plt.savefig(title + ".png")
#
def save_figure(title, dataframe):
    # Set the figure size
    fig, axs = plt.subplots(figsize=(12, 6))

    # Plot the data
    dataframe.plot(rot=0, ax=axs, xlabel='Gün içerisindeki saat', ylabel='Atılan tweet sayısı', linewidth=2, marker='o', markersize=8)

    # Set the x-ticks to be from 0 to 23 (hours in a day)
    plt.xticks(range(0, 24))

    # Set the title with a larger font size
    plt.title("Ayların İlk Gününde Atılan ve Yanlış Bilgi İçeren Tweetler", fontsize=24, pad=20)

    # Increase the font size of the axis labels
    axs.set_xlabel('Gün içerisindeki saat', fontsize=18)
    axs.set_ylabel('Atılan tweet sayısı', fontsize=18)

    # Increase the font size of the tick labels
    axs.tick_params(axis='both', which='major', labelsize=14)

    # Add grid lines for better readability
    axs.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Save the figure with a high DPI for better quality in papers
    plt.savefig(title + ".png", dpi=300, bbox_inches='tight')

    # Show the plot (optional, for debugging)
    plt.show()


def draw_graph():
    df_tweets_2021_01_11 = pd.read_csv('../reporting/tweet_ids--2021-01-11.csv')
    df_tweets_2021_01_11 = df_tweets_2021_01_11.loc[df_tweets_2021_01_11['credible'] == 0].copy()

    df_tweets_2021_02_01 = pd.read_csv('../reporting/tweet_ids--2021-02-01.csv')
    df_tweets_2021_02_01 = df_tweets_2021_02_01.loc[df_tweets_2021_02_01['credible'] == 0].copy()

    df_tweets_2021_03_01 = pd.read_csv('../reporting/tweet_ids--2021-03-01.csv')
    df_tweets_2021_03_01 = df_tweets_2021_03_01.loc[df_tweets_2021_03_01['credible'] == 0].copy()

    df_tweets_2021_04_01 = pd.read_csv('../reporting/tweet_ids--2021-04-01.csv')
    df_tweets_2021_04_01 = df_tweets_2021_04_01.loc[df_tweets_2021_04_01['credible'] == 0].copy()

    df_tweets_2021_05_01 = pd.read_csv('../reporting/tweet_ids--2021-05-01.csv')
    df_tweets_2021_05_01 = df_tweets_2021_05_01.loc[df_tweets_2021_05_01['credible'] == 0].copy()

    df_tweets_2021_06_01 = pd.read_csv('../reporting/tweet_ids--2021-06-01.csv')
    df_tweets_2021_06_01 = df_tweets_2021_06_01.loc[df_tweets_2021_06_01['credible'] == 0].copy()

    df_tweets_2021_07_01 = pd.read_csv('../reporting/tweet_ids--2021-07-01.csv')
    df_tweets_2021_07_01 = df_tweets_2021_07_01.loc[df_tweets_2021_07_01['credible'] == 0].copy()

    df_tweets_2021_08_01 = pd.read_csv('../reporting/tweet_ids--2021-08-01.csv')
    df_tweets_2021_08_01 = df_tweets_2021_08_01.loc[df_tweets_2021_08_01['credible'] == 0].copy()

    df_tweets_2021_09_01 = pd.read_csv('../reporting/tweet_ids--2021-09-01.csv')
    df_tweets_2021_09_01 = df_tweets_2021_09_01.loc[df_tweets_2021_09_01['credible'] == 0].copy()

    df_tweets_2021_10_01 = pd.read_csv('../reporting/tweet_ids--2021-10-01.csv')
    df_tweets_2021_10_01 = df_tweets_2021_10_01.loc[df_tweets_2021_10_01['credible'] == 0].copy()

    df_tweets_2021_11_01 = pd.read_csv('../reporting/tweet_ids--2021-11-01.csv')
    df_tweets_2021_11_01 = df_tweets_2021_11_01.loc[df_tweets_2021_11_01['credible'] == 0].copy()

    df_tweets_2021_12_01 = pd.read_csv('../reporting/tweet_ids--2021-12-01.csv')
    df_tweets_2021_12_01 = df_tweets_2021_12_01.loc[df_tweets_2021_12_01['credible'] == 0].copy()

    df_tweets_2021_01_11['created_at'] = pd.to_datetime(df_tweets_2021_01_11['created_at'])
    df_tweets_2021_01_11 = df_tweets_2021_01_11.set_index(['created_at'])
    hourly_count_2021_01_11 = df_tweets_2021_01_11.groupby(df_tweets_2021_01_11.index.hour).apply(f)
    save_figure("2021-01-11-NonCredible", hourly_count_2021_01_11)

    df_tweets_2021_02_01['created_at'] = pd.to_datetime(df_tweets_2021_02_01['created_at'])
    df_tweets_2021_02_01 = df_tweets_2021_02_01.set_index(['created_at'])
    hourly_count_2021_02_01 = df_tweets_2021_02_01.groupby(df_tweets_2021_02_01.index.hour).apply(f)
    save_figure("2021-02-01-NonCredible", hourly_count_2021_02_01)

    df_tweets_2021_03_01['created_at'] = pd.to_datetime(df_tweets_2021_03_01['created_at'])
    df_tweets_2021_03_01 = df_tweets_2021_03_01.set_index(['created_at'])
    hourly_count_2021_03_01 = df_tweets_2021_03_01.groupby(df_tweets_2021_03_01.index.hour).apply(f)
    save_figure("2021-03-01-NonCredible", hourly_count_2021_03_01)

    df_tweets_2021_04_01['created_at'] = pd.to_datetime(df_tweets_2021_04_01['created_at'])
    df_tweets_2021_04_01 = df_tweets_2021_04_01.set_index(['created_at'])
    hourly_count_2021_04_01 = df_tweets_2021_04_01.groupby(df_tweets_2021_04_01.index.hour).apply(f)
    save_figure("2021-04-01-NonCredible", hourly_count_2021_04_01)

    df_tweets_2021_05_01['created_at'] = pd.to_datetime(df_tweets_2021_05_01['created_at'])
    df_tweets_2021_05_01 = df_tweets_2021_05_01.set_index(['created_at'])
    hourly_count_2021_05_01 = df_tweets_2021_05_01.groupby(df_tweets_2021_05_01.index.hour).apply(f)
    save_figure("2021-05-01-NonCredible", hourly_count_2021_05_01)

    df_tweets_2021_06_01['created_at'] = pd.to_datetime(df_tweets_2021_06_01['created_at'])
    df_tweets_2021_06_01 = df_tweets_2021_06_01.set_index(['created_at'])
    hourly_count_2021_06_01 = df_tweets_2021_06_01.groupby(df_tweets_2021_06_01.index.hour).apply(f)
    save_figure("2021-06-01-NonCredible", hourly_count_2021_06_01)

    df_tweets_2021_07_01['created_at'] = pd.to_datetime(df_tweets_2021_07_01['created_at'])
    df_tweets_2021_07_01 = df_tweets_2021_07_01.set_index(['created_at'])
    hourly_count_2021_07_01 = df_tweets_2021_07_01.groupby(df_tweets_2021_07_01.index.hour).apply(f)
    save_figure("2021-07-01-NonCredible", hourly_count_2021_07_01)

    df_tweets_2021_08_01['created_at'] = pd.to_datetime(df_tweets_2021_08_01['created_at'])
    df_tweets_2021_08_01 = df_tweets_2021_08_01.set_index(['created_at'])
    hourly_count_2021_08_01 = df_tweets_2021_08_01.groupby(df_tweets_2021_08_01.index.hour).apply(f)
    save_figure("2021-08-01-NonCredible", hourly_count_2021_08_01)

    df_tweets_2021_09_01['created_at'] = pd.to_datetime(df_tweets_2021_09_01['created_at'])
    df_tweets_2021_09_01 = df_tweets_2021_09_01.set_index(['created_at'])
    hourly_count_2021_09_01 = df_tweets_2021_09_01.groupby(df_tweets_2021_09_01.index.hour).apply(f)
    save_figure("2021-09-01-NonCredible", hourly_count_2021_09_01)

    df_tweets_2021_10_01['created_at'] = pd.to_datetime(df_tweets_2021_10_01['created_at'])
    df_tweets_2021_10_01 = df_tweets_2021_10_01.set_index(['created_at'])
    hourly_count_2021_10_01 = df_tweets_2021_10_01.groupby(df_tweets_2021_10_01.index.hour).apply(f)
    save_figure("2021-10-01-NonCredible", hourly_count_2021_10_01)

    df_tweets_2021_11_01['created_at'] = pd.to_datetime(df_tweets_2021_11_01['created_at'])
    df_tweets_2021_11_01 = df_tweets_2021_11_01.set_index(['created_at'])
    hourly_count_2021_11_01 = df_tweets_2021_11_01.groupby(df_tweets_2021_11_01.index.hour).apply(f)
    save_figure("2021-11-01-NonCredible", hourly_count_2021_11_01)

    df_tweets_2021_12_01['created_at'] = pd.to_datetime(df_tweets_2021_12_01['created_at'])
    df_tweets_2021_12_01 = df_tweets_2021_12_01.set_index(['created_at'])
    hourly_count_2021_12_01 = df_tweets_2021_12_01.groupby(df_tweets_2021_12_01.index.hour).apply(f)
    save_figure("2021-12-01-NonCredible", hourly_count_2021_12_01)

    df = pd.DataFrame({'2021_01_11': hourly_count_2021_01_11['Number_of_tweets'],
                       '2021_02_01': hourly_count_2021_02_01['Number_of_tweets'],
                       '2021_03_01': hourly_count_2021_03_01['Number_of_tweets'],
                       '2021_04_01': hourly_count_2021_04_01['Number_of_tweets'],
                       '2021_05_01': hourly_count_2021_05_01['Number_of_tweets'],
                       '2021_06_01': hourly_count_2021_06_01['Number_of_tweets'],
                       '2021_07_01': hourly_count_2021_07_01['Number_of_tweets'],
                       '2021_08_01': hourly_count_2021_08_01['Number_of_tweets'],
                       '2021_09_01': hourly_count_2021_09_01['Number_of_tweets'],
                       '2021_10_01': hourly_count_2021_10_01['Number_of_tweets'],
                       '2021_11_01': hourly_count_2021_11_01['Number_of_tweets'],
                       '2021_12_01': hourly_count_2021_12_01['Number_of_tweets'],
                       })
    save_figure("First-Day-Of-Months-NonCredible", df)


def main():
    draw_graph()


def f(x):
    return Series(dict(Number_of_tweets=x['tweet_id'].count(), ))


if __name__ == '__main__':
    main()

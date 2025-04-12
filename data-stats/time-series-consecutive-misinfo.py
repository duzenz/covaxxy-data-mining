import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series


# def save_figure(title, dataframe):
#     fig, axs = plt.subplots(figsize=(20, 10))
#     dataframe.plot(rot=0, ax=axs, xlabel='Hour in day', ylabel='Tweet count')
#     plt.xticks(range(0, 24))
#     plt.title("", fontsize=30)
#     plt.savefig(title + ".png")

def save_figure(title, dataframe):
    # Set the figure size
    fig, axs = plt.subplots(figsize=(12, 6))

    # Plot the data
    dataframe.plot(rot=0, ax=axs, xlabel='Gün içerisindeki saat', ylabel='Atılan tweet sayısı', linewidth=2, marker='o', markersize=8)

    # Set the x-ticks to be from 0 to 23 (hours in a day)
    plt.xticks(range(0, 24))

    # Set the title with a larger font size
    plt.title("Ardışık 10 Günde Atılan ve Yanlış Bilgi İçeren Tweetler", fontsize=24, pad=20)

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
    df_tweets_2021_03_19 = pd.read_csv('../reporting/tweet_ids--2021-03-19.csv')
    df_tweets_2021_03_19 = df_tweets_2021_03_19.loc[df_tweets_2021_03_19['credible'] == 0].copy()

    df_tweets_2021_03_20 = pd.read_csv('../reporting/tweet_ids--2021-03-20.csv')
    df_tweets_2021_03_20 = df_tweets_2021_03_20.loc[df_tweets_2021_03_20['credible'] == 0].copy()

    df_tweets_2021_03_21 = pd.read_csv('../reporting/tweet_ids--2021-03-21.csv')
    df_tweets_2021_03_21 = df_tweets_2021_03_21.loc[df_tweets_2021_03_21['credible'] == 0].copy()

    df_tweets_2021_03_22 = pd.read_csv('../reporting/tweet_ids--2021-03-22.csv')
    df_tweets_2021_03_22 = df_tweets_2021_03_22.loc[df_tweets_2021_03_22['credible'] == 0].copy()

    df_tweets_2021_03_23 = pd.read_csv('../reporting/tweet_ids--2021-03-23.csv')
    df_tweets_2021_03_23 = df_tweets_2021_03_23.loc[df_tweets_2021_03_23['credible'] == 0].copy()

    df_tweets_2021_03_24 = pd.read_csv('../reporting/tweet_ids--2021-03-24.csv')
    df_tweets_2021_03_24 = df_tweets_2021_03_24.loc[df_tweets_2021_03_24['credible'] == 0].copy()

    df_tweets_2021_03_25 = pd.read_csv('../reporting/tweet_ids--2021-03-25.csv')
    df_tweets_2021_03_25 = df_tweets_2021_03_25.loc[df_tweets_2021_03_25['credible'] == 0].copy()

    df_tweets_2021_03_26 = pd.read_csv('../reporting/tweet_ids--2021-03-26.csv')
    df_tweets_2021_03_26 = df_tweets_2021_03_26.loc[df_tweets_2021_03_26['credible'] == 0].copy()

    df_tweets_2021_03_27 = pd.read_csv('../reporting/tweet_ids--2021-03-27.csv')
    df_tweets_2021_03_27 = df_tweets_2021_03_27.loc[df_tweets_2021_03_27['credible'] == 0].copy()

    df_tweets_2021_03_28 = pd.read_csv('../reporting/tweet_ids--2021-03-28.csv')
    df_tweets_2021_03_28 = df_tweets_2021_03_28.loc[df_tweets_2021_03_28['credible'] == 0].copy()

    df_tweets_2021_03_19['created_at'] = pd.to_datetime(df_tweets_2021_03_19['created_at'])
    df_tweets_2021_03_19 = df_tweets_2021_03_19.set_index(['created_at'])
    hourly_count_2021_03_19 = df_tweets_2021_03_19.groupby(df_tweets_2021_03_19.index.hour).apply(f)
    save_figure("2021-03-19-NonCredible", hourly_count_2021_03_19)

    df_tweets_2021_03_20['created_at'] = pd.to_datetime(df_tweets_2021_03_20['created_at'])
    df_tweets_2021_03_20 = df_tweets_2021_03_20.set_index(['created_at'])
    hourly_count_2021_03_20 = df_tweets_2021_03_20.groupby(df_tweets_2021_03_20.index.hour).apply(f)
    save_figure("2021-03-20-NonCredible", hourly_count_2021_03_20)

    df_tweets_2021_03_21['created_at'] = pd.to_datetime(df_tweets_2021_03_21['created_at'])
    df_tweets_2021_03_21 = df_tweets_2021_03_21.set_index(['created_at'])
    hourly_count_2021_03_21 = df_tweets_2021_03_21.groupby(df_tweets_2021_03_21.index.hour).apply(f)
    save_figure("2021-03-21-NonCredible", hourly_count_2021_03_21)

    df_tweets_2021_03_22['created_at'] = pd.to_datetime(df_tweets_2021_03_22['created_at'])
    df_tweets_2021_03_22 = df_tweets_2021_03_22.set_index(['created_at'])
    hourly_count_2021_03_22 = df_tweets_2021_03_22.groupby(df_tweets_2021_03_22.index.hour).apply(f)
    save_figure("2021-03-22-NonCredible", hourly_count_2021_03_22)

    df_tweets_2021_03_23['created_at'] = pd.to_datetime(df_tweets_2021_03_23['created_at'])
    df_tweets_2021_03_23 = df_tweets_2021_03_23.set_index(['created_at'])
    hourly_count_2021_03_23 = df_tweets_2021_03_23.groupby(df_tweets_2021_03_23.index.hour).apply(f)
    save_figure("2021-03-23-NonCredible", hourly_count_2021_03_23)

    df_tweets_2021_03_24['created_at'] = pd.to_datetime(df_tweets_2021_03_24['created_at'])
    df_tweets_2021_03_24 = df_tweets_2021_03_24.set_index(['created_at'])
    hourly_count_2021_03_24 = df_tweets_2021_03_24.groupby(df_tweets_2021_03_24.index.hour).apply(f)
    save_figure("2021-03-24-NonCredible", hourly_count_2021_03_24)

    df_tweets_2021_03_25['created_at'] = pd.to_datetime(df_tweets_2021_03_25['created_at'])
    df_tweets_2021_03_25 = df_tweets_2021_03_25.set_index(['created_at'])
    hourly_count_2021_03_25 = df_tweets_2021_03_25.groupby(df_tweets_2021_03_25.index.hour).apply(f)
    save_figure("2021-03-25-NonCredible", hourly_count_2021_03_25)

    df_tweets_2021_03_26['created_at'] = pd.to_datetime(df_tweets_2021_03_26['created_at'])
    df_tweets_2021_03_26 = df_tweets_2021_03_26.set_index(['created_at'])
    hourly_count_2021_03_26 = df_tweets_2021_03_26.groupby(df_tweets_2021_03_26.index.hour).apply(f)
    save_figure("2021-03-26-NonCredible", hourly_count_2021_03_26)

    df_tweets_2021_03_27['created_at'] = pd.to_datetime(df_tweets_2021_03_27['created_at'])
    df_tweets_2021_03_27 = df_tweets_2021_03_27.set_index(['created_at'])
    hourly_count_2021_03_27 = df_tweets_2021_03_27.groupby(df_tweets_2021_03_27.index.hour).apply(f)
    save_figure("2021-03-27-NonCredible", hourly_count_2021_03_27)

    df_tweets_2021_03_28['created_at'] = pd.to_datetime(df_tweets_2021_03_28['created_at'])
    df_tweets_2021_03_28 = df_tweets_2021_03_28.set_index(['created_at'])
    hourly_count_2021_03_28 = df_tweets_2021_03_28.groupby(df_tweets_2021_03_28.index.hour).apply(f)
    save_figure("2021-03-28-NonCredible", hourly_count_2021_03_28)

    df = pd.DataFrame({'2021_03_19': hourly_count_2021_03_19['Number_of_tweets'],
                       '2021_03_20': hourly_count_2021_03_20['Number_of_tweets'],
                       '2021_03_21': hourly_count_2021_03_21['Number_of_tweets'],
                       '2021_03_22': hourly_count_2021_03_22['Number_of_tweets'],
                       '2021_03_23': hourly_count_2021_03_23['Number_of_tweets'],
                       '2021_03_24': hourly_count_2021_03_24['Number_of_tweets'],
                       '2021_03_25': hourly_count_2021_03_25['Number_of_tweets'],
                       '2021_03_26': hourly_count_2021_03_26['Number_of_tweets'],
                       '2021_03_27': hourly_count_2021_03_27['Number_of_tweets'],
                       '2021_03_28': hourly_count_2021_03_28['Number_of_tweets'],
                       })
    save_figure("Consecutive-NonCredible", df)


def main():
    draw_graph()


def f(x):
    return Series(dict(Number_of_tweets=x['tweet_id'].count(), ))


if __name__ == '__main__':
    main()

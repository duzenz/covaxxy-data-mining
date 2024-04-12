import csv
import os
import pandas as pd

DOWNLOADS_FOLDER = "../../reporting/"


def main():
    # header = ['filename', 'date', 'tweet-count', 'credible-count', 'not-credible-count', 'most-active-user', 'most-active-tweet-count']
    # writer.writerow(header)

    for (root, dirs, fileSub) in os.walk(DOWNLOADS_FOLDER):
        for filename in fileSub:
            print(filename)
            date = filename.split('/')[-1].split('.')[0].split("--")[1]
            f = open('popularity-non-credible-users-' + date + '.csv', 'w', encoding="utf-8", newline='')
            writer = csv.writer(f)
            header = ['username', 'date', 'tweet-count', 'followers-count', 'following-count']
            writer.writerow(header)

            tweets = pd.read_csv(DOWNLOADS_FOLDER + filename)

            # get non credible ones
            non_credible = tweets.loc[tweets['credible'] == 0]

            # get all distinct users of non-credible
            non_credible_users = non_credible['username'].unique()

            for user in non_credible_users:
                # for each user we need to add a row to csv file
                # 1. username
                # 2. date
                # 3. tweet count
                # 4. followers count
                # 5. following count

                tweet_count = len(non_credible.loc[non_credible['username'] == user])
                followers_count = non_credible.loc[non_credible['username'] == user].iloc[0]['followers_count']
                following_count = non_credible.loc[non_credible['username'] == user].iloc[0]['following_count']
                writer.writerow([user, date, tweet_count, followers_count, following_count])

            f.close()
            # tweet_count = len(tweets)
            # dictionary = tweets['username'].value_counts().nlargest(1).to_dict()
            # createMostActiveUserCsv(date, tweets['username'].value_counts().nlargest(5).to_dict())
            # credible_count = len(tweets.loc[tweets['credible'] == 1])
            # not_credible_count = len(tweets.loc[tweets['credible'] == 0])
            # writer.writerow(
            #     [filename, date, tweet_count, credible_count, not_credible_count, list(dictionary.keys())[0], list(dictionary.values())[0]])
        break

    # f.close()


def createMostActiveUserCsv(date, dictionary):
    filefile = open(str(date) + '-5.csv', 'w', encoding="utf-8", newline='')
    writer2 = csv.writer(filefile)
    header2 = ['username', 'tweet-count']
    writer2.writerow(header2)
    for key, value in dictionary.items():
        writer2.writerow([key, value])
    filefile.close()


if __name__ == '__main__':
    main()

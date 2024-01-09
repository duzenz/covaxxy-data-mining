import csv
import os
import pandas as pd

DOWNLOADS_FOLDER = "../../reporting/"


def main():
    f = open('statistics.csv', 'w', encoding="utf-8", newline='')
    writer = csv.writer(f)
    header = ['filename', 'credible-count', 'not-credible-count']
    writer.writerow(header)

    for (root, dirs, fileSub) in os.walk(DOWNLOADS_FOLDER):
        for filename in fileSub:
            print(filename)
            # read csv into pandas dataframe
            tweets = pd.read_csv(DOWNLOADS_FOLDER + filename)
            credible_count = len(tweets.loc[tweets['credible'] == 1])
            not_credible_count = len(tweets.loc[tweets['credible'] == 0])
            writer.writerow([filename, credible_count, not_credible_count])
        break

    f.close()


if __name__ == '__main__':
    main()

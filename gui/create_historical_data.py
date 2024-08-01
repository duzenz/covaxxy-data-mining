import csv
import pickle
from datetime import date

import networkx as nx
import pandas as pd
import textstat as tx

from create_daily_csv_select_columns import daterange


def main():
    dataframes = get_training_dataframes()

    file = open('historical.csv', 'w', encoding="utf-8", newline='')
    header = ["user_influence", "network", "metric_type", "metric_value", "readability", "multimedia_presence", "reach", "longevity"]
    writer = csv.writer(file)
    writer.writerow(header)

    # train data for 20 days
    start_date = date(2021, 3, 1)
    end_date = date(2021, 3, 16)
    for single_date in daterange(start_date, end_date):
        print("Started Date:" + str(single_date))
        current_data_frame = dataframes[str(single_date)]
        retweets_network = pickle.load(open("networks/retweets-network-" + str(single_date) + ".pickle", 'rb'))
        # mentions_network = pickle.load(open("networks/mentions-network-" + str(single_date) + ".pickle", 'rb'))
        # replies_network = pickle.load(open("net
        # ,++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++works/replies-network-" + str(single_date) + ".pickle", 'rb'))
        print("Total retweet network node numbers: " + str(nx.number_of_nodes(retweets_network)))
        # print("Total mention network node numbers: " + str(nx.number_of_nodes(mentions_network)))
        # print("Total reply network node numbers: " + str(nx.number_of_nodes(replies_network)))
        retweet_degree_centrality_dictionary = nx.degree_centrality(retweets_network)
        # mention_degree_centrality_dictionary = nx.degree_centrality(mentions_network)
        # reply_degree_centrality_dictionary = nx.degree_centrality(replies_network)

        for key in retweet_degree_centrality_dictionary:
            edge_attributes = get_edge_attributes(retweets_network, key)

            try:
                user_row = current_data_frame.loc[current_data_frame['username'] == key].to_dict(orient='records')[0]
                # print(user_row)
            except:
                continue

            user_engagement_rate = calculate_user_engagement(current_data_frame, key)
            network_value = get_network_value('retweet')
            metric_type = get_metric_type_value('degree')
            metric_value = "{:.4f}".format(retweet_degree_centrality_dictionary[key])

            for edge_key in edge_attributes:
                # find in dataframe where username is key and retweet_id is edge_attributes[edge_key]['retweet_id']
                reacted_tweet = current_data_frame.loc[(current_data_frame['username'] == key) & (current_data_frame['retweet_id'] == edge_attributes[edge_key]['retweet_id'])].to_dict(orient='records')[0]
                readability_value = calculate_readability(reacted_tweet['text'])
                multimedia_presence_value = int('//t.co/' in reacted_tweet['text'])
                reach_value = calculate_reach_of_tweet(reacted_tweet)
                longevity_value = calculate_longevity_of_tweet(dataframes, reacted_tweet, network_value)
                user_influence = calculate_user_influence(user_engagement_rate, reacted_tweet)

                writer.writerow(["{:.4f}".format(user_influence), network_value, metric_type, metric_value, readability_value, multimedia_presence_value, reach_value, longevity_value])
                break

        for key in mention_degree_centrality_dictionary:
            edge_attributes = get_edge_attributes(mentions_network, key)

            try:
                user_row = current_data_frame.loc[current_data_frame['username'] == key].to_dict(orient='records')[0]
                # print(user_row)
            except:
                continue

            user_engagement_rate = calculate_user_engagement(current_data_frame, key)
            network_value = get_network_value('mention')
            metric_type = get_metric_type_value('degree')
            metric_value = "{:.4f}".format(mention_degree_centrality_dictionary[key])

            for edge_key in edge_attributes:
                # find in dataframe where username is key and user_mentions_id is edge_attributes[edge_key]['user_mentions_id']
                reacted_tweet = current_data_frame.loc[(current_data_frame['username'] == key) & (current_data_frame['user_mentions_id'] == edge_attributes[edge_key]['user_mentions_id'])].to_dict(orient='records')[0]
                readability_value = calculate_readability(reacted_tweet['text'])
                multimedia_presence_value = int('//t.co/' in reacted_tweet['text'])
                reach_value = calculate_reach_of_tweet(reacted_tweet)
                longevity_value = calculate_longevity_of_tweet(dataframes, reacted_tweet, network_value)
                user_influence = calculate_user_influence(user_engagement_rate, reacted_tweet)

                writer.writerow(["{:.4f}".format(user_influence), network_value, metric_type, metric_value, readability_value, multimedia_presence_value, reach_value, longevity_value])
                break

        for key in reply_degree_centrality_dictionary:
            edge_attributes = get_edge_attributes(replies_network, key)

            try:
                user_row = current_data_frame.loc[current_data_frame['username'] == key].to_dict(orient='records')[0]
                # print(user_row)
            except:
                continue

            user_engagement_rate = calculate_user_engagement(current_data_frame, key)
            network_value = get_network_value('reply')
            metric_type = get_metric_type_value('degree')
            metric_value = "{:.4f}".format(reply_degree_centrality_dictionary[key])

            for edge_key in edge_attributes:
                # find in dataframe where username is key and in_reply_to_tweet_id is edge_attributes[edge_key]['in_reply_to_tweet_id']
                reacted_tweet = current_data_frame.loc[(current_data_frame['username'] == key) & (current_data_frame['in_reply_to_tweet_id'] == edge_attributes[edge_key]['in_reply_to_tweet_id'])].to_dict(orient='records')[0]
                readability_value = calculate_readability(reacted_tweet['text'])
                multimedia_presence_value = int('//t.co/' in reacted_tweet['text'])
                reach_value = calculate_reach_of_tweet(reacted_tweet)
                longevity_value = calculate_longevity_of_tweet(dataframes, reacted_tweet, network_value)
                user_influence = calculate_user_influence(user_engagement_rate, reacted_tweet)

                writer.writerow(["{:.4f}".format(user_influence), network_value, metric_type, metric_value, readability_value, multimedia_presence_value, reach_value, longevity_value])
                break

        print("Finished Date:" + str(single_date))

    file.close()


def get_metric_type_value(type):
    if type == 'degree':
        return 1
    elif type == 'betweenness':
        return 2
    elif type == 'eigenvector':
        return 3
    elif type == 'closeness':
        return 4
    elif type == 'katz':
        return 5
    else:
        return


def get_network_value(type):
    if type == 'retweet':
        return 1
    elif type == 'reply':
        return 2
    elif type == 'mention':
        return 3
    else:
        return 0


def get_edge_attributes(network, key):
    edge_attributes = {}
    for neighbor in network.neighbors(key):
        edge_attributes[neighbor] = network.get_edge_data(key, neighbor)
    return edge_attributes


def calculate_readability(content):
    return tx.textstat.flesch_reading_ease(content)


def calculate_reach_of_tweet(tweet_row):
    return tweet_row['followers_count'] + tweet_row['like_count'] + tweet_row['quote_count'] + tweet_row['reply_count'] + tweet_row['retweet_count']


def calculate_user_influence(engagement_rate, tweet_row):
    followers_count = (tweet_row['followers_count'] - 0) / (10000000 - tweet_row['followers_count'])  # normalized 0 - 1
    verified = 1 if tweet_row['verified'] else 0
    like_count = tweet_row['like_count']
    quote_count = tweet_row['quote_count']
    reply_count = tweet_row['reply_count']
    retweet_count = tweet_row['retweet_count']
    total_reaction = like_count + quote_count + reply_count + retweet_count
    respond_rate = total_reaction / (175000 - total_reaction)  # normalized 0 - 1

    # calculate respond rate to user from like, quote, reply, retweet counts
    user_influence = followers_count * 0.4425 + engagement_rate * 0.1753 + respond_rate * 0.1753 + verified * 0.07
    return user_influence


def calculate_longevity_of_tweet(dataframes, tweet_row, network_value):
    count = 0
    for key in dataframes:
        reference_id = '#'
        compare_key = 'reference_id'
        if network_value == 1:
            compare_key = 'retweet_id'
            reference_id = tweet_row[compare_key]
        elif network_value == 2:
            compare_key = 'in_reply_to_tweet_id'
            reference_id = tweet_row[compare_key]
        elif network_value == 3:
            compare_key = 'user_mentions_id'
            reference_id = tweet_row[compare_key]

        if reference_id == '#':
            compare_key = 'reference_id'
            reference_id = tweet_row['tweet_id']

        found = dataframes[key].loc[dataframes[key][compare_key] == str(reference_id)]
        if not found.empty:
            count += 1
    return count


def calculate_user_engagement(current_data_frame, user_name):
    user_daily_tweet_count = current_data_frame.loc[current_data_frame['username'] == user_name].shape[0]
    user_daily_retweet_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['retweet_id'] != '#')].shape[0]
    user_daily_mention_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['user_mentions_id'] != '#')].shape[0]
    user_daily_reply_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['in_reply_to_tweet_id'] != '#')].shape[0]

    retweet_rate = user_daily_retweet_count / user_daily_tweet_count
    reply_rate = user_daily_reply_count / user_daily_tweet_count
    mention_rate = user_daily_mention_count / user_daily_tweet_count
    other_tweet_rate = 1 - retweet_rate - reply_rate - mention_rate

    return retweet_rate * 0.519 + reply_rate * 0.201 + mention_rate * 0.201 + other_tweet_rate * 0.079


def get_training_dataframes():
    dataframes = {'2021-03-01': pd.read_csv("../reporting/tweet_ids--2021-03-01.csv"),
                  '2021-03-02': pd.read_csv("../reporting/tweet_ids--2021-03-02.csv"),
                  '2021-03-03': pd.read_csv("../reporting/tweet_ids--2021-03-03.csv"),
                  '2021-03-04': pd.read_csv("../reporting/tweet_ids--2021-03-04.csv"),
                  '2021-03-05': pd.read_csv("../reporting/tweet_ids--2021-03-05.csv"),
                  '2021-03-06': pd.read_csv("../reporting/tweet_ids--2021-03-06.csv"),
                  '2021-03-07': pd.read_csv("../reporting/tweet_ids--2021-03-07.csv"),
                  '2021-03-08': pd.read_csv("../reporting/tweet_ids--2021-03-08.csv"),
                  '2021-03-09': pd.read_csv("../reporting/tweet_ids--2021-03-09.csv"),
                  '2021-03-10': pd.read_csv("../reporting/tweet_ids--2021-03-10.csv"),
                  '2021-03-11': pd.read_csv("../reporting/tweet_ids--2021-03-11.csv"),
                  '2021-03-12': pd.read_csv("../reporting/tweet_ids--2021-03-12.csv"),
                  '2021-03-13': pd.read_csv("../reporting/tweet_ids--2021-03-13.csv"),
                  '2021-03-14': pd.read_csv("../reporting/tweet_ids--2021-03-14.csv"),
                  '2021-03-15': pd.read_csv("../reporting/tweet_ids--2021-03-15.csv")}
    return dataframes


if __name__ == '__main__':
    main()

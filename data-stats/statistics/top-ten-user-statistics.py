import csv
import itertools

import networkx as nx
import numpy as np
import pandas as pd
import textstat as tx


def calculate_user_engagement(user_profile):
    retweet_rate = user_profile['retweet_rate']
    reply_rate = user_profile['reply_rate']
    mention_rate = user_profile['mention_rate']
    other_tweet_rate = 1 - retweet_rate - reply_rate - mention_rate

    return retweet_rate * 0.35 + reply_rate * 0.25 + mention_rate * 0.25 + other_tweet_rate * 0.15


def calculate_user_influence(engagement_rate, user_profile):
    followers_count = user_profile['follower_count'] / 1000
    verified = 1 if user_profile['is_verified'] else 0
    like_count = user_profile['like_count']
    quote_count = user_profile['quote_count']
    reply_count = user_profile['reply_count']
    retweet_count = user_profile['retweet_count']

    # calculate respond rate to user from like, quote, reply, retweet counts
    respond_rate = (like_count + quote_count + reply_count + retweet_count) / 100
    user_influence = followers_count * 0.4 + engagement_rate * 0.25 + respond_rate * 0.25 + verified * 0.1
    return user_influence


def calculate_readability(content):
    return tx.textstat.flesch_reading_ease(content)


def extract_features(tweet, user_profile, network):
    # Extract features for prediction
    user_engagement_value = calculate_user_engagement(user_profile)
    user_influence = calculate_user_influence(user_engagement_value, user_profile)
    # centrality = 0.08147174770039423
    centrality = nx.degree_centrality(network)[tweet['username']]
    # if metric_type == 'degree_centrality':
    #     centrality = nx.degree_centrality(network)[tweet['author_id']]
    # elif metric_type == 'betweenness_centrality':
    #     centrality = nx.betweenness_centrality(network)[tweet['author_id']]
    # elif metric_type == 'eigenvector_centrality':
    #     centrality = nx.eigenvector_centrality(network)[tweet['author_id']]
    readability = calculate_readability(tweet['text'])
    multimedia_presence = int('//t.co/' in tweet['text'])

    return np.array([user_influence, 1, 1, centrality, readability, multimedia_presence])


def calculate_impact_factor(tweet, user_profile, network, reach_model, longevity_model):
    # Extract features
    features = extract_features(tweet, user_profile, network)

    # Predict reach and longevity
    predicted_reach = reach_model.predict([features])[0]
    predicted_longevity = longevity_model.predict([features])[0]

    return calculate_impact_score(predicted_reach, predicted_longevity), predicted_reach, predicted_longevity


def calculate_impact_score(reach, longevity):
    # Step 1: Normalize reach and longevity
    normalized_reach = reach / 10000000  # Scale reach to 0-1 range
    normalized_longevity = longevity / 15  # Scale longevity to 0-1 range

    # Step 2: Combine the normalized values to calculate the raw impact score
    # Let's assume we want to give equal weight to reach and longevity
    raw_score = (normalized_reach + normalized_longevity) / 2

    # Step 3: Normalize the raw score to a 0-10 range
    impact_score = raw_score * 10

    # Step 4: Ensure the score has more than 3 decimal places
    impact_score = round(impact_score, 4)

    return impact_score


def get_retweets_graph(df, min_connection_count):
    graph_retweets = nx.from_pandas_edgelist(df[df.retweeted_screen_name != '#'], 'username', 'retweeted_screen_name',
                                             ['author_id', 'retweet_author_id', 'retweet_id'],
                                             create_using=nx.DiGraph())
    return get_graph(graph_retweets, min_connection_count)


def get_graph(graph, min_connection_count):
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, min_connection_count)
    return graph


def get_user_profile_from_tweet_row(tweet_row, user_engagement_rates):
    return {
        'follower_count': tweet_row['followers_count'],
        'retweet_rate': user_engagement_rates['retweet_rate'],
        'reply_rate': user_engagement_rates['reply_rate'],
        'mention_rate': user_engagement_rates['mention_rate'],
        'is_verified': 1 if tweet_row['verified'] else 0,
        'like_count': tweet_row['like_count'],
        'quote_count': tweet_row['quote_count'],
        'reply_count': tweet_row['reply_count'],
        'retweet_count': tweet_row['retweet_count']
    }


def get_user_engagement_rates(current_data_frame, user_name):
    user_daily_tweet_count = current_data_frame.loc[current_data_frame['username'] == user_name].shape[0]
    user_daily_retweet_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['retweet_id'] != '#')].shape[0]
    user_daily_mention_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['user_mentions_id'] != '#')].shape[0]
    user_daily_reply_count = current_data_frame.loc[(current_data_frame['username'] == user_name) & (current_data_frame['in_reply_to_tweet_id'] != '#')].shape[0]
    if user_daily_tweet_count == 0:
        return {"retweet_rate": 0, "reply_rate": 0, "mention_rate": 0}
    retweet_rate = user_daily_retweet_count / user_daily_tweet_count
    reply_rate = user_daily_reply_count / user_daily_tweet_count
    mention_rate = user_daily_mention_count / user_daily_tweet_count
    return {"retweet_rate": retweet_rate, "reply_rate": reply_rate, "mention_rate": mention_rate}


def calculate_reach_of_tweet(tweet_row):
    return tweet_row['followers_count'] + tweet_row['like_count'] + tweet_row['quote_count'] + tweet_row['reply_count'] + tweet_row['retweet_count']


def get_edge_attributes(network, key):
    edge_attributes = {}
    for neighbor in network.neighbors(key):
        edge_attributes[neighbor] = network.get_edge_data(key, neighbor)
    return edge_attributes


df = pd.read_csv("../../reporting/tweet_ids--2021-03-16.csv")
network = get_retweets_graph(df, 7)
retweet_degree_centrality_dictionary = nx.degree_centrality(network)
retweet_betweenness_centrality_dictionary = nx.betweenness_centrality(network)
retweet_closeness_centrality_dictionary = nx.closeness_centrality(network)
influential_nodes = dict(itertools.islice(dict(sorted(retweet_degree_centrality_dictionary.items(), key=lambda item: item[1], reverse=True)).items(), 15))

# for each key in dictionary print key and value
# o günkü değerler diye koyucaz bunu

file = open('top-user-statistics.csv', 'w', encoding="utf-8", newline='')
header = ["username", "user_influence", "degree", "betweenness", "closeness"]
writer = csv.writer(file)
writer.writerow(header)

for key in influential_nodes:
    user_engagement_rates = get_user_engagement_rates(df, key)

    try:
        row = df.loc[df['username'] == key].tail(1).to_dict(orient='records')[0]
    except:
        continue
    user_profile = get_user_profile_from_tweet_row(row, user_engagement_rates)
    user_engagement_value = calculate_user_engagement(user_profile)
    user_influence = calculate_user_influence(user_engagement_value, user_profile)
    print(key, retweet_degree_centrality_dictionary[key])
    print(key, retweet_betweenness_centrality_dictionary[key])
    print(key, retweet_closeness_centrality_dictionary[key])
    writer.writerow([key, "{:.2f}".format(user_influence), "{:.4f}".format(retweet_degree_centrality_dictionary[key]), "{:.4f}".format(retweet_betweenness_centrality_dictionary[key]), "{:.4f}".format(retweet_closeness_centrality_dictionary[key])])

file.close()

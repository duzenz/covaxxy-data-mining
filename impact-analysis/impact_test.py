import csv
import itertools
import math

import networkx as nx
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
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


def train_models(historical_data):
    # Train reach prediction model
    reach_model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor())
    ])

    # user_influence,network,metric_type,metric_value,readability,multimedia_presence,reach,longevity
    X = historical_data[['user_influence', 'network', 'metric_type', 'metric_value', 'readability', 'multimedia_presence']]
    y_reach = historical_data['reach']

    reach_model.fit(X, y_reach)

    # Train longevity prediction model
    longevity_model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor())
    ])

    y_longevity = historical_data['longevity']

    longevity_model.fit(X, y_longevity)

    return reach_model, longevity_model


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


def get_metric_type_value(metric_type):
    if metric_type == 'degree':
        return 1
    elif metric_type == 'betweenness':
        return 2
    elif metric_type == 'eigenvector':
        return 3
    elif metric_type == 'closeness':
        return 4
    elif metric_type == 'katz':
        return 5
    else:
        return


def get_network_value(network_type):
    if network_type == 'retweet':
        return 1
    elif network_type == 'reply':
        return 2
    elif network_type == 'mention':
        return 3
    else:
        return 0


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


def get_next_dataframes():
    return {
        '2021-03-17': pd.read_csv("../reporting/tweet_ids--2021-03-17.csv"),
        '2021-03-18': pd.read_csv("../reporting/tweet_ids--2021-03-18.csv"),
        '2021-03-19': pd.read_csv("../reporting/tweet_ids--2021-03-19.csv"),
        '2021-03-20': pd.read_csv("../reporting/tweet_ids--2021-03-20.csv"),
        '2021-03-21': pd.read_csv("../reporting/tweet_ids--2021-03-21.csv"),
        '2021-03-22': pd.read_csv("../reporting/tweet_ids--2021-03-22.csv"),
        '2021-03-23': pd.read_csv("../reporting/tweet_ids--2021-03-23.csv"),
        '2021-03-24': pd.read_csv("../reporting/tweet_ids--2021-03-24.csv"),
        '2021-03-25': pd.read_csv("../reporting/tweet_ids--2021-03-25.csv"),
        '2021-03-26': pd.read_csv("../reporting/tweet_ids--2021-03-26.csv"),
        '2021-03-27': pd.read_csv("../reporting/tweet_ids--2021-03-27.csv"),
        '2021-03-28': pd.read_csv("../reporting/tweet_ids--2021-03-28.csv"),
        '2021-03-29': pd.read_csv("../reporting/tweet_ids--2021-03-29.csv"),
        '2021-03-30': pd.read_csv("../reporting/tweet_ids--2021-03-30.csv"),
        '2021-03-31': pd.read_csv("../reporting/tweet_ids--2021-03-31.csv"),
    }


def calculate_longevity_of_tweet(dataframes, tweet_row):
    count = 0
    for key in dataframes:
        reference_id = tweet_row['retweet_id']
        if reference_id == '#':
            reference_id = tweet_row['tweet_id']
        found = dataframes[key].loc[dataframes[key]['retweet_id'] == str(reference_id)]
        if not found.empty:
            count += 1
    return count


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


def get_edge_attributes(network, key):
    edge_attributes = {}
    for neighbor in network.neighbors(key):
        edge_attributes[neighbor] = network.get_edge_data(key, neighbor)
    return edge_attributes


df = pd.read_csv("../reporting/tweet_ids--2021-03-16.csv")
network = get_retweets_graph(df, 7)
retweet_degree_centrality_dictionary = nx.degree_centrality(network)
influential_nodes = dict(itertools.islice(dict(sorted(retweet_degree_centrality_dictionary.items(), key=lambda item: item[1], reverse=True)).items(), 15))
dataframes = get_next_dataframes()

historical_data = pd.read_csv('historical15-latest.csv')
print("historical data loaded")
reach_model, longevity_model = train_models(historical_data)
print("models trained")

file = open('test-results.csv', 'w', encoding="utf-8", newline='')
header = ["tweet_id", "is_misinformation", "metric_value", "reach", "longevity", "predicted_reach", "predicted_longevity", "impact_factor"]
writer = csv.writer(file)
writer.writerow(header)

# for each key in dictionary print key and value
for key in influential_nodes:
    print(key, influential_nodes[key])
    edge_attributes = get_edge_attributes(network, key)
    user_engagement_rates = get_user_engagement_rates(df, key)

    # find all tweets of this username in the dataframe
    df_tweets = df.loc[df['username'] == key]
    for index, row in df_tweets.iterrows():
        # for edge_key in edge_attributes:
        # row = df.loc[(df['username'] == key) & (df['retweet_id'] == edge_attributes[edge_key]['retweet_id'])].to_dict(orient='records')[0]
        print(row['tweet_id'], row['text'])

        current_reach = calculate_reach_of_tweet(row)
        print(f"Current Reach: {current_reach}")
        current_longevity = calculate_longevity_of_tweet(dataframes, row, 1)
        print(f"Current Longevity: {current_longevity}")
        user_profile = get_user_profile_from_tweet_row(row, user_engagement_rates)
        impact_factor, reach, longevity = calculate_impact_factor(row, user_profile, network, reach_model, longevity_model)
        print(f"Impact Factor: {impact_factor}, Predicted Reach: {reach}, Predicted Longevity: {longevity}")
        print("done")
        writer.writerow([row['tweet_id'], row['credible'], "{:.4f}".format(retweet_degree_centrality_dictionary[key]), current_reach, current_longevity, math.floor(reach), longevity, impact_factor])

file.close()

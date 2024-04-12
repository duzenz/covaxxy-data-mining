import json
import random
from datetime import date, timedelta

import networkx as nx
import pandas as pd
import csv

random.seed(5)
REPORTING_FOLDER = "../reporting/"


def get_survival_type(survival_info, key):
    survival_type = ''
    if survival_info[key] >= 7:
        survival_type = "long"
    elif survival_info[key] >= 4:
        survival_type = "mid"
    elif survival_info[key] >= 1:
        survival_type = "short"
    return survival_type


def get_non_credible_author(row):
    if row['reference_type'] == 'replied_to':
        return row['in_reply_to_username']
    elif row['reference_type'] == 'retweeted':
        return row['retweeted_screen_name']
    else:
        return row['user_mentions_screen_name']


def insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, centrality_type, writer, row):
    centrality_of_community = {community: centrality_dict[centrality_type][community] for community in community_unique}
    sorted_community_of_centrality = dict(sorted(centrality_of_community.items(), key=lambda item: item[1], reverse=True))

    writer.writerow([key, username, survival_type, network_type, centrality_type,
                     str(centrality_dict[centrality_type][username]),
                     str(len(sorted_community_of_centrality)),
                     str(list(sorted_community_of_centrality.keys()).index(username) + 1),
                     row["followers_count"], row["following_count"]
                     ])


def measure_importance(survival_info, non_credible_frame, communities, centrality_dict, network_type, writer):
    for key in survival_info.keys():
        survival_type = get_survival_type(survival_info, key)

        row = non_credible_frame.loc[non_credible_frame['reference_id'] == key].iloc[0]
        username = get_non_credible_author(row)

        user_found_in_communities = False
        for community in communities:
            if username in community:
                user_found_in_communities = True
                community_unique = list(dict.fromkeys(community))

                #insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_degree", writer, row)
                #insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_closeness", writer, row)
                #insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_betweenness", writer, row)
                insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_eigenvector", writer, row)
                #insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_katz", writer, row)
                insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_pagerank", writer, row)
                insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_load", writer, row)
                insert_rows(centrality_dict, community_unique, username, key, survival_type, network_type, "graph_harmonic", writer, row)
                break
        if not user_found_in_communities:
            writer.writerow([key, username, survival_type, network_type, "#", "#", "#", "#", "#", "#"])
    return 0


def get_retweet_network(data):
    graph = nx.from_pandas_edgelist(data[data.retweeted_screen_name != '#'], 'username',
                                    'retweeted_screen_name', ['author_id', 'retweet_author_id', 'retweet_id'],
                                    create_using=nx.DiGraph())
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, 4)
    return graph


def get_mention_network(data):
    graph = nx.from_pandas_edgelist(data[data.user_mentions_screen_name != '#'], 'username',
                                    'user_mentions_screen_name',
                                    ['author_id', 'user_mentions_id'],
                                    create_using=nx.DiGraph())
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, 4)
    return graph


def get_reply_network(data):
    graph = nx.from_pandas_edgelist(data[data.in_reply_to_username != '#'], 'username', 'in_reply_to_username',
                                    ['author_id', 'in_reply_to_tweet_id', 'in_reply_to_user_id'],
                                    create_using=nx.DiGraph())
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, 3)
    return graph


def read_retweet_communities(single_date):
    with open('retweets-community-' + single_date + '.txt', 'r') as filehandle:
        retweet_communities = json.load(filehandle)
    return retweet_communities


def read_mention_communities(single_date):
    with open('mentions-community-' + single_date + '.txt', 'r') as filehandle:
        mention_communities = json.load(filehandle)
    return mention_communities


def read_reply_communities(single_date):
    with open('replies-community-' + single_date + '.txt', 'r') as filehandle:
        reply_communities = json.load(filehandle)
    return reply_communities


def read_non_credible_survival_information(single_date):
    with open(single_date + '-recurrence.json', 'r') as filehandle:
        survival_info = json.load(filehandle)
    return survival_info


def read_graphs(graph):
    # graph_betweenness1 = nx.betweenness_centrality(graph, normalized=True)
    # with open("test1.json", 'w') as filehandle:
    #     json.dump(graph_betweenness1, filehandle)
    #
    # graph_betweenness2 = nx.betweenness_centrality(graph, k=200, seed=20, normalized=False)
    # TODO add as documents
    return {
        # "graph_degree": nx.degree_centrality(graph),
        # "graph_closeness": nx.closeness_centrality(graph),
        # "graph_betweenness": nx.betweenness_centrality(graph),
        "graph_eigenvector": nx.eigenvector_centrality(graph),
       # "graph_katz": nx.katz_centrality(graph, max_iter=1000),
        "graph_pagerank": nx.pagerank(graph),
        "graph_load": nx.load_centrality(graph),
        "graph_harmonic": nx.harmonic_centrality(graph),
    }



def main():
    start_date = date(2021, 3, 1)
    end_date = date(2021, 3, 2)
    for single_date in daterange(start_date, end_date):
        single_date = str(single_date)

        file = open(single_date + '-importance-report.csv', 'w', encoding="utf-8", newline='')
        header = ["tweet-id", "tweet-author", "survival-type", "network-type", "centrality-type", "centrality-measure",
                  "community-node-count", "importance-order-in-community", "followers_count", "following_count"]
        writer = csv.writer(file)
        writer.writerow(header)

        # read tweets
        df_tweets_all = pd.read_csv('../reporting/tweet_ids--' + single_date + '.csv')

        # read misinformation tweets
        df_tweets_non_credible = df_tweets_all.loc[df_tweets_all['credible'] == 0].copy()

        # read survival info of non-credible tweets
        survival_info = read_non_credible_survival_information(single_date)

        # operate on retweet network
        retweet_network = get_retweet_network(df_tweets_all)
        retweet_network_centrality = read_graphs(retweet_network)
        retweet_communities = read_retweet_communities(single_date)
        measure_importance(survival_info, df_tweets_non_credible, retweet_communities, retweet_network_centrality, "retweet", writer)

        # operate on mention network
        mention_network = get_mention_network(df_tweets_all)
        mention_graph_centrality = read_graphs(mention_network)
        mention_communities = read_mention_communities(single_date)
        measure_importance(survival_info, df_tweets_non_credible, mention_communities, mention_graph_centrality, "mention", writer)

        # operate on reply network
        reply_network = get_reply_network(df_tweets_all)
        reply_communities = read_reply_communities(single_date)
        reply_graph_centrality = read_graphs(reply_network)
        measure_importance(survival_info, df_tweets_non_credible, reply_communities, reply_graph_centrality, "reply", writer)

        file.close()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == '__main__':
    main()

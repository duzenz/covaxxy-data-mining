import json
import random
from datetime import date, timedelta

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nx_comm
import pandas as pd

random.seed(5)
REPORTING_FOLDER = "../reporting/"


def get_graph(graph, min_connection_count):
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, min_connection_count)
    return graph


def get_retweets_graph(df, min_connection_count):
    graph_retweets = nx.from_pandas_edgelist(df[df.retweeted_screen_name != '#'], 'username', 'retweeted_screen_name',
                                             ['author_id', 'retweet_author_id', 'retweet_id'],
                                             create_using=nx.DiGraph())
    return get_graph(graph_retweets, min_connection_count)


def get_mentions_graph(df, min_connection_count):
    graph_mentions = nx.from_pandas_edgelist(df[df.user_mentions_screen_name != '#'], 'username',
                                             'user_mentions_screen_name', ['author_id', 'user_mentions_id'],
                                             create_using=nx.DiGraph())
    return get_graph(graph_mentions, min_connection_count)


def get_replies_graph(df, min_connection_count):
    graph_replies = nx.from_pandas_edgelist(df[df.in_reply_to_username != '#'], 'username', 'in_reply_to_username',
                                            ['author_id', 'in_reply_to_tweet_id', 'in_reply_to_user_id'],
                                            create_using=nx.DiGraph())
    return get_graph(graph_replies, min_connection_count)


def get_communities_from_network(graph):
    return nx.girvan_newman(graph)
    #return nx_comm.louvain_communities(graph, seed=123)


def draw_communities_graph(communities, replies_graph):
    node_groups = []
    for com in next(communities):
        node_groups.append(list(com))

    pos = nx.spring_layout(replies_graph, k=0.05)
    plt.figure(figsize=(10, 10))
    nx.draw(replies_graph, pos=pos, cmap=plt.cm.PiYG, edge_color="black", linewidths=0.3, alpha=0.6,
            with_labels=False)

    for group in node_groups:
        nx.draw_networkx_nodes(replies_graph, pos, nodelist=group,
                               node_color=["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])])


def save_communities_graph(graph, day, filename):
    communities = get_communities_from_network(graph)
    save_communities_to_file(communities, filename + day + '.txt')
    # draw_communities_graph(communities, graph)
    # plt.savefig(filename + day + '.png')


def read_csv_report(filepath):
    return pd.read_csv(filepath)


def save_communities_to_file(communities, filename):
    node_groups = []
    for com in communities:
        node_groups.append(list(com))
    node_groups = sorted(node_groups, key=len, reverse=True)
    with open(filename, 'w') as filehandle:
        json.dump(list(node_groups), filehandle)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def run_centrality_calculator(graph):
    graph_centrality = nx.degree_centrality(graph)


def main():
    start_date = date(2021, 3, 16)
    end_date = date(2021, 3, 23)
    for single_date in daterange(start_date, end_date):
        day = single_date.strftime("%Y-%m-%d")
        print("community creation for " + day)
        df = read_csv_report(REPORTING_FOLDER + 'columnar/network-report-' + day + '.csv')
        print("working on replies graph")
        replies_graph = get_replies_graph(df, 3)
        save_communities_graph(replies_graph, day, 'replies-community-')
        # run_centrality_calculator(replies_graph)
        print("working on retweets graph")
        retweets_graph = get_retweets_graph(df, 4)
        save_communities_graph(retweets_graph, day, 'retweets-community-')
        print("working on mentions graph")
        mentions_graph = get_mentions_graph(df, 4)
        save_communities_graph(mentions_graph, day, 'mentions-community-')


if __name__ == '__main__':
    main()

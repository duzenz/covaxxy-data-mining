import pickle
import sys

import numpy as np
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt


def read_csv_report(filepath):
    return pd.read_csv(filepath)


def get_replies_graph(df, min_connection_count):
    graph_replies = nx.from_pandas_edgelist(df[df.in_reply_to_username != '#'], 'username', 'in_reply_to_username',
                                            ['author_id', 'in_reply_to_tweet_id', 'in_reply_to_user_id'],
                                            create_using=nx.DiGraph())
    return get_graph(graph_replies, min_connection_count)


def get_graph(graph, min_connection_count):
    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.k_core(graph, min_connection_count)
    return graph


def get_mentions_graph(df, min_connection_count):
    graph_mentions = nx.from_pandas_edgelist(df[df.user_mentions_screen_name != '#'], 'username',
                                             'user_mentions_screen_name', ['author_id', 'user_mentions_id'],
                                             create_using=nx.DiGraph())
    return get_graph(graph_mentions, min_connection_count)


def get_retweets_graph(df, min_connection_count):
    graph_retweets = nx.from_pandas_edgelist(df[df.retweeted_screen_name != '#'], 'username', 'retweeted_screen_name',
                                             ['author_id', 'retweet_author_id', 'retweet_id'],
                                             create_using=nx.DiGraph())
    return get_graph(graph_retweets, min_connection_count)


def main():
    df = read_csv_report("tweet_ids--2021-02-01.csv")
    # print("working on replies network")
    # replies_graph = get_replies_graph(df, 3)
    # print("replies network created")
    # # save_communities_graph(replies_graph, day, 'replies-community-')
    # # run_centrality_calculator(replies_graph)
    # print("working on retweets network")
    retweets_graph = get_retweets_graph(df, 5)
    print("retweets network created")
    # fig, ax = plt.subplots(figsize=(15, 9))
    # ax.axis("off")
    # plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    # nx.draw_networkx(retweets_graph, pos=nx.random_layout(retweets_graph), ax=ax, **plot_options)
    # plt.show()

    pos = nx.spring_layout(retweets_graph, iterations=15, seed=1721)
    # fig, ax = plt.subplots(figsize=(15, 9))
    # ax.axis("off")
    # plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    # nx.draw_networkx(retweets_graph, pos=pos, ax=ax, **plot_options)
    # plt.show()

    # # save_communities_graph(retweets_graph, daysave_communities_graph, 'retweets-community-')
    # print("working on mentions network")
    # mentions_graph = get_mentions_graph(df, 10)
    # print("mentions network created")

    print(retweets_graph.number_of_nodes())
    print(retweets_graph.number_of_edges())
    print(np.mean([d for _, d in retweets_graph.degree()]))

    shortest_path_lengths = dict(nx.shortest_path_length(retweets_graph))
    diameter = max([max(j.values()) for (i, j) in nx.shortest_path_length(retweets_graph)])

    print(diameter)

    # Compute the average shortest path length for each node
    average_path_lengths = [
        np.mean(list(spl.values())) for spl in shortest_path_lengths.values()
    ]
    # The average over all nodes
    print(np.mean(average_path_lengths))

    # We know the maximum shortest path length (the diameter), so create an array
    # to store values from 0 up to (and including) diameter
    path_lengths = np.zeros(diameter + 1, dtype=int)

    # Extract the frequency of shortest path lengths between two nodes
    for pls in shortest_path_lengths.values():
        pl, cnts = np.unique(list(pls.values()), return_counts=True)
        path_lengths[pl] += cnts

    # Express frequency distribution as a percentage (ignoring path lengths of 0)
    freq_percent = 100 * path_lengths[1:] / path_lengths[1:].sum()

    # Plot the frequency distribution (ignoring path lengths of 0) as a percentage
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(np.arange(1, diameter + 1), height=freq_percent)
    ax.set_title(
        "Distribution of shortest path length in G", fontdict={"size": 35}, loc="center"
    )
    ax.set_xlabel("Shortest Path Length", fontdict={"size": 22})
    ax.set_ylabel("Frequency (%)", fontdict={"size": 22})
    plt.show()

    degree_centrality = nx.centrality.degree_centrality(
        retweets_graph
    )  # save results in a variable to use again
    print((sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True))[:8])
    print((sorted(retweets_graph.degree, key=lambda item: item[1], reverse=True))[:8])

    plt.figure(figsize=(15, 8))
    plt.hist(degree_centrality.values(), bins=100)
    plt.xticks(ticks=[0, 0.025, 0.05, 0.1, 0.15, 0.2])  # set the x axis ticks
    plt.title("Degree Centrality Histogram ", fontdict={"size": 35}, loc="center")
    plt.xlabel("Degree Centrality", fontdict={"size": 20})
    plt.ylabel("Counts", fontdict={"size": 20})
    plt.show()

    node_size = [
        v * 1000 for v in degree_centrality.values()
    ]  # set up nodes size for a nice graph representation
    plt.figure(figsize=(15, 8))
    nx.draw_networkx(retweets_graph, pos=pos, node_size=node_size, with_labels=False, width=0.15)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    main()

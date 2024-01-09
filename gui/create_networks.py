import pickle
import sys
import pandas as pd
import networkx as nx

file_path = sys.argv[1]


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
    df = read_csv_report(file_path)
    print("working on replies network")
    replies_graph = get_replies_graph(df, 3)
    print("replies network created")
    # save_communities_graph(replies_graph, day, 'replies-community-')
    # run_centrality_calculator(replies_graph)
    print("working on retweets network")
    retweets_graph = get_retweets_graph(df, 10)
    print("retweets network created")
    # save_communities_graph(retweets_graph, daysave_communities_graph, 'retweets-community-')
    print("working on mentions network")
    mentions_graph = get_mentions_graph(df, 10)
    print("mentions network created")
    pickle.dump(replies_graph, open('networks/replies_network.pickle', 'wb'))
    pickle.dump(retweets_graph, open('networks/retweets_network.pickle', 'wb'))
    pickle.dump(mentions_graph, open('networks/mentions_network.pickle', 'wb'))
    # save_communities_graph(mentions_graph, day, 'mentions-community-')

    print("All networks are saved the networks folder")


if __name__ == '__main__':
    main()

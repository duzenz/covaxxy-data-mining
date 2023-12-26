import json
import pickle

import networkx as nx


def calculate_reply_network_metrics():
    print("centrality metric calculation started for reply network")
    reply_network = pickle.load(open('networks/replies_network.pickle', 'rb'))

    dictionary = nx.degree_centrality(reply_network)
    with open("centrality/reply_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of degree centrality is finished")

    dictionary = nx.closeness_centrality(reply_network)
    with open("centrality/reply_closeness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of closeness centrality is finished")

    dictionary = nx.betweenness_centrality(reply_network)
    with open("centrality/reply_betweenness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of betweenness centrality is finished")

    dictionary = nx.in_degree_centrality(reply_network)
    with open("centrality/reply_in_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of in degree centrality is finished")

    dictionary = nx.out_degree_centrality(reply_network)
    with open("centrality/reply_out_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of out degree centrality is finished")


def calculate_retweet_network_metrics():
    print("centrality metric calculation started for retweet network")
    retweet_network = pickle.load(open('networks/retweets_network.pickle', 'rb'))

    dictionary = nx.degree_centrality(retweet_network)
    with open("centrality/retweet_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of degree centrality is finished")

    dictionary = nx.closeness_centrality(retweet_network)
    with open("centrality/retweet_closeness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of closeness centrality is finished")

    dictionary = nx.betweenness_centrality(retweet_network)
    with open("centrality/retweet_betweenness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of betweenness centrality is finished")

    dictionary = nx.in_degree_centrality(retweet_network)
    with open("centrality/retweet_in_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of in degree centrality is finished")

    dictionary = nx.out_degree_centrality(retweet_network)
    with open("centrality/retweet_out_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of out degree centrality is finished")


def calculate_mention_network_metrics():
    print("centrality metric calculation started for mention network")
    mention_network = pickle.load(open('networks/mentions_network.pickle', 'rb'))

    dictionary = nx.degree_centrality(mention_network)
    with open("centrality/mention_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of degree centrality is finished")

    dictionary = nx.closeness_centrality(mention_network)
    with open("centrality/mention_closeness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of closeness centrality is finished")

    dictionary = nx.betweenness_centrality(mention_network)
    with open("centrality/mention_betweenness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of betweenness centrality is finished")

    dictionary = nx.in_degree_centrality(mention_network)
    with open("centrality/mention_in_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of in degree centrality is finished")

    dictionary = nx.out_degree_centrality(mention_network)
    with open("centrality/mention_out_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of out degree centrality is finished")


def main():
    calculate_reply_network_metrics()
    calculate_retweet_network_metrics()
    calculate_mention_network_metrics()


if __name__ == '__main__':
    main()

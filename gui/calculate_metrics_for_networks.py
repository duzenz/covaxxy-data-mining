import json
import pickle

import networkx as nx


def calculate_reply_network_metrics():
    print("prestige metric calculation started for reply network")
    reply_network = pickle.load(open('networks/replies_network.pickle', 'rb'))

    dictionary = nx.degree_centrality(reply_network)
    with open("centrality/reply_degree.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of degree centrality is finished")

    dictionary = nx.closeness_centrality(reply_network)
    with open("centrality/reply_closeness.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of closeness centrality is finished")

    # dictionary = nx.betweenness_centrality(reply_network)
    # with open("centrality/reply_betweenness.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of betweenness centrality is finished")

    # dictionary = nx.in_degree_centrality(reply_network)
    # with open("centrality/reply_in_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of in degree centrality is finished")
    #
    # dictionary = nx.out_degree_centrality(reply_network)
    # with open("centrality/reply_out_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of out degree centrality is finished")

    # try:
    #     dictionary = nx.katz_centrality(reply_network)
    #     with open("centrality/reply_katz.json", "w") as outfile:
    #         json.dump(dictionary, outfile)
    #     print("calculation of katz centrality is finished")
    # except:
    #     print("katz centrality could not be calculated")
    #
    # dictionary = nx.load_centrality(reply_network)
    # with open("centrality/reply_load.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of load centrality is finished")
    #
    # dictionary = nx.harmonic_centrality(reply_network)
    # with open("centrality/reply_harmonic.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of harmonic centrality is finished")

    dictionary = nx.pagerank(reply_network)
    with open("centrality/reply_pagerank.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of pagerank is finished")

    hub_score, authority_score = nx.hits(reply_network)
    with open("centrality/reply_hub_score.json", "w") as outfile:
        json.dump(hub_score, outfile)
    with open("centrality/reply_authority_score.json", "w") as outfile:
        json.dump(authority_score, outfile)

    # clustering_coefficient = nx.clustering(reply_network)
    # with open("centrality/reply_clustering_coefficient.json", "w") as outfile:
    #     json.dump(clustering_coefficient, outfile)
    # print("calculation of clustering coefficient is finished")
    #
    # assortativity = nx.degree_assortativity_coefficient(reply_network)
    # with open("centrality/reply_assortativity.json", "w") as outfile:
    #     json.dump(assortativity, outfile)
    # print("calculation of assortativity is finished")

    try:
        dictionary = nx.eigenvector_centrality(reply_network)
        with open("centrality/reply_eigenvector.json", "w") as outfile:
            json.dump(dictionary, outfile)
        print("calculation of eigenvector centrality is finished")
    except:
        print("eigenvector centrality could not be calculated")


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

    # dictionary = nx.betweenness_centrality(retweet_network)
    # with open("centrality/retweet_betweenness.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of betweenness centrality is finished")
    #
    # dictionary = nx.in_degree_centrality(retweet_network)
    # with open("centrality/retweet_in_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of in degree centrality is finished")
    #
    # dictionary = nx.out_degree_centrality(retweet_network)
    # with open("centrality/retweet_out_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of out degree centrality is finished")
    #
    # try:
    #     dictionary = nx.katz_centrality(retweet_network)
    #     with open("centrality/retweet_katz.json", "w") as outfile:
    #         json.dump(dictionary, outfile)
    #     print("calculation of katz centrality is finished")
    # except:
    #     print("katz centrality could not be calculated")
    #
    # dictionary = nx.load_centrality(retweet_network)
    # with open("centrality/retweet_load.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of load centrality is finished")
    #
    # dictionary = nx.harmonic_centrality(retweet_network)
    # with open("centrality/retweet_harmonic.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of harmonic centrality is finished")

    hub_score, authority_score = nx.hits(retweet_network)
    with open("centrality/retweet_hub_score.json", "w") as outfile:
        json.dump(hub_score, outfile)
    with open("centrality/retweet_authority_score.json", "w") as outfile:
        json.dump(authority_score, outfile)

    dictionary = nx.pagerank(retweet_network)
    with open("centrality/retweet_pagerank.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of pagerank is finished")

    # clustering_coefficient = nx.clustering(retweet_network)
    # with open("centrality/retweet_clustering_coefficient.json", "w") as outfile:
    #     json.dump(clustering_coefficient, outfile)
    # print("calculation of clustering coefficient is finished")
    #
    # assortativity = nx.degree_assortativity_coefficient(retweet_network)
    # with open("centrality/retweet_assortativity.json", "w") as outfile:
    #     json.dump(assortativity, outfile)
    # print("calculation of assortativity is finished")

    try:
        dictionary = nx.eigenvector_centrality(retweet_network)
        with open("centrality/retweet_eigenvector.json", "w") as outfile:
            json.dump(dictionary, outfile)
        print("calculation of eigenvector centrality is finished")
    except:
        print("eigenvector centrality could not be calculated")


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

    # dictionary = nx.betweenness_centrality(mention_network)
    # with open("centrality/mention_betweenness.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of betweenness centrality is finished")
    #
    # dictionary = nx.in_degree_centrality(mention_network)
    # with open("centrality/mention_in_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of in degree centrality is finished")
    #
    # dictionary = nx.out_degree_centrality(mention_network)
    # with open("centrality/mention_out_degree.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of out degree centrality is finished")
    #
    # try:
    #     dictionary = nx.katz_centrality(mention_network)
    #     with open("centrality/mention_katz.json", "w") as outfile:
    #         json.dump(dictionary, outfile)
    #     print("calculation of katz centrality is finished")
    # except:
    #
    #     print("katz centrality could not be calculated")
    #
    # dictionary = nx.load_centrality(mention_network)
    # with open("centrality/mention_load.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of load centrality is finished")
    #
    # dictionary = nx.harmonic_centrality(mention_network)
    # with open("centrality/mention_harmonic.json", "w") as outfile:
    #     json.dump(dictionary, outfile)
    # print("calculation of harmonic centrality is finished")

    hub_score, authority_score = nx.hits(mention_network)
    with open("centrality/mention_hub_score.json", "w") as outfile:
        json.dump(hub_score, outfile)
    with open("centrality/mention_authority_score.json", "w") as outfile:
        json.dump(authority_score, outfile)

    dictionary = nx.pagerank(mention_network)
    with open("centrality/mention_pagerank.json", "w") as outfile:
        json.dump(dictionary, outfile)
    print("calculation of pagerank is finished")

    # clustering_coefficient = nx.clustering(mention_network)
    # with open("centrality/mention_clustering_coefficient.json", "w") as outfile:
    #     json.dump(clustering_coefficient, outfile)
    # print("calculation of clustering coefficient is finished")
    #
    # assortativity = nx.degree_assortativity_coefficient(mention_network)
    # with open("centrality/mention_assortativity.json", "w") as outfile:
    #     json.dump(assortativity, outfile)
    # print("calculation of assortativity is finished")

    try:
        dictionary = nx.eigenvector_centrality(mention_network)
        with open("centrality/mention_eigenvector.json", "w") as outfile:
            json.dump(dictionary, outfile)
        print("calculation of eigenvector centrality is finished")
    except:
        print("eigenvector centrality could not be calculated")


def main():
    calculate_reply_network_metrics()
    calculate_retweet_network_metrics()
    calculate_mention_network_metrics()


if __name__ == '__main__':
    main()

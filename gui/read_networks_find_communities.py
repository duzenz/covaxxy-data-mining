import pickle
import sys
import networkx.algorithms.community as nx_comm
import json
import random

import networkx as nx
import matplotlib.pyplot as plt


def save_communities_graph(graph, filename):
    communities = get_communities_from_network(graph)
    save_communities_to_file(communities, filename + '.txt')
    draw_communities_graph(communities, graph)
    plt.savefig(filename + '.png')


def save_communities_to_file(communities, filename):
    node_groups = []
    for com in communities:
        node_groups.append(list(com))
    node_groups = sorted(node_groups, key=len, reverse=True)
    with open(filename, 'w') as filehandle:
        json.dump(list(node_groups), filehandle)


def draw_communities_graph(communities, replies_graph):
    node_groups = []
    for com in communities:
        node_groups.append(list(com))

    pos = nx.spring_layout(replies_graph, k=0.05)
    plt.figure(figsize=(10, 10))
    nx.draw(replies_graph, pos=pos, cmap=plt.cm.PiYG, edge_color="black", linewidths=0.3, alpha=0.6,
            with_labels=False)

    for group in node_groups:
        nx.draw_networkx_nodes(replies_graph, pos, nodelist=group,
                               node_color=["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])])


def get_communities_from_network(graph):
    return nx.girvan_newman(graph)
    #return nx_comm.louvain_communities(graph, seed=123)


def main():
    print("process reply start")
    reply_network = pickle.load(open('networks/replies_network.pickle', 'rb'))
    save_communities_graph(reply_network, "networks/replies_communities")
    print("process reply finish")
    print("process retweet start")
    retweet_network = pickle.load(open('networks/retweets_network.pickle', 'rb'))
    save_communities_graph(retweet_network, "networks/retweets_communities")
    print("process retweet finish")
    print("process mention start")
    mention_network = pickle.load(open('networks/mentions_network.pickle', 'rb'))
    save_communities_graph(mention_network, "networks/mentions_communities")
    print("process mention finish")


if __name__ == '__main__':
    main()

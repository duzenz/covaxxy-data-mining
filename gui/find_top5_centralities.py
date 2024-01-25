import csv
import json
import os

import pandas as pd


# PluginTwter
# CoronaUpdateBot
# YawGyebi
# KwakubaK
# Daniel39618529
def get_centrality_dictionary(type):
    centrality = {}
    with open('centrality/' + type + '_degree.json', 'r') as filehandle:
        centrality["degree"] = json.load(filehandle)
    with open('centrality/' + type + '_betweenness.json', 'r') as filehandle:
        centrality["betweenness"] = json.load(filehandle)
    with open('centrality/' + type + '_closeness.json', 'r') as filehandle:
        centrality["closeness"] = json.load(filehandle)
    with open('centrality/' + type + '_in_degree.json', 'r') as filehandle:
        centrality["in_degree"] = json.load(filehandle)
    with open('centrality/' + type + '_out_degree.json', 'r') as filehandle:
        centrality["out_degree"] = json.load(filehandle)

    with open('centrality/' + type + '_katz.json', 'r') as filehandle:
        centrality["katz"] = json.load(filehandle)

    with open('centrality/' + type + '_load.json', 'r') as filehandle:
        centrality["load"] = json.load(filehandle)

    with open('centrality/' + type + '_harmonic.json', 'r') as filehandle:
        centrality["harmonic"] = json.load(filehandle)

    with open('centrality/' + type + '_pagerank.json', 'r') as filehandle:
        centrality["pagerank"] = json.load(filehandle)

    with open('centrality/' + type + '_clustering_coefficient.json', 'r') as filehandle:
        centrality["clustering_coefficient"] = json.load(filehandle)

    with open('centrality/' + type + '_eigenvector.json', 'r') as filehandle:
        centrality["eigenvector"] = json.load(filehandle)

    return centrality


def main():
    retweet_centrality = get_centrality_dictionary("retweet")
    mention_centrality = get_centrality_dictionary("mention")
    reply_centrality = get_centrality_dictionary("reply")

    f = open('statistics-01.csv', 'w', encoding="utf-8", newline='')
    writer = csv.writer(f)
    header = ['username', 'tweet-count', 'network', 'degree', 'in-degree', 'out-degree',
              'betweenness', 'closeness', 'katz', 'load', 'harmonic', 'pagerank', 'clustering_coefficient', 'eigenvector']
    writer.writerow(header)

    katz_val = retweet_centrality["katz"]["PluginTwter"] if "PluginTwter" in retweet_centrality["katz"] else 0
    writer.writerow(
        ["PluginTwter", 0, "retweet", retweet_centrality["degree"]["PluginTwter"], retweet_centrality["in_degree"]["PluginTwter"],
         retweet_centrality["out_degree"]["PluginTwter"], retweet_centrality["betweenness"]["PluginTwter"],
         retweet_centrality["closeness"]["PluginTwter"], katz_val,
         retweet_centrality["load"]["PluginTwter"], retweet_centrality["harmonic"]["PluginTwter"],
         retweet_centrality["pagerank"]["PluginTwter"], retweet_centrality["clustering_coefficient"]["PluginTwter"],
         retweet_centrality["eigenvector"]["PluginTwter"]])

    katz_val = retweet_centrality["katz"]["CoronaUpdateBot"] if "CoronaUpdateBot" in retweet_centrality["katz"] else 0
    writer.writerow(
        ["CoronaUpdateBot", 0, "retweet", retweet_centrality["degree"]["CoronaUpdateBot"],
         retweet_centrality["in_degree"]["CoronaUpdateBot"],
         retweet_centrality["out_degree"]["CoronaUpdateBot"], retweet_centrality["betweenness"]["CoronaUpdateBot"],
         retweet_centrality["closeness"]["CoronaUpdateBot"], katz_val,
         retweet_centrality["load"]["CoronaUpdateBot"], retweet_centrality["harmonic"]["CoronaUpdateBot"],
         retweet_centrality["pagerank"]["CoronaUpdateBot"], retweet_centrality["clustering_coefficient"]["CoronaUpdateBot"],
         retweet_centrality["eigenvector"]["CoronaUpdateBot"]])

    katz_val = retweet_centrality["katz"]["YawGyebi"] if "YawGyebi" in retweet_centrality["katz"] else 0
    writer.writerow(
        ["YawGyebi", 0, "retweet", retweet_centrality["degree"]["YawGyebi"], retweet_centrality["in_degree"]["YawGyebi"],
         retweet_centrality["out_degree"]["YawGyebi"], retweet_centrality["betweenness"]["YawGyebi"],
         retweet_centrality["closeness"]["YawGyebi"], katz_val,
         retweet_centrality["load"]["YawGyebi"], retweet_centrality["harmonic"]["YawGyebi"],
         retweet_centrality["pagerank"]["YawGyebi"], retweet_centrality["clustering_coefficient"]["YawGyebi"],
         retweet_centrality["eigenvector"]["YawGyebi"]])

    katz_val = retweet_centrality["katz"]["KwakubaK"] if "KwakubaK" in retweet_centrality["katz"] else 0
    writer.writerow(
        ["KwakubaK", 0, "retweet", retweet_centrality["degree"]["KwakubaK"], retweet_centrality["in_degree"]["KwakubaK"],
         retweet_centrality["out_degree"]["KwakubaK"], retweet_centrality["betweenness"]["KwakubaK"],
         retweet_centrality["closeness"]["KwakubaK"], katz_val,
         retweet_centrality["load"]["KwakubaK"], retweet_centrality["harmonic"]["KwakubaK"],
         retweet_centrality["pagerank"]["KwakubaK"], retweet_centrality["clustering_coefficient"]["KwakubaK"],
         retweet_centrality["eigenvector"]["KwakubaK"]])

    katz_val = retweet_centrality["katz"]["Daniel39618529"] if "Daniel39618529" in retweet_centrality["katz"] else 0
    writer.writerow(
        ["Daniel39618529", 0, "retweet", retweet_centrality["degree"]["Daniel39618529"], retweet_centrality["in_degree"]["Daniel39618529"],
         retweet_centrality["out_degree"]["Daniel39618529"], retweet_centrality["betweenness"]["Daniel39618529"],
         retweet_centrality["closeness"]["Daniel39618529"], katz_val,
         retweet_centrality["load"]["Daniel39618529"], retweet_centrality["harmonic"]["Daniel39618529"],
         retweet_centrality["pagerank"]["Daniel39618529"], retweet_centrality["clustering_coefficient"]["Daniel39618529"],
         retweet_centrality["eigenvector"]["Daniel39618529"]])

    katz_val = mention_centrality["katz"]["PluginTwter"] if "PluginTwter" in mention_centrality["katz"] else 0
    writer.writerow(
        ["PluginTwter", 0, "mention", mention_centrality["degree"]["PluginTwter"], mention_centrality["in_degree"]["PluginTwter"],
         mention_centrality["out_degree"]["PluginTwter"], mention_centrality["betweenness"]["PluginTwter"],
         mention_centrality["closeness"]["PluginTwter"], katz_val,
         mention_centrality["load"]["PluginTwter"], mention_centrality["harmonic"]["PluginTwter"],
         mention_centrality["pagerank"]["PluginTwter"], mention_centrality["clustering_coefficient"]["PluginTwter"],
         mention_centrality["eigenvector"]["PluginTwter"]])

    katz_val = mention_centrality["katz"]["CoronaUpdateBot"] if "CoronaUpdateBot" in mention_centrality["katz"] else 0
    writer.writerow(
        ["CoronaUpdateBot", 0, "mention", mention_centrality["degree"]["CoronaUpdateBot"],
         mention_centrality["in_degree"]["CoronaUpdateBot"],
         mention_centrality["out_degree"]["CoronaUpdateBot"], mention_centrality["betweenness"]["CoronaUpdateBot"],
         mention_centrality["closeness"]["CoronaUpdateBot"], katz_val,
         mention_centrality["load"]["CoronaUpdateBot"], mention_centrality["harmonic"]["CoronaUpdateBot"],
         mention_centrality["pagerank"]["CoronaUpdateBot"], mention_centrality["clustering_coefficient"]["CoronaUpdateBot"],
         mention_centrality["eigenvector"]["CoronaUpdateBot"]])

    katz_val = mention_centrality["katz"]["YawGyebi"] if "YawGyebi" in mention_centrality["katz"] else 0
    writer.writerow(
        ["YawGyebi", 0, "mention", mention_centrality["degree"]["YawGyebi"], mention_centrality["in_degree"]["YawGyebi"],
         mention_centrality["out_degree"]["YawGyebi"], mention_centrality["betweenness"]["YawGyebi"],
         mention_centrality["closeness"]["YawGyebi"], katz_val,
         mention_centrality["load"]["YawGyebi"], mention_centrality["harmonic"]["YawGyebi"],
         mention_centrality["pagerank"]["YawGyebi"], mention_centrality["clustering_coefficient"]["YawGyebi"],
         mention_centrality["eigenvector"]["YawGyebi"]])

    katz_val = mention_centrality["katz"]["KwakubaK"] if "KwakubaK" in mention_centrality["katz"] else 0
    writer.writerow(
        ["KwakubaK", 0, "mention", mention_centrality["degree"]["KwakubaK"], mention_centrality["in_degree"]["KwakubaK"],
         mention_centrality["out_degree"]["KwakubaK"], mention_centrality["betweenness"]["KwakubaK"],
         mention_centrality["closeness"]["KwakubaK"], katz_val,
         mention_centrality["load"]["KwakubaK"], mention_centrality["harmonic"]["KwakubaK"],
         mention_centrality["pagerank"]["KwakubaK"], mention_centrality["clustering_coefficient"]["KwakubaK"],
         mention_centrality["eigenvector"]["KwakubaK"]])

    katz_val = mention_centrality["katz"]["Daniel39618529"] if "Daniel39618529" in mention_centrality["katz"] else 0
    writer.writerow(
        ["Daniel39618529", 0, "mention", mention_centrality["degree"]["Daniel39618529"], mention_centrality["in_degree"]["Daniel39618529"],
         mention_centrality["out_degree"]["Daniel39618529"], mention_centrality["betweenness"]["Daniel39618529"],
         mention_centrality["closeness"]["Daniel39618529"], katz_val,
         mention_centrality["load"]["Daniel39618529"], mention_centrality["harmonic"]["Daniel39618529"],
         mention_centrality["pagerank"]["Daniel39618529"], mention_centrality["clustering_coefficient"]["Daniel39618529"],
         mention_centrality["eigenvector"]["Daniel39618529"]])
    #
    # katz_val = reply_centrality["katz"]["PluginTwter"] if "PluginTwter" in reply_centrality["katz"] else 0
    # writer.writerow(
    #     ["PluginTwter", 0, "reply", reply_centrality["degree"]["PluginTwter"], reply_centrality["in_degree"]["PluginTwter"],
    #      reply_centrality["out_degree"]["PluginTwter"], reply_centrality["betweenness"]["PluginTwter"],
    #      reply_centrality["closeness"]["PluginTwter"], katz_val,
    #      reply_centrality["load"]["PluginTwter"], reply_centrality["harmonic"]["PluginTwter"],
    #      reply_centrality["pagerank"]["PluginTwter"], reply_centrality["clustering_coefficient"]["PluginTwter"],
    #      reply_centrality["eigenvector"]["PluginTwter"]])
    #
    # katz_val = reply_centrality["katz"]["CoronaUpdateBot"] if "CoronaUpdateBot" in reply_centrality["katz"] else 0
    # writer.writerow(
    #     ["CoronaUpdateBot", 0, "reply", reply_centrality["degree"]["CoronaUpdateBot"], reply_centrality["in_degree"]["CoronaUpdateBot"],
    #      reply_centrality["out_degree"]["CoronaUpdateBot"], reply_centrality["betweenness"]["CoronaUpdateBot"],
    #      reply_centrality["closeness"]["CoronaUpdateBot"], katz_val,
    #      reply_centrality["load"]["CoronaUpdateBot"], reply_centrality["harmonic"]["CoronaUpdateBot"],
    #      reply_centrality["pagerank"]["CoronaUpdateBot"], reply_centrality["clustering_coefficient"]["CoronaUpdateBot"],
    #      reply_centrality["eigenvector"]["CoronaUpdateBot"]])
    #
    # katz_val = reply_centrality["katz"]["YawGyebi"] if "YawGyebi" in reply_centrality["katz"] else 0
    # writer.writerow(
    #     ["YawGyebi", 0, "reply", reply_centrality["degree"]["YawGyebi"], reply_centrality["in_degree"]["YawGyebi"],
    #      reply_centrality["out_degree"]["YawGyebi"], reply_centrality["betweenness"]["YawGyebi"],
    #      reply_centrality["closeness"]["YawGyebi"], katz_val,
    #      reply_centrality["load"]["YawGyebi"], reply_centrality["harmonic"]["YawGyebi"],
    #      reply_centrality["pagerank"]["YawGyebi"], reply_centrality["clustering_coefficient"]["YawGyebi"],
    #      reply_centrality["eigenvector"]["YawGyebi"]])
    #
    # katz_val = reply_centrality["katz"]["KwakubaK"] if "KwakubaK" in reply_centrality["katz"] else 0
    # writer.writerow(
    #     ["KwakubaK", 0, "reply", reply_centrality["degree"]["KwakubaK"], reply_centrality["in_degree"]["KwakubaK"],
    #      reply_centrality["out_degree"]["KwakubaK"], reply_centrality["betweenness"]["KwakubaK"],
    #      reply_centrality["closeness"]["KwakubaK"], katz_val,
    #      reply_centrality["load"]["KwakubaK"], reply_centrality["harmonic"]["KwakubaK"],
    #      reply_centrality["pagerank"]["KwakubaK"], reply_centrality["clustering_coefficient"]["KwakubaK"],
    #      reply_centrality["eigenvector"]["KwakubaK"]])
    #
    # katz_val = reply_centrality["katz"]["Daniel39618529"] if "Daniel39618529" in reply_centrality["katz"] else 0
    # writer.writerow(
    #     ["Daniel39618529", 0, "reply", reply_centrality["degree"]["Daniel39618529"], reply_centrality["in_degree"]["Daniel39618529"],
    #      reply_centrality["out_degree"]["Daniel39618529"], reply_centrality["betweenness"]["Daniel39618529"],
    #      reply_centrality["closeness"]["Daniel39618529"], katz_val,
    #      reply_centrality["load"]["Daniel39618529"], reply_centrality["harmonic"]["Daniel39618529"],
    #      reply_centrality["pagerank"]["Daniel39618529"], reply_centrality["clustering_coefficient"]["Daniel39618529"],
    #      reply_centrality["eigenvector"]["Daniel39618529"]])

    f.close()


if __name__ == '__main__':
    main()

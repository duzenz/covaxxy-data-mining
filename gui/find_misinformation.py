import csv
import json
import sys

import pandas as pd

file_path = sys.argv[1]


def read_csv_report(filepath):
    return pd.read_csv(filepath)


def get_bot_users_list(df_tweets):
    df_non_credible_ids = df_tweets.loc[df_tweets['credible'] == 0].copy()
    # read bot users for that day
    tweet_id_list = df_non_credible_ids['tweet_id'].tolist()

    bot_users = []
    for tweet_id in tweet_id_list:
        try:
            row = df_tweets.loc[df_tweets['tweet_id'] == tweet_id]
            bot_users.append(row['username'].item())
        except:
            pass
    return list(dict.fromkeys(bot_users))


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


def get_communities():
    communities = {}
    with open('networks/retweets_communities.txt', 'r') as filehandle:
        communities["retweet"] = json.load(filehandle)
    with open('networks/mentions_communities.txt', 'r') as filehandle:
        communities["mention"] = json.load(filehandle)
    with open('networks/replies_communities.txt', 'r') as filehandle:
        communities["reply"] = json.load(filehandle)

    return communities


def create_retweet_report(bot_users, communities, centrality, writer):
    for community in communities:
        create_report("retweet", "degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "closeness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "betweenness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "in_degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "out_degree", community, centrality, bot_users, writer)

    try:
        for community in communities:
            create_report("retweet", "katz", community, centrality, bot_users, writer)
    except:
        print("katz centrality could not be calculated")
    for community in communities:
        create_report("retweet", "load", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "harmonic", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "pagerank", community, centrality, bot_users, writer)
    for community in communities:
        create_report("retweet", "clustering_coefficient", community, centrality, bot_users, writer)
    try:
        for community in communities:
            create_report("retweet", "eigenvector", community, centrality, bot_users, writer)
    except:
        print("eigenvector centrality could not be calculated")


def create_mention_report(bot_users, communities, centrality, writer):
    for community in communities:
        create_report("mention", "degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "closeness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "betweenness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "in_degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "out_degree", community, centrality, bot_users, writer)
    try:
        for community in communities:
            create_report("mention", "katz", community, centrality, bot_users, writer)
    except:
        print("katz centrality could not be calculated")
    for community in communities:
        create_report("mention", "load", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "harmonic", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "pagerank", community, centrality, bot_users, writer)
    for community in communities:
        create_report("mention", "clustering_coefficient", community, centrality, bot_users, writer)
    try:
        for community in communities:
            create_report("mention", "eigenvector", community, centrality, bot_users, writer)
    except:
        print("eigenvector centrality could not be calculated")


def create_reply_report(bot_users, communities, centrality, writer):
    for community in communities:
        create_report("reply", "degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "closeness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "betweenness", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "in_degree", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "out_degree", community, centrality, bot_users, writer)
    try:
        for community in communities:
            create_report("reply", "katz", community, centrality, bot_users, writer)
    except:
        print("katz centrality could not be calculated")
    for community in communities:
        create_report("reply", "load", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "harmonic", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "pagerank", community, centrality, bot_users, writer)
    for community in communities:
        create_report("reply", "clustering_coefficient", community, centrality, bot_users, writer)
    try:
        for community in communities:
            create_report("reply", "eigenvector", community, centrality, bot_users, writer)
    except:
        print("eigenvector centrality could not be calculated")


def create_report(network_type, centrality_type, community, centrality, bot_users, writer):
    community_unique = list(dict.fromkeys(community))
    dict_you_want = {your_key: centrality[centrality_type][your_key] for your_key in community_unique}
    sorted_community = dict(sorted(dict_you_want.items(), key=lambda item: item[1], reverse=True))

    keys = list(sorted_community.keys())
    min_index = len(keys)
    total_bot_count = 0
    for user in bot_users:
        try:
            found_index = keys.index(user)
            total_bot_count += 1
            if found_index < min_index:
                min_index = found_index
        except:
            pass
    if min_index == len(keys):
        min_index = -1
    algorithm_value = sorted_community[keys[min_index]] if min_index != -1 else "#"
    index_value = str(min_index + 1) if min_index != -1 else "#"
    index_user = keys[min_index] if min_index != -1 else "#"
    average_value = sum(sorted_community.values()) / len(sorted_community)
    writer.writerow(
        [network_type, centrality_type, str(len(sorted_community)), index_value, index_user, str(total_bot_count), algorithm_value,
         average_value])


def main():
    print("Misinformation module is started")
    file = open('report/' + file_path.split('/')[-1].split('.')[0].split("--")[1] + '-misinformation-report.csv', 'w', encoding="utf-8",
                newline='')
    writer = csv.writer(file)
    header = ["Network Type", "Centrality Type", "Community Size", "First Misinformation Index", "First Uncredible Username",
              "Uncredible User Count in Community",
              "Centrality Algorithm Value", "Average Value in Community"]

    writer.writerow(header)
    df_tweets = read_csv_report(file_path)
    bot_users = get_bot_users_list(df_tweets)
    communities = get_communities()

    retweet_centrality = get_centrality_dictionary("retweet")
    mention_centrality = get_centrality_dictionary("mention")
    reply_centrality = get_centrality_dictionary("reply")

    create_retweet_report(bot_users, communities["retweet"], retweet_centrality, writer)
    print("Retweet network misinformation report is finished")
    create_mention_report(bot_users, communities["mention"], mention_centrality, writer)
    print("Mention network misinformation report is finished")
    create_reply_report(bot_users, communities['reply'], reply_centrality, writer)
    print("Reply network misinformation report is finished")
    file.close()
    print("Misinformation module is finished")


if __name__ == '__main__':
    main()

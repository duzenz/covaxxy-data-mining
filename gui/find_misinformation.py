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

def create_report(network_type, centrality_type, community, centrality, bot_users, writer):
    community_unique = list(dict.fromkeys(community))
    dict_you_want = {your_key: centrality[centrality_type][your_key] for your_key in community_unique}
    sorted_community = dict(sorted(dict_you_want.items(), key=lambda item: item[1], reverse=True))

    index_array = []
    keys = list(sorted_community.keys())
    for user in bot_users:
        if user in keys:
            index_array.append(keys.index(user) + 1)

    orders = '_'.join(str(e) for e in index_array)
    if orders == '':
        orders = '-'
    writer.writerow([network_type, centrality_type, str(len(sorted_community)), orders])


def main():
    print("Misinformation module is started")
    file = open('report/importance-report.csv', 'w', encoding="utf-8", newline='')
    writer = csv.writer(file)
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

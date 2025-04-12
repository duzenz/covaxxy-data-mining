import json
import operator

import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta


def operate_reactions(single_date, reactions_dict, day_count):
    pd.set_option('display.max_columns', None)

    # non-credible tweet id list
    reference_id_list = reactions_dict[str(single_date)]['reference_id'].tolist()

    report = {}
    for reference_id in reference_id_list:
        for day in reactions_dict.keys():
            if day == str(single_date):
                continue  # skip controlling day
            reference_row = get_referenced_row(reactions_dict[day], reference_id)
            if not reference_row.empty:
                if reference_id not in report:
                    report[reference_id] = {}
                report[reference_id][day] = {"reference_type": reference_row["reference_type"].values[0],
                                             "reaction_count": int(reference_row["quote_count"].values[0]) +
                                                               int(reference_row["reply_count"].values[0]) +
                                                               int(reference_row["retweet_count"].values[0]) +
                                                               int(reference_row["like_count"].values[0])}

    with open(str(single_date) + '-survive-' + str(day_count) + '.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    draw_report_graph(report, single_date, len(reference_id_list), day_count)


def draw_report_graph(report, single_day, non_credible_count, day_count):
    recurrence = []
    recurrence_dict = {}
    for key in report.keys():
        recurrence.append(len(report[key]))
        recurrence_dict[key] = len(report[key])

    sorted_recurrence_dict = dict(sorted(recurrence_dict.items(), key=operator.itemgetter(1), reverse=True))
    with open(str(single_day) + "-recurrence.json", 'w') as filehandle:
        json.dump(sorted_recurrence_dict, filehandle)
    count = pd.Series(recurrence).value_counts()
    p = count.sort_index().plot.bar(xlabel="Days", ylabel="Reacted Tweet Count")
    p.bar_label(p.containers[0])
    plt.title("")
    plt.savefig(str(single_day) + '-' + str(day_count) + '-survive.png')
    plt.show()
    plt.close()
    print("operations for " + str(single_day) + " finished")


def get_referenced_row(dataset, reference_id):
    return dataset.loc[dataset["reference_id"] == reference_id]


def read_reactions(date_to_operate, only_non_credible=False):
    df_tweets = pd.read_csv("../reporting/columnar/reactions-report-" + date_to_operate + ".csv",
                            dtype={'tweet_id': str, 'reference_id': str})
    if only_non_credible:
        df_tweets = df_tweets.loc[df_tweets['credible'] == 0].copy()

    df_tweets = df_tweets.drop_duplicates(subset=['reference_id'])
    df_tweets = df_tweets.dropna()
    return df_tweets[df_tweets['reference_id'] != '#']


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def read_reports_into_array(single_date, spread_day_count):
    reactions = {str(single_date): read_reactions(str(single_date), True)}
    for i in range(1, spread_day_count):
        reactions[str(single_date + timedelta(i))] = read_reactions(str(single_date + timedelta(i)))
    return reactions


def main():
    day_count = 20
    start_date = date(2021, 3, 1)
    end_date = date(2021, 3, 2)
    for single_date in daterange(start_date, end_date):
        print("operations for " + str(single_date) + " started")
        reactions_dict = read_reports_into_array(single_date, day_count)
        operate_reactions(single_date, reactions_dict, day_count)


if __name__ == '__main__':
    main()

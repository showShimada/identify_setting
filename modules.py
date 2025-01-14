import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# from matplotlib import rcParams
from scipy.stats import binom
from math import comb

def create_pie_graph_only_bonuses(BB_count,RB_count,START_count,df_probabilities):
    plt.figure(figsize=(8,6))
    probabilities = [(comb(START_count, BB_count) * comb(START_count - BB_count, RB_count) *
            (row.BB ** BB_count) * (row.RB ** RB_count) *
            (row.ハズレ ** (START_count - BB_count - RB_count))) 
            for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    return plt

def create_binom_graph(target, target_count, START_count, df_probabilities):
    range_count = range(max(0,target_count - 5),min(START_count,target_count + 5) + 1)
    max_probability = 0

    plt.figure(figsize=(8,6))
    for i,p in enumerate(df_probabilities[target].tolist()):
        probabilities = [binom.pmf(count,START_count,p) for count in range_count]
        plt.plot(range_count, probabilities, label=f'設定：{i + 1}')
        probabilities.append(max_probability)
        max_probability = max(probabilities)

    bar_values = [max_probability if count == target_count else 0 for count in range_count]

    plt.bar(range_count, bar_values, color="blue", alpha=0.5, label="今回")

    plt.title(target + "の二項分布")
    plt.xlabel(target + "回数")
    plt.ylabel("確率")
    plt.xticks(range_count)
    plt.legend()
    plt.grid()
    plt.tight_layout()

    return plt

def get_outcome(START_count,target_count):
    try:
        outcome = round(START_count/target_count,1)
    except ZeroDivisionError:
        outcome = np.nan

    return outcome
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import binom
from math import floor, ceil

def create_pie_graph_only_bonuses(BB_count,RB_count,game_count,df_flag_counts):
    df_probabilities = pd.DataFrame({
        "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB":[row.RB_flag_counts/(row.amount_flag_counts - row.BB_flag_counts) for row in df_flag_counts.itertuples(index=False, name="setting")]    })
    plt.figure(figsize=(8,6))
    probabilities = [
        binom.pmf(BB_count,game_count,row.BB)
        * binom.pmf(RB_count,game_count - BB_count,row.RB)
        for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    return plt

def create_pie_graph_include_grapes(BB_count,RB_count,grapes_count,game_count,df_flag_counts):
    df_probabilities = pd.DataFrame({
        "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB":[row.RB_flag_counts/(row.amount_flag_counts - row.BB_flag_counts) for row in df_flag_counts.itertuples(index=False, name="setting")],
        "grapes":[row.grapes_flag_counts/(row.amount_flag_counts - row.BB_flag_counts - row.RB_flag_counts) for row in df_flag_counts.itertuples(index=False, name="setting")]
    })
    plt.figure(figsize=(8,6))
    probabilities = [
        binom.pmf(BB_count,game_count,row.BB)
        * binom.pmf(RB_count,game_count - BB_count,row.RB)
        * binom.pmf(grapes_count,game_count - BB_count - RB_count,row.grapes)
        for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    return plt

def create_pie_graph_detail_happy_v3(dict_inputs,game_count,cherry_sum,df_flag_counts):
    df_probabilities = pd.DataFrame({
        "BB_single":[(row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts))
                / (row.amount_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "BB_cherry":[(row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts))
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts)))
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB_single":[row.RB_single_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts))
                    - (row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts)))
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB_cherry":[row.RB_cherry_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts))
                    - (row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts))
                    - row.RB_single_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "grapes":[row.grapes_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts))
                    - (row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts))
                    - row.RB_single_flag_counts
                    - row.RB_cherry_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "cherry":[row.single_cherry_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_cherry_flag_counts))
                    - (row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts))
                    - row.RB_single_flag_counts
                    - row.RB_cherry_flag_counts
                    - row.grapes_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "cherry_with_bonus":[((row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts)) + row.RB_cherry_flag_counts)
                / ((row.BB_cherry_flag_counts + ceil(row.BB_cherry_flag_counts))
                    + row.RB_cherry_flag_counts
                    + row.single_cherry_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
    })
    plt.figure(figsize=(8,6))
    probabilities = [
        binom.pmf(dict_inputs["BB_single_count"],game_count,row.BB_single)
        * binom.pmf(dict_inputs["BB_cherry_count"],game_count - dict_inputs["BB_single_count"],row.BB_cherry)
        * binom.pmf(dict_inputs["RB_single_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"],row.RB_single)
        * binom.pmf(dict_inputs["RB_cherry_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"],row.RB_cherry)
        * binom.pmf(dict_inputs["grapes_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"] - dict_inputs["RB_cherry_count"],row.grapes)
        * binom.pmf(dict_inputs["cherry_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"] - dict_inputs["RB_cherry_count"] - dict_inputs["grapes_count"],row.cherry)
        * binom.pmf(dict_inputs["BB_cherry_count"] + dict_inputs["RB_cherry_count"],cherry_sum, row.cherry_with_bonus)
        for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    return plt

def create_pie_graph_detail_my_juggler(dict_inputs,game_count,df_flag_counts):
    df_probabilities = pd.DataFrame({
        "BB_single":[(row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                / (row.amount_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "BB_cherry":[(row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2)))
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB_single":[row.RB_single_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2)))
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "RB_cherry":[row.RB_cherry_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - row.RB_single_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "grapes":[row.grapes_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - row.RB_single_flag_counts
                    - row.RB_cherry_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
        "cherry":[row.single_cherry_flag_counts
                / (row.amount_flag_counts
                    - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    - row.RB_single_flag_counts
                    - row.RB_cherry_flag_counts
                    - row.grapes_flag_counts)
                for row in df_flag_counts.itertuples(index=False, name="setting")],
    })
    plt.figure(figsize=(8,6))
    probabilities = [
        binom.pmf(dict_inputs["BB_single_count"],game_count,row.BB_single)
        * binom.pmf(dict_inputs["BB_cherry_count"],game_count - dict_inputs["BB_single_count"],row.BB_cherry)
        * binom.pmf(dict_inputs["RB_single_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"],row.RB_single)
        * binom.pmf(dict_inputs["RB_cherry_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"],row.RB_cherry)
        * binom.pmf(dict_inputs["grapes_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"] - dict_inputs["RB_cherry_count"],row.grapes)
        * binom.pmf(dict_inputs["cherry_count"],game_count - dict_inputs["BB_single_count"] - dict_inputs["BB_cherry_count"] - dict_inputs["RB_single_count"] - dict_inputs["RB_cherry_count"] - dict_inputs["grapes_count"],row.cherry)
        for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    return plt

def create_binom_graph(target, target_count, game_count, df_probabilities, additional_range):
    range_count = range(max(0,target_count - additional_range),min(game_count,target_count + additional_range) + 1)
    max_probability = 0

    plt.figure(figsize=(8,6))
    for i,p in enumerate(df_probabilities[target].tolist()):
        probabilities = [binom.pmf(count,game_count,p) for count in range_count]
        plt.plot(range_count, probabilities, label=f'設定：{i + 1}')
        probabilities.append(max_probability)
        max_probability = max(probabilities)

    bar_values = [max_probability if count == target_count else 0 for count in range_count]
    plt.bar(range_count, bar_values, color="blue", alpha=0.5, label="今回")

    if target_count >= 100:
        plt.xticks(range_count,rotation=90)
    else:
        plt.xticks(range_count)

    plt.title(target + "の二項分布")
    plt.xlabel(target + "回数")
    plt.ylabel("確率")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    return plt

def get_outcome(game_count,target_count):
    try:
        outcome = round(game_count/target_count,1)
    except ZeroDivisionError:
        outcome = np.nan

    return outcome
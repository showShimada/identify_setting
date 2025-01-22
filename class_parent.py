import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import binom
# from math import floor, ceil

class parent:
    def __init__(self):
        self.df_flag_counts = pd.DataFrame()
        self.dict_inputs = {}

    def display_input_area_only_bonuses(self):
        st.header("入力欄")
        self.dict_inputs = {
            "BB_count":st.number_input("BB回数",0),
            "RB_count":st.number_input("RB回数",0),
            "START_count":st.number_input("開始ゲーム数",0),
            "END_count":st.number_input("現在ゲーム数",3000)
        }
        self.game_count = self.dict_inputs["END_count"] - self.dict_inputs["START_count"]

    def content_only_bonuses(self):
        self.display_input_area_only_bonuses()

        # 判別パート
        if st.button("実行"):
            st.header("総合判定")
            df_outcome = pd.DataFrame({
                "ゲーム数":self.game_count,
                "BB確率":self.get_outcome("BB_count"),
                "RB確率":self.get_outcome("RB_count")
            },index=["結果"])
            st.dataframe(df_outcome)

            plt = self.create_pie_graph_only_bonuses()
            st.pyplot(plt)

            st.header("BBの二項分布")
            plt = self.create_binom_graph("BB", self.dict_inputs["BB_count"], 5)
            st.pyplot(plt)

            st.header("RBの二項分布")
            plt = self.create_binom_graph("RB", self.dict_inputs["RB_count"], 5)
            st.pyplot(plt)

    def display_input_area_bonuses_and_grapes(self):
        st.header("入力欄")
        self.dict_inputs = {
            "BB_count":st.number_input("BB回数",0),
            "RB_count":st.number_input("RB回数",0),
            "grapes_count":st.number_input("ブドウ",0),
            "START_count":st.number_input("開始ゲーム数",0),
            "END_count":st.number_input("現在ゲーム数",3000)
        }
        self.game_count = self.dict_inputs["END_count"] - self.dict_inputs["START_count"]

    def create_content_bonuses_and_grapes(self):
        self.display_input_area_bonuses_and_grapes()
        # 判別パート
        if st.button("実行"):
            st.header("総合判定")
            df_outcome = pd.DataFrame({
                "ゲーム数":self.game_count,
                "BB確率":self.get_outcome("BB_count"),
                "RB確率":self.get_outcome("RB_count"),
                "ブドウ":self.get_outcome("grapes_count")
            },index=["結果"])
            st.dataframe(df_outcome)

            plt = self.create_pie_graph_include_grapes()
            st.pyplot(plt)

            st.header("BBの二項分布")
            plt = self.create_binom_graph("BB", self.dict_inputs["BB_count"], 5)
            st.pyplot(plt)

            st.header("RBの二項分布")
            plt = self.create_binom_graph("RB", self.dict_inputs["RB_count"], 5)
            st.pyplot(plt)

            st.header("ブドウの二項分布")
            plt = self.create_binom_graph("ブドウ", self.dict_inputs["grapes_count"], 20)
            st.pyplot(plt)

    def create_pie_graph_only_bonuses(self):
        df_probabilities_pie = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/(row.amount_flag_counts - row.BB_flag_counts) for row in self.df_flag_counts.itertuples(index=False, name="setting")]})
        plt.figure(figsize=(8,6))
        probabilities = [
            binom.pmf(self.dict_inputs["BB_count"],self.game_count,row.BB)
            * binom.pmf(self.dict_inputs["RB_count"],self.game_count - self.dict_inputs["BB_count"],row.RB)
            for row in df_probabilities_pie.itertuples(index=False, name="setting")]
        labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
        plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

        plt.title("総合判定")
        return plt

    def create_pie_graph_include_grapes(self):
        self.df_probabilities_pie = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/(row.amount_flag_counts - row.BB_flag_counts) for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "grapes":[row.grapes_flag_counts/(row.amount_flag_counts - row.BB_flag_counts - row.RB_flag_counts) for row in self.df_flag_counts.itertuples(index=False, name="setting")]
        })
        plt.figure(figsize=(8,6))
        probabilities = [
            binom.pmf(self.dict_inputs["BB_count"],self.game_count,row.BB)
            * binom.pmf(self.dict_inputs["RB_count"],self.game_count - self.dict_inputs["BB_count"],row.RB)
            * binom.pmf(self.dict_inputs["grapes_count"],self.game_count - self.dict_inputs["BB_count"] - self.dict_inputs["RB_count"],row.grapes)
            for row in self.df_probabilities_pie.itertuples(index=False, name="setting")]
        labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
        plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

        plt.title("総合判定")
        return plt

    def create_binom_graph(self, target, target_count, additional_range):
        range_count = range(max(0,target_count - additional_range),min(self.game_count,target_count + additional_range) + 1)
        max_probability = 0

        plt.figure(figsize=(8,6))
        for i,p in enumerate(self.df_probabilities[target].tolist()):
            probabilities = [binom.pmf(count,self.game_count,p) for count in range_count]
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

    def get_outcome(self,target):
        try:
            outcome = round(self.game_count/self.dict_inputs[target],1)
        except ZeroDivisionError:
            outcome = np.nan
        return outcome
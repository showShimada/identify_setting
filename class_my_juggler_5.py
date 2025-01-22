import streamlit as st
import pandas as pd
from class_parent import parent
from math import floor, ceil
from matplotlib import pyplot as plt
from scipy.stats import binom

class my_juggler_5(parent):
    def __init__(self):
        self.df_flag_counts = pd.DataFrame({
            "BB_flag_counts":[240,242,246,258,273,286],
            "RB_flag_counts":[160,170,195,226,244,286],
            "grapes_flag_counts":[11110,11200,11300,11340,11380,11580],
            "single_cherry_flag_counts":[1720,1720,1780,1840,1840,1840],
            "BB_single_flag_counts":[160,161,164,173,185,194],
            "BB_cherry_flag_counts":[46,47,48,51,54,58],
            "BB_rareA_flag_counts":[9,9,9,9,9,9],
            "BB_rareB_flag_counts":[9,9,9,9,9,9],
            "BB_rareP_flag_counts":[4,4,4,4,4,4],
            "BB_rareAP_flag_counts":[4,4,4,4,4,4],
            "BB_rareBP_flag_counts":[6,6,6,6,6,6],
            "BB_rareABP_flag_counts":[2,2,2,2,2,2],
            "RB_single_flag_counts":[100,109,133,161,168,200],
            "RB_cherry_flag_counts":[60,61,62,65,76,86],
            "amount_flag_counts":[65536,65536,65536,65536,65536,65536]
        })

        self.df_probabilities = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BBバラケ目":[(row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BBチェリー重複":[(row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB単独":[row.RB_single_flag_counts/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RBチェリー重複":[row.RB_cherry_flag_counts/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.grapes_flag_counts/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "ペカらないチェリー":[row.single_cherry_flag_counts/row.amount_flag_counts
                        for row in self.df_flag_counts.itertuples(index=False, name="setting")]
        })


        self.display_probabilities()

    def display_probabilities(self):
        df_probabilities_for_display = pd.DataFrame({
            "設定":["1","2","3","4","5","6"],
            "BB_合成":[row.amount_flag_counts/row.BB_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_合成":[row.amount_flag_counts/row.RB_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_単独":[row.amount_flag_counts/row.BB_single_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_チェリー重複":[row.amount_flag_counts/row.BB_cherry_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアA":[row.amount_flag_counts/row.BB_rareA_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアB":[row.amount_flag_counts/row.BB_rareB_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアP":[row.amount_flag_counts/row.BB_rareP_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアAP":[row.amount_flag_counts/row.BB_rareAP_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアBP":[row.amount_flag_counts/row.BB_rareBP_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_レアABP":[row.amount_flag_counts/row.BB_rareABP_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_単独":[row.amount_flag_counts/row.RB_single_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_チェリー重複":[row.amount_flag_counts/row.RB_cherry_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.amount_flag_counts/row.grapes_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "単独チェリー":[row.amount_flag_counts/row.single_cherry_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")]
        })
        df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
        st.dataframe(df_probabilities_for_display)

    def create_content_detail(self):
        self.display_input_area_detail()

        # 判別パート
        if st.button("実行"):
            st.header("総合判定")
            df_outcome = pd.DataFrame({
                "ゲーム数":self.game_count,
                "BB合成":self.get_outcome(self.dict_inputs["BB_single_count"] + self.dict_inputs["BB_cherry_count"]),
                "RB合成":self.get_outcome(self.dict_inputs["RB_single_count"] + self.dict_inputs["RB_cherry_count"]),
                "BBバラケ目":self.get_outcome(self.dict_inputs["BB_single_count"]),
                "BBチェリー重複":self.get_outcome(self.dict_inputs["BB_cherry_count"]),
                "RB単独":self.get_outcome(self.dict_inputs["RB_single_count"]),
                "RBチェリー重複":self.get_outcome(self.dict_inputs["RB_cherry_count"]),
                "ブドウ":self.get_outcome(self.dict_inputs["grapes_count"]),
                "ペカらないチェリー":self.get_outcome(self.dict_inputs["cherry_count"])
            },index=["結果"])
            st.dataframe(df_outcome)

            plt = self.create_pie_graph_detail()
            st.pyplot(plt)

            st.header("BBバラケ目の二項分布")
            plt = self.create_binom_graph("BBバラケ目", self.dict_inputs["BB_single_count"], self.game_count,5)
            st.pyplot(plt)

            st.header("BBチェリー重複の二項分布")
            plt = self.create_binom_graph("BBチェリー重複", self.dict_inputs["BB_cherry_count"], self.game_count,5)
            st.pyplot(plt)

            st.header("RB単独の二項分布")
            plt = self.create_binom_graph("RB単独", self.dict_inputs["RB_single_count"], self.game_count,5)
            st.pyplot(plt)

            st.header("RBチェリー重複の二項分布")
            plt = self.create_binom_graph("RBチェリー重複", self.dict_inputs["RB_cherry_count"], self.game_count,5)
            st.pyplot(plt)

            st.header("ブドウの二項分布")
            plt = self.create_binom_graph("ブドウ", self.dict_inputs["grapes_count"], self.game_count,20)
            st.pyplot(plt)

            st.header("ペカらないチェリーの二項分布")
            plt = self.create_binom_graph("ペカらないチェリー", self.dict_inputs["cherry_count"], self.game_count,5)
            st.pyplot(plt)

    def display_input_area_detail(self):
        st.header("入力欄")
        self.dict_inputs ={
            "BB_single_count":st.number_input("BBバラケ目回数",0)
            ,"BB_cherry_count":st.number_input("BBチェリー重複回数",0)
            ,"RB_single_count":st.number_input("RB単独回数",0)
            ,"RB_cherry_count":st.number_input("RBチェリー重複回数",0)
            ,"grapes_count":st.number_input("ブドウ",0)
            ,"cherry_count":st.number_input("ペカらないチェリー",0)
            ,"START_count":st.number_input("開始ゲーム数",0)
            ,"END_count":st.number_input("現在ゲーム数",3000)
        }
        self.game_count = self.dict_inputs["END_count"] - self.dict_inputs["START_count"]
        self.cherry_sum = self.dict_inputs["BB_cherry_count"] + self.dict_inputs["RB_cherry_count"] + self.dict_inputs["cherry_count"]

    def create_pie_graph_detail(self):
        df_probabilities_pie = pd.DataFrame({
            "BB_single":[(row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    / (row.amount_flag_counts)
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "BB_cherry":[(row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                    / (row.amount_flag_counts
                        - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2)))
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_single":[row.RB_single_flag_counts
                    / (row.amount_flag_counts
                        - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2)))
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_cherry":[row.RB_cherry_flag_counts
                    / (row.amount_flag_counts
                        - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - row.RB_single_flag_counts)
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "grapes":[row.grapes_flag_counts
                    / (row.amount_flag_counts
                        - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - row.RB_single_flag_counts
                        - row.RB_cherry_flag_counts)
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "cherry":[row.single_cherry_flag_counts
                    / (row.amount_flag_counts
                        - (row.BB_single_flag_counts + row.BB_rareP_flag_counts + floor((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - (row.BB_cherry_flag_counts + row.BB_rareABP_flag_counts + ceil((row.BB_rareA_flag_counts + row.BB_rareB_flag_counts + row.BB_rareAP_flag_counts + row.BB_rareBP_flag_counts)/2))
                        - row.RB_single_flag_counts
                        - row.RB_cherry_flag_counts
                        - row.grapes_flag_counts)
                    for row in self.df_flag_counts.itertuples(index=False, name="setting")],
        })
        plt.figure(figsize=(8,6))
        probabilities = [
            binom.pmf(self.dict_inputs["BB_single_count"],self.game_count,row.BB_single)
            * binom.pmf(self.dict_inputs["BB_cherry_count"],self.game_count - self.dict_inputs["BB_single_count"],row.BB_cherry)
            * binom.pmf(self.dict_inputs["RB_single_count"],self.game_count - self.dict_inputs["BB_single_count"] - self.dict_inputs["BB_cherry_count"],row.RB_single)
            * binom.pmf(self.dict_inputs["RB_cherry_count"],self.game_count - self.dict_inputs["BB_single_count"] - self.dict_inputs["BB_cherry_count"] - self.dict_inputs["RB_single_count"],row.RB_cherry)
            * binom.pmf(self.dict_inputs["grapes_count"],self.game_count - self.dict_inputs["BB_single_count"] - self.dict_inputs["BB_cherry_count"] - self.dict_inputs["RB_single_count"] - self.dict_inputs["RB_cherry_count"],row.grapes)
            * binom.pmf(self.dict_inputs["cherry_count"],self.game_count - self.dict_inputs["BB_single_count"] - self.dict_inputs["BB_cherry_count"] - self.dict_inputs["RB_single_count"] - self.dict_inputs["RB_cherry_count"] - self.dict_inputs["grapes_count"],row.cherry)
            for row in df_probabilities_pie.itertuples(index=False, name="setting")]
        labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
        plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

        plt.title("総合判定")
        return plt
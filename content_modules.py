import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from math import floor, ceil
import modules

def content_only_bonuses(df_flag_counts):

    st.header("入力欄")
    BB_count = st.number_input("BB回数",0)
    RB_count = st.number_input("RB回数",0)
    START_count = st.number_input("開始ゲーム数",0)
    END_count = st.number_input("現在ゲーム数",3000)
    game_count = END_count - START_count

    # 判別パート
    if st.button("実行"):

        df_probabilities = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
        })

        st.header("総合判定")
        df_outcome = pd.DataFrame({
            "ゲーム数":game_count,
            "BB確率":modules.get_outcome(game_count, BB_count),
            "RB確率":modules.get_outcome(game_count, RB_count)
        },index=["結果"])
        st.dataframe(df_outcome)

        plt = modules.create_pie_graph_only_bonuses(BB_count,RB_count,game_count,df_flag_counts)
        st.pyplot(plt)

        st.header("BBの二項分布")
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("RBの二項分布")
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

def create_content_bonuses_and_grapes(df_flag_counts):
    st.header("入力欄")
    BB_count = st.number_input("BB回数",0)
    RB_count = st.number_input("RB回数",0)
    grapes_count = st.number_input("ブドウ",0)
    START_count = st.number_input("開始ゲーム数",0)
    END_count = st.number_input("現在ゲーム数",3000)
    game_count = END_count - START_count

    # 判別パート
    if st.button("実行"):

        df_probabilities = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.grapes_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
        })

        st.header("総合判定")
        df_outcome = pd.DataFrame({
            "ゲーム数":game_count,
            "BB確率":modules.get_outcome(game_count, BB_count),
            "RB確率":modules.get_outcome(game_count, RB_count),
            "ブドウ":modules.get_outcome(game_count, grapes_count)
        },index=["結果"])
        st.dataframe(df_outcome)

        plt = modules.create_pie_graph_include_grapes(BB_count,RB_count,grapes_count,game_count,df_flag_counts)
        st.pyplot(plt)

        st.header("BBの二項分布")
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("RBの二項分布")
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("ブドウの二項分布")
        plt = modules.create_binom_graph("ブドウ", grapes_count, game_count, df_probabilities,20)
        st.pyplot(plt)

def create_content_detail_happy_v3(df_flag_counts):
    st.header("入力欄")
    dict_inputs ={
        "BB_single_count":st.number_input("BBバラケ目回数",0)
        ,"BB_cherry_count":st.number_input("BBチェリー重複回数",0)
        ,"RB_single_count":st.number_input("RB単独回数",0)
        ,"RB_cherry_count":st.number_input("RBチェリー重複回数",0)
        ,"grapes_count":st.number_input("ブドウ",0)
        ,"cherry_count":st.number_input("ペカらないチェリー",0)
        ,"START_count":st.number_input("開始ゲーム数",0)
        ,"END_count":st.number_input("現在ゲーム数",3000)
    }
    game_count = dict_inputs["END_count"] - dict_inputs["START_count"]
    cherry_sum = dict_inputs["BB_cherry_count"] + dict_inputs["RB_cherry_count"] + dict_inputs["cherry_count"]

    # 判別パート
    if st.button("実行"):

        df_probabilities = pd.DataFrame({
            "BBバラケ目":[(row.BB_single_flag_counts + row.BB_rare_flag_counts + floor(row.BB_rare_cherry_flag_counts/2))/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "BBチェリー重複":[(row.BB_cherry_flag_counts + ceil(row.BB_rare_cherry_flag_counts/2))/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RB単独":[row.RB_single_flag_counts/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RBチェリー重複":[row.RB_cherry_flag_counts/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.grapes_flag_counts/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "ペカらないチェリー":[row.single_cherry_flag_counts/row.amount_flag_counts
                        for row in df_flag_counts.itertuples(index=False, name="setting")],
            "チェリー重複率":[(row.BB_cherry_flag_counts + ceil(row.BB_rare_cherry_flag_counts/2) + row.RB_cherry_flag_counts)/(row.single_cherry_flag_counts + row.BB_cherry_flag_counts + ceil(row.BB_rare_cherry_flag_counts/2) + row.RB_cherry_flag_counts)
                        for row in df_flag_counts.itertuples(index=False, name="setting")]
        })

        st.header("総合判定")
        df_outcome = pd.DataFrame({
            "ゲーム数":game_count,
            "BB合成":modules.get_outcome(game_count, dict_inputs["BB_single_count"] + dict_inputs["BB_cherry_count"]),
            "RB合成":modules.get_outcome(game_count, dict_inputs["RB_single_count"] + dict_inputs["RB_cherry_count"]),
            "BBバラケ目":modules.get_outcome(game_count, dict_inputs["BB_single_count"]),
            "BBチェリー重複":modules.get_outcome(game_count, dict_inputs["BB_cherry_count"]),
            "RB単独":modules.get_outcome(game_count, dict_inputs["RB_single_count"]),
            "RBチェリー重複":modules.get_outcome(game_count, dict_inputs["RB_cherry_count"]),
            "チェリー重複率(%)":round(((dict_inputs["BB_cherry_count"] + dict_inputs["RB_cherry_count"])/cherry_sum)*100,1),
            "ブドウ":modules.get_outcome(game_count, dict_inputs["grapes_count"]),
            "ペカらないチェリー":modules.get_outcome(game_count, dict_inputs["cherry_count"])
        },index=["結果"])
        st.dataframe(df_outcome)

        plt = modules.create_pie_graph_detail_happy_v3(dict_inputs,game_count,cherry_sum,df_flag_counts)
        st.pyplot(plt)

        st.header("BBバラケ目の二項分布")
        plt = modules.create_binom_graph("BBバラケ目", dict_inputs["BB_single_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("BBチェリー重複の二項分布")
        plt = modules.create_binom_graph("BBチェリー重複", dict_inputs["BB_cherry_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("RB単独の二項分布")
        plt = modules.create_binom_graph("RB単独", dict_inputs["RB_single_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("RBチェリー重複の二項分布")
        plt = modules.create_binom_graph("RBチェリー重複", dict_inputs["RB_cherry_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        st.header("チェリー重複率の二項分布")
        plt = modules.create_binom_graph("チェリー重複率", dict_inputs["BB_cherry_count"] + dict_inputs["RB_cherry_count"], cherry_sum, df_probabilities,5)
        st.pyplot(plt)

        st.header("ブドウの二項分布")
        plt = modules.create_binom_graph("ブドウ", dict_inputs["grapes_count"], game_count, df_probabilities,20)
        st.pyplot(plt)

        st.header("ペカらないチェリーの二項分布")
        plt = modules.create_binom_graph("ペカらないチェリー", dict_inputs["cherry_count"], game_count, df_probabilities,10)
        st.pyplot(plt)
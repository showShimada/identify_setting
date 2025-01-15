import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams
from math import floor, ceil
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import modules

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

st.title("ハッピージャグラーV3判別ツール")
"""
# 設定別の確率
"""
BB_flag_counts = [240,242,249,258,274,290]
RB_flag_counts = [165,181,197,218,240,256]
grapes_flag_counts = [10850,10900,10960,11220,11280,11320]
single_cherry_flag_counts = [1033,1029,1021,1004,995,983]
BB_single_flag_counts = [150,152,159,158,174,190]
BB_rare_flag_counts = [26,26,26,26,26,26]
BB_cherry_flag_counts = [44,44,44,54,54,54]
BB_rare_cherry_flag_counts = [20,20,20,20,20,20]
RB_single_flag_counts = [103,115,123,137,150,154]
RB_cherry_flag_counts = [62,66,74,81,90,102]
amount_flag_count = 65536

df_probabilities_for_display = pd.DataFrame({
    "設定":["1","2","3","4","5","6"],
    "BB_合成":[amount_flag_count/flag_count for flag_count in BB_flag_counts],
    "RB_合成":[amount_flag_count/flag_count for flag_count in RB_flag_counts],
    "BB_単独":[amount_flag_count/flag_count for flag_count in BB_single_flag_counts],
    "BB_チェリー重複":[amount_flag_count/flag_count for flag_count in BB_cherry_flag_counts],
    "BB_レアチェリー重複":[amount_flag_count/flag_count for flag_count in BB_rare_cherry_flag_counts],
    "BB_一枚役重複":[amount_flag_count/flag_count for flag_count in BB_rare_flag_counts],
    "RB_単独":[amount_flag_count/flag_count for flag_count in RB_single_flag_counts],
    "RB_チェリー重複":[amount_flag_count/flag_count for flag_count in RB_cherry_flag_counts],
    "ブドウ":[amount_flag_count/flag_count for flag_count in grapes_flag_counts],
    "単独チェリー":[amount_flag_count/flag_count for flag_count in single_cherry_flag_counts]
})
df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
st.dataframe(df_probabilities_for_display)

df_probabilities_detail = pd.DataFrame({
    "BBバラケ目":[(single_flag + rare_flag + floor(rare_cherry_flag/2))/amount_flag_count for single_flag, rare_flag, rare_cherry_flag in zip(BB_single_flag_counts,BB_rare_flag_counts,BB_rare_cherry_flag_counts)],
    "BBチェリー重複":[(cherry_flag + ceil(rare_cherry_flag/2))/amount_flag_count for cherry_flag, rare_cherry_flag in zip(BB_cherry_flag_counts,BB_rare_cherry_flag_counts)],
    "RB単独":[flag_count/amount_flag_count for flag_count in RB_single_flag_counts],
    "RBチェリー重複":[flag_count/amount_flag_count for flag_count in RB_cherry_flag_counts],
    "ブドウ":[flag_count/amount_flag_count for flag_count in grapes_flag_counts],
    "単独チェリー":[flag_count/amount_flag_count for flag_count in single_cherry_flag_counts],
    "ハズレ":[(amount_flag_count - BB_flag_count - RB_flag_count - grapes_flag_count - single_cherry_flag_count)/amount_flag_count for BB_flag_count,RB_flag_count,grapes_flag_count,single_cherry_flag_count in zip(BB_flag_counts,RB_flag_counts,grapes_flag_counts,single_cherry_flag_counts)]
})

option = st.selectbox(
    "入力内容を選んで下さい",
    ("ボーナス確率のみ","ボーナス確率とブドウ","詳細版")
)

if option == "ボーナス確率のみ":
    """
    # 入力欄
    """
    BB_count = st.number_input("BB回数",0)
    RB_count = st.number_input("RB回数",0)
    START_count = st.number_input("開始ゲーム数",0)
    END_count = st.number_input("現在ゲーム数",3000)
    game_count = END_count - START_count

    # 判別パート
    if st.button("実行"):

        df_probabilities = pd.DataFrame({
            "BB":[flag_count/amount_flag_count for flag_count in BB_flag_counts],
            "RB":[flag_count/amount_flag_count for flag_count in RB_flag_counts],
            "ハズレ":[(amount_flag_count - BB_flag_count - RB_flag_count)/amount_flag_count for BB_flag_count,RB_flag_count in zip(BB_flag_counts,RB_flag_counts)]
        })

        """
        # 総合判定
        """
        df_outcome = pd.DataFrame({
            "ゲーム数":game_count,
            "BB確率":modules.get_outcome(game_count, BB_count),
            "RB確率":modules.get_outcome(game_count, RB_count)
        },index=["結果"])
        st.dataframe(df_outcome)

        plt = modules.create_pie_graph_only_bonuses(BB_count,RB_count,game_count,df_probabilities)
        st.pyplot(plt)

        """
        # BBの二項分布
        """
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities)
        st.pyplot(plt)

        """
        # RBの二項分布
        """
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities)
        st.pyplot(plt)

elif option == "ボーナス確率とブドウ":
    """
    # 入力欄
    """
    BB_count = st.number_input("BB回数",0)
    RB_count = st.number_input("RB回数",0)
    grapes_count = st.number_input("ブドウ",0)
    START_count = st.number_input("開始ゲーム数",0)
    END_count = st.number_input("現在ゲーム数",3000)
    game_count = END_count - START_count

    # 判別パート
    if st.button("実行"):

        df_probabilities = pd.DataFrame({
            "BB":[flag_count/amount_flag_count for flag_count in BB_flag_counts],
            "RB":[flag_count/amount_flag_count for flag_count in RB_flag_counts],
            "ハズレ":[(amount_flag_count - BB_flag_count - RB_flag_count)/amount_flag_count for BB_flag_count,RB_flag_count in zip(BB_flag_counts,RB_flag_counts)]
        })
        df_probabilities_include_grapes = pd.DataFrame({
            "BB":[flag_count/amount_flag_count for flag_count in BB_flag_counts],
            "RB":[flag_count/amount_flag_count for flag_count in RB_flag_counts],
            "ブドウ":[flag_count/amount_flag_count for flag_count in grapes_flag_counts],
            "ハズレ":[(amount_flag_count - BB_flag_count - RB_flag_count - grapes_flag_count)/amount_flag_count for BB_flag_count,RB_flag_count,grapes_flag_count in zip(BB_flag_counts,RB_flag_counts,grapes_flag_counts)]
        })

        """
        # 総合判定
        """
        df_outcome = pd.DataFrame({
            "ゲーム数":game_count,
            "BB確率":modules.get_outcome(game_count, BB_count),
            "RB確率":modules.get_outcome(game_count, RB_count),
            "ブドウ":modules.get_outcome(game_count, grapes_count)
        },index=["結果"])
        st.dataframe(df_outcome)

        plt = modules.create_pie_graph_only_bonuses(BB_count,RB_count,game_count,df_probabilities)
        # plt = modules.create_pie_graph_include_grapes(BB_count,RB_count,grapes_count,game_count,df_probabilities_include_grapes)
        st.pyplot(plt)

        """
        # BBの二項分布
        """
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities_include_grapes,5)
        st.pyplot(plt)

        """
        # RBの二項分布
        """
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities_include_grapes,5)
        st.pyplot(plt)

        """
        # ブドウの二項分布
        """
        plt = modules.create_binom_graph("ブドウ", grapes_count, game_count, df_probabilities_include_grapes,20)
        st.pyplot(plt)
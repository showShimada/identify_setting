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
df_flag_counts = pd.DataFrame({
    "BB_flag_counts":[240,242,249,258,274,290],
    "RB_flag_counts":[165,181,197,218,240,256],
    "grapes_flag_counts":[10850,10900,10960,11220,11280,11320],
    "single_cherry_flag_counts":[1033,1029,1021,1004,995,983],
    "BB_single_flag_counts":[150,152,159,158,174,190],
    "BB_rare_flag_counts":[26,26,26,26,26,26],
    "BB_cherry_flag_counts":[44,44,44,54,54,54],
    "BB_rare_cherry_flag_counts":[20,20,20,20,20,20],
    "RB_single_flag_counts":[103,115,123,137,150,154],
    "RB_cherry_flag_counts":[62,66,74,81,90,102],
    "amount_flag_counts":[65536,65536,65536,65536,65536,65536]
})


df_probabilities_for_display = pd.DataFrame({
    "設定":["1","2","3","4","5","6"],
    "BB_合成":[row.amount_flag_counts/row.BB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "RB_合成":[row.amount_flag_counts/row.RB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_単独":[row.amount_flag_counts/row.BB_single_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_チェリー重複":[row.amount_flag_counts/row.BB_cherry_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアチェリー重複":[row.amount_flag_counts/row.BB_rare_cherry_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_一枚役重複":[row.amount_flag_counts/row.BB_rare_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "RB_単独":[row.amount_flag_counts/row.RB_single_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "RB_チェリー重複":[row.amount_flag_counts/row.RB_cherry_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "ブドウ":[row.amount_flag_counts/row.grapes_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "単独チェリー":[row.amount_flag_counts/row.single_cherry_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
})
df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
st.dataframe(df_probabilities_for_display)

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
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
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

        plt = modules.create_pie_graph_only_bonuses(BB_count,RB_count,game_count,df_flag_counts)
        st.pyplot(plt)

        """
        # BBの二項分布
        """
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # RBの二項分布
        """
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities,5)
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
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.grapes_flag_counts/row.amount_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
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

        plt = modules.create_pie_graph_include_grapes(BB_count,RB_count,grapes_count,game_count,df_flag_counts)
        st.pyplot(plt)

        """
        # BBの二項分布
        """
        plt = modules.create_binom_graph("BB", BB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # RBの二項分布
        """
        plt = modules.create_binom_graph("RB", RB_count, game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # ブドウの二項分布
        """
        plt = modules.create_binom_graph("ブドウ", grapes_count, game_count, df_probabilities,20)
        st.pyplot(plt)

elif option == "詳細版":
    """
    # 入力欄
    """
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

        """
        # 総合判定
        """
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

        plt = modules.create_pie_graph_full(dict_inputs,game_count,cherry_sum,df_flag_counts)
        st.pyplot(plt)

        """
        # BBバラケ目の二項分布
        """
        plt = modules.create_binom_graph("BBバラケ目", dict_inputs["BB_single_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # BBチェリー重複の二項分布
        """
        plt = modules.create_binom_graph("BBチェリー重複", dict_inputs["BB_cherry_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # RB単独の二項分布
        """
        plt = modules.create_binom_graph("RB単独", dict_inputs["RB_single_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # RBチェリー重複の二項分布
        """
        plt = modules.create_binom_graph("RBチェリー重複", dict_inputs["RB_cherry_count"], game_count, df_probabilities,5)
        st.pyplot(plt)

        """
        # チェリー重複率の二項分布
        """
        plt = modules.create_binom_graph("チェリー重複率", dict_inputs["BB_cherry_count"] + dict_inputs["RB_cherry_count"], cherry_sum, df_probabilities,5)
        st.pyplot(plt)

        """
        # ブドウの二項分布
        """
        plt = modules.create_binom_graph("ブドウ", dict_inputs["grapes_count"], game_count, df_probabilities,20)
        st.pyplot(plt)

        """
        # ペカらないチェリーの二項分布
        """
        plt = modules.create_binom_graph("ペカらないチェリー", dict_inputs["cherry_count"], game_count, df_probabilities,10)
        st.pyplot(plt)
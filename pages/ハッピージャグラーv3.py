import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
from scipy.stats import binom
from math import comb
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
amount_flag_count = 65536

df_probabilities_for_display = pd.DataFrame({
    "設定":["1","2","3","4","5","6"],
    "BB":[amount_flag_count/flag_count for flag_count in BB_flag_counts],
    "RB":[amount_flag_count/flag_count for flag_count in RB_flag_counts]
})
df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
st.dataframe(df_probabilities_for_display)

df_probabilities = pd.DataFrame({
    "BB":[flag_count/amount_flag_count for flag_count in BB_flag_counts],
    "RB":[flag_count/amount_flag_count for flag_count in RB_flag_counts],
    "ハズレ":[(amount_flag_count - BB_flag_count - RB_flag_count)/amount_flag_count for BB_flag_count,RB_flag_count in zip(BB_flag_counts,RB_flag_counts)]
})

"""
# 入力欄
"""
BB_count = st.number_input("BB回数",0)
RB_count = st.number_input("RB回数",0)
START_count = st.number_input("回転数",0)

# 判別パート
if st.button("実行"):
    """
    # 総合判定
    """
    df_outcome = pd.DataFrame({
        "BB確率":modules.get_outcome(START_count, BB_count),
        "RB確率":modules.get_outcome(START_count, RB_count)
    },index=["結果"])
    st.dataframe(df_outcome)

    plt.figure(figsize=(8,6))
    probabilities = [(comb(START_count, BB_count) * comb(START_count - BB_count, RB_count) *
            (row.BB ** BB_count) * (row.RB ** RB_count) *
            (row.ハズレ ** (START_count - BB_count - RB_count))) 
            for row in df_probabilities.itertuples(index=False, name="setting")]
    labels = [f'設定：{i}' for i in range(1, len(probabilities) +1 )]
    plt.pie(probabilities, labels=labels, startangle=90, counterclock=False, autopct="%.1f%%", pctdistance=0.8)

    plt.title("総合判定")
    st.pyplot(plt)

    """
    # BBの二項分布
    """
    plt = modules.create_binom_graph("BB", BB_count, START_count, df_probabilities)
    st.pyplot(plt)

    """
    # RBの二項分布
    """
    plt = modules.create_binom_graph("RB", RB_count, START_count, df_probabilities)
    st.pyplot(plt)
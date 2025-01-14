import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
from scipy.stats import binom

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
    "設定":["1","2","3","4","5","6"],
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
    # 今回の出現率
    """
    try:
        BB_outcome = round(START_count/BB_count,1)
    except ZeroDivisionError:
        BB_outcome = np.nan
    try:
        RB_outcome = round(START_count/RB_count,1)
    except ZeroDivisionError:
        RB_outcome = np.nan


    df_outcome = pd.DataFrame({
        "BB確率":BB_outcome,
        "RB確率":RB_outcome
    },index=["結果"])
    st.dataframe(df_outcome)

    """
    # BBの二項分布
    """
    range_count = range(max(0,BB_count - 5),min(START_count,BB_count + 5) + 1)

    plt.figure(figsize=(8,6))
    for i,p in enumerate(df_probabilities["BB"].tolist()):
        probabilities = [binom.pmf(count,START_count,p) for count in range_count]
        plt.plot(range_count, probabilities, marker='o', label=f'設定：{i +1}')
    
    bar_values = [max(probabilities) + (max(probabilities)/10) if count == BB_count else 0 for count in range_count]

    plt.bar(range_count, bar_values, color="blue", alpha=0.5, label="今回")

    plt.title("BBの二項分布")
    plt.xlabel("BB回数")
    plt.ylabel("確率")
    plt.xticks(range_count)
    plt.legend()
    plt.grid()
    plt.tight_layout()

    st.pyplot(plt)

    """
    # RBの二項分布
    """
    range_count = range(max(0,RB_count - 5),min(START_count,RB_count + 5) + 1)

    plt.figure(figsize=(8,6))
    for i,p in enumerate(df_probabilities["RB"].tolist()):
        probabilities = [binom.pmf(count,START_count,p) for count in range_count]
        plt.plot(range_count, probabilities, marker='o', label=f'設定：{i +1}')
    
    bar_values = [max(probabilities) + (max(probabilities)/10) if count == RB_count else 0 for count in range_count]

    plt.bar(range_count, bar_values, color="blue", alpha=0.5, label="今回")

    plt.title("RBの二項分布")
    plt.xlabel("RB回数")
    plt.ylabel("確率")
    plt.xticks(range_count)
    plt.legend()
    plt.grid()
    plt.tight_layout()

    st.pyplot(plt)
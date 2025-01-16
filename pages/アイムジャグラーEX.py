import streamlit as st
import pandas as pd
from matplotlib import rcParams
from math import floor, ceil
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import content_modules

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

st.title("アイムジャグラーEX判別ツール")
"""
# 設定別の確率
"""
df_flag_counts = pd.DataFrame({
    "BB_flag_counts":[240,243,243,253,253,257],
    "RB_flag_counts":[149,164,198,208,257,257],
    "grapes_flag_counts":[10890,10890,10890,10890,10890,11340],
    "amount_flag_counts":[65536,65536,65536,65536,65536,65536]
})


df_probabilities_for_display = pd.DataFrame({
    "設定":["1","2","3","4","5","6"],
    "BB_合成":[row.amount_flag_counts/row.BB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "RB_合成":[row.amount_flag_counts/row.RB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "ブドウ":[row.amount_flag_counts/row.grapes_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")]
})
df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
st.dataframe(df_probabilities_for_display)

option = st.selectbox(
    "入力内容を選んで下さい",
    ("ボーナス確率のみ","ボーナス確率とブドウ")
)

if option == "ボーナス確率のみ":
    content_modules.content_only_bonuses(df_flag_counts)

elif option == "ボーナス確率とブドウ":
    content_modules.create_content_bonuses_and_grapes(df_flag_counts)
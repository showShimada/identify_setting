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
    content_modules.content_only_bonuses(df_flag_counts)

elif option == "ボーナス確率とブドウ":
    content_modules.create_content_bonuses_and_grapes(df_flag_counts)

elif option == "詳細版":
    content_modules.create_content_detail_happy_v3(df_flag_counts)
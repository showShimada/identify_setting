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

st.title("マイジャグラー5判別ツール")
"""
# 設定別の確率
"""
df_flag_counts = pd.DataFrame({
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


df_probabilities_for_display = pd.DataFrame({
    "設定":["1","2","3","4","5","6"],
    "BB_合成":[row.amount_flag_counts/row.BB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "RB_合成":[row.amount_flag_counts/row.RB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_単独":[row.amount_flag_counts/row.BB_single_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_チェリー重複":[row.amount_flag_counts/row.BB_cherry_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアA":[row.amount_flag_counts/row.BB_rareA_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアB":[row.amount_flag_counts/row.BB_rareB_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアP":[row.amount_flag_counts/row.BB_rareP_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアAP":[row.amount_flag_counts/row.BB_rareAP_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアBP":[row.amount_flag_counts/row.BB_rareBP_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
    "BB_レアABP":[row.amount_flag_counts/row.BB_rareABP_flag_counts for row in df_flag_counts.itertuples(index=False, name="setting")],
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
    content_modules.create_content_detail_my_juggler(df_flag_counts)
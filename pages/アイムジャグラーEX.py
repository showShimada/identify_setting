import streamlit as st
# import pandas as pd
from matplotlib import rcParams
# from math import floor, ceil
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from class_im_juggler_ex import im_juggler_ex

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

st.title("アイムジャグラーEX判別ツール")
"""
# 設定別の確率
"""
content = im_juggler_ex()

option = st.selectbox(
    "入力内容を選んで下さい",
    ("ボーナス確率のみ","ボーナス確率とブドウ")
)

if option == "ボーナス確率のみ":
    content.content_only_bonuses()

elif option == "ボーナス確率とブドウ":
    content.create_content_bonuses_and_grapes()
import streamlit as st
import pandas as pd
from matplotlib import rcParams
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from class_my_juggler_5 import my_juggler_5

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

st.title("マイジャグラー5判別ツール")
"""
# 設定別の確率
"""
content = my_juggler_5()
option = st.selectbox(
    "入力内容を選んで下さい",
    ("ボーナス確率のみ","ボーナス確率とブドウ","詳細版")
)

if option == "ボーナス確率のみ":
    content.content_only_bonuses()
elif option == "ボーナス確率とブドウ":
    content.create_content_bonuses_and_grapes()
elif option == "詳細版":
    content.create_content_detail()
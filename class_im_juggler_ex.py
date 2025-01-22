import streamlit as st
import pandas as pd
from class_parent import parent

class im_juggler_ex(parent):
    def __init__(self):
        self.df_flag_counts = pd.DataFrame({
            "BB_flag_counts":[240,243,243,253,253,257],
            "RB_flag_counts":[149,164,198,208,257,257],
            "grapes_flag_counts":[10890,10890,10890,10890,10890,11340],
            "amount_flag_counts":[65536,65536,65536,65536,65536,65536]
        })

        self.df_probabilities = pd.DataFrame({
            "BB":[row.BB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB":[row.RB_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.grapes_flag_counts/row.amount_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")]
        })

        self.display_probabilities()

    def display_probabilities(self):
        df_probabilities_for_display = pd.DataFrame({
            "設定":["1","2","3","4","5","6"],
            "BB_合成":[row.amount_flag_counts/row.BB_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "RB_合成":[row.amount_flag_counts/row.RB_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")],
            "ブドウ":[row.amount_flag_counts/row.grapes_flag_counts for row in self.df_flag_counts.itertuples(index=False, name="setting")]
        })
        df_probabilities_for_display = df_probabilities_for_display.set_index("設定")
        st.dataframe(df_probabilities_for_display)
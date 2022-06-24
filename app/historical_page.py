import datetime

import streamlit as st

from utils import read_hisotrical_data

col1, col2 = st.columns([1, 1])

with col1:
    date_from = st.date_input("start date", datetime.date.today())
with col2:
    date_to = st.date_input("end date", datetime.date.today())

set_of_titles_urls = list(read_hisotrical_data(str(date_from), str(date_to)))

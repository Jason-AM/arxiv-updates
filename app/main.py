import datetime
from pathlib import Path

import streamlit as st

from utils import body, head, read_data

NUM_ARTICLES_PER_PAGE = 3

head()

if "articles" not in st.session_state:
    st.session_state["articles"] = NUM_ARTICLES_PER_PAGE


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    date_from = st.date_input("start date", datetime.date.today())
with col2:
    date_to = st.date_input("end date", datetime.date.today())


next_articles = st.button("Next articles")


if next_articles:

    DATA_DIR = Path("./data")

    filename = DATA_DIR / f"stat-ml_cs-LG_{date_from}-{date_to}.pkl"
    set_of_titles_urls = list(read_data(filename))

    current_article_set = st.session_state["articles"]

    list_of_current_titles_urls = set_of_titles_urls[
        current_article_set - NUM_ARTICLES_PER_PAGE : current_article_set
    ]
    st.session_state.articles += NUM_ARTICLES_PER_PAGE

    body(list_of_current_titles_urls)

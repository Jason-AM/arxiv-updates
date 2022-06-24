import pickle
from pathlib import Path
from typing import List

import streamlit as st

from article_info_extraction import get_and_save_info
from rss_extraction import get_title_link_from_rss

DATA_DIR = Path("./data")


@st.cache(suppress_st_warning=True)
def read_hisotrical_data(date_from, date_to):

    filename = DATA_DIR / f"stat-ml_cs-LG_{date_from}-{date_to}.pkl"

    if filename.is_file():
        print("loaded_data")
        with open(filename, "rb") as fp:
            titles_urls = pickle.load(fp)
    else:
        st.write("First computation of day - excpect delay in loading")
        titles_urls = get_and_save_info(date_from, date_to)
    return titles_urls


@st.cache(suppress_st_warning=True)
def read_todays_data(topics: List[str] = ["cs.LG", "stat.ML"]):
    title_link_set = set()
    for topic in topics:
        title_link_set = title_link_set.union(get_title_link_from_rss(topic))
    return title_link_set


def head():
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: -35px;'>
        ArXiv Summary
        </h1>
    """,
        unsafe_allow_html=True,
    )

    st.caption(
        """
        <p style='text-align: center'>
        by <a href='https://medium.com/geoclid'>Geoclid</a>
        </p>
    """,
        unsafe_allow_html=True,
    )

    st.write(
        "Over the difficulty of sifiting through new ArXiv releases. ",
        "Click the button for todays ArXiv summary \U0001F642.",
    )


def display_articles(list_of_current_titles_urls, article_start_number):
    for i, (title, url) in enumerate(list_of_current_titles_urls):
        st.write(f"{article_start_number + i}. {title.capitalize()} ({url})")

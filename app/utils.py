import pickle
from pathlib import Path

import streamlit as st

from article_info_extraction import get_and_save_info


@st.cache(suppress_st_warning=True)
def read_data(path):
    DATA_DIR = Path("./data")
    date_from = "2022-06-16"
    date_to = "2022-06-17"

    filename = DATA_DIR / f"stat-ml_cs-LG_{date_from}-{date_to}.pkl"

    if filename.is_file():
        print("loaded_data")
        with open(filename, "rb") as fp:
            titles_urls = pickle.load(fp)
    else:
        titles_urls = get_and_save_info(date_from, date_to)
    return titles_urls


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


def body(list_of_current_titles_urls):
    for title, url in list_of_current_titles_urls:
        st.markdown("---")
        st.write(f"{title.capitalize()}")
        st.write(f"Link: {url}")
    st.markdown("---")

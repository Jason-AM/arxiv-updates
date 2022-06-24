import streamlit as st

from noun_chunk import get_word_cloud
from utils import display_articles, read_todays_data


def analysis_page():
    list_of_titles_urls = list(read_todays_data(["cs.LG"]))

    # st.pyplot(fig=get_word_cloud(list_of_titles_urls))
    for word in get_word_cloud(list_of_titles_urls):
        st.text(word)

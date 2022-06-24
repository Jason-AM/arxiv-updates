import streamlit as st

from noun_chunk import get_word_cloud
from utils import read_todays_data


def analysis_page():
    list_of_titles_urls = list(read_todays_data(["cs.LG"]))

    # st.pyplot(fig=get_word_cloud(list_of_titles_urls))

    st.markdown(
        """
        <h3 style='text-align: center; margin-bottom: -35px;'>
        Top phrases found
        </h1>
    """,
        unsafe_allow_html=True,
    )

    for word in get_word_cloud(list_of_titles_urls):
        st.text(word)

import streamlit as st

from noun_chunk import get_word_cloud
from utils import read_todays_data


def analysis_page():
    list_of_titles_urls = list(read_todays_data(["cs.LG"]))

    # st.pyplot(fig=get_word_cloud(list_of_titles_urls))

    st.markdown(
        """
        ## Top phrases found

        Prints top 30 by default


        ---


        """
    )

    for i, word in enumerate(get_word_cloud(list_of_titles_urls)):
        st.markdown(f"{i+1}. {word.capitalize()}")

import random
from pathlib import Path

import streamlit as st

from analysis_page import analysis_page
from article_ordering import sort_articles_by_key_words
from utils import display_articles, head, read_todays_data

NUM_ARTICLES_PER_PAGE = 5

DATA_DIR = Path("./data")


def reset_current_article_num():
    st.session_state["article_display_start_index"] = 0


def get_article_list_to_show(list_of_titles_urls, start_indx, end_indx):

    list_of_current_titles_urls = list_of_titles_urls[start_indx:end_indx]

    article_start_number = start_indx + 1
    display_articles(list_of_current_titles_urls, article_start_number)


def main_page():

    head()

    if "article_display_start_index" not in st.session_state:
        reset_current_article_num()

    list_of_titles_urls = list(read_todays_data(["cs.LG"]))

    key_words_inputted = st.text_input(
        "Words to surface", value=st.session_state.get("key_words", "")
    )

    if "key_words" not in st.session_state:
        st.session_state["key_words"] = key_words_inputted

    if key_words_inputted != st.session_state["key_words"]:
        st.session_state["key_words"] = key_words_inputted
        reset_current_article_num()

    list_of_key_words = key_words_inputted.split(",") if key_words_inputted else None

    if list_of_key_words:
        sorted_list_of_titles_urls = sort_articles_by_key_words(
            list_of_titles_urls, list_of_key_words
        )
    else:
        sorted_list_of_titles_urls = list_of_titles_urls

    previous_button, next_button, random_spin, _ = st.columns([1, 1, 1, 1.5])
    with previous_button:
        previous_articles = st.button("Previous articles")
    with next_button:
        next_articles = st.button("Next articles")
    with random_spin:
        random_articles = st.button("Random articles")

    st.write(f"Total of {len(sorted_list_of_titles_urls)} articles")

    if random_articles:
        random_start_indx = random.randint(
            0, len(sorted_list_of_titles_urls) - NUM_ARTICLES_PER_PAGE
        )
        get_article_list_to_show(
            sorted_list_of_titles_urls,
            random_start_indx,
            random_start_indx + NUM_ARTICLES_PER_PAGE,
        )
        reset_current_article_num()
    else:

        if previous_articles:
            # ensure that start index must be at least 0
            updated_start_indx = max(
                st.session_state["article_display_start_index"] - NUM_ARTICLES_PER_PAGE,
                0,
            )

            st.session_state["article_display_start_index"] = updated_start_indx

        if next_articles:

            # ensure that start index can't be more than the number of articles on the
            # last page
            updated_start_indx = min(
                st.session_state["article_display_start_index"] + NUM_ARTICLES_PER_PAGE,
                len(sorted_list_of_titles_urls) - NUM_ARTICLES_PER_PAGE,
            )

            st.session_state["article_display_start_index"] = updated_start_indx

        start_idx = st.session_state["article_display_start_index"]
        end_idx = start_idx + NUM_ARTICLES_PER_PAGE
        get_article_list_to_show(sorted_list_of_titles_urls, start_idx, end_idx)


page_names_to_funcs = {
    "Main Page": main_page,
    "Analysis page": analysis_page,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

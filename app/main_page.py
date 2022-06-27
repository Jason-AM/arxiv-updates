import random
from pathlib import Path

import streamlit as st

from article_ordering import sort_articles_by_key_words
from utils import read_todays_data

NUM_ARTICLES_PER_PAGE = 5

DATA_DIR = Path("./data")


def reset_current_article_num():
    st.session_state["article_display_start_index"] = 0


def show_titles_urls_abstract(list_of_titles_urls, start_indx, end_indx):

    list_of_current_titles_urls = list_of_titles_urls[start_indx:end_indx]

    article_start_number = start_indx + 1

    for i, (title, url, abstract) in enumerate(list_of_current_titles_urls):

        st.write(f"{article_start_number + i}. {title.capitalize()} ({url})")

        _, container, _ = st.columns([0.1, 1, 0.1])
        with container:
            expander = st.expander("Abstract")
            expander.write(abstract)


def heading():

    st.markdown(
        """
        # ArXiv Summary

        Over the difficulty of sifiting through new ArXiv releases.
        Easily explore todays ArXiv uploads. \U0001F642.

        ---


        """
    )


def initilization_of_states():
    if "article_display_start_index" not in st.session_state:
        reset_current_article_num()

    if "last_button_pressed" not in st.session_state:
        st.session_state["last_button_pressed"] = "previous"


def previous_next_random_update(button_type):
    """Callback function that updates when a previous/nect/random button in pressed"""
    st.session_state["last_button_pressed"] = button_type


def main_page():

    # get heading text
    heading()

    # initilize states if not already initilialsed
    initilization_of_states()

    # get arxiv info from rss feed
    list_of_titles_urls = sorted(read_todays_data(["cs.LG", "stat.ML"]))

    # manage title ordering from word search
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

    # set up previous, next and random for title viewing
    previous_button, next_button, random_spin, _ = st.columns([1, 1, 1, 1.5])
    # with previous_button:
    #     previous_articles = st.button("Previous articles")
    # with next_button:
    #     next_articles = st.button("Next articles")
    # with random_spin:
    #     random_articles = st.button("Random articles")

    with previous_button:
        st.button(
            "Previous articles",
            key="upper_preivous_button",
            on_click=previous_next_random_update,
            args=("previous",),
        )
    with next_button:
        st.button(
            "Next articles",
            key="upper_next_button",
            on_click=previous_next_random_update,
            args=("next",),
        )
    with random_spin:
        st.button(
            "Random articles",
            key="random_button",
            on_click=previous_next_random_update,
            args=("random",),
        )

    st.write(f"Total of {len(sorted_list_of_titles_urls)} articles")

    if st.session_state["last_button_pressed"] == "random":

        random_start_indx = random.randint(
            0, len(sorted_list_of_titles_urls) - NUM_ARTICLES_PER_PAGE
        )

        show_titles_urls_abstract(
            sorted_list_of_titles_urls,
            random_start_indx,
            random_start_indx + NUM_ARTICLES_PER_PAGE,
        )

        # after random spin we start back at index 0
        reset_current_article_num()
    else:
        if st.session_state["last_button_pressed"] == "previous":
            # ensure that start index must be at least 0
            updated_start_indx = max(
                st.session_state["article_display_start_index"] - NUM_ARTICLES_PER_PAGE,
                0,
            )

            st.session_state["article_display_start_index"] = updated_start_indx

        elif st.session_state["last_button_pressed"] == "next":

            # ensure that start index can't be more than the number of articles on the
            # last page
            updated_start_indx = min(
                st.session_state["article_display_start_index"] + NUM_ARTICLES_PER_PAGE,
                len(sorted_list_of_titles_urls) - NUM_ARTICLES_PER_PAGE,
            )

            st.session_state["article_display_start_index"] = updated_start_indx

        start_idx = st.session_state["article_display_start_index"]
        end_idx = start_idx + NUM_ARTICLES_PER_PAGE
        show_titles_urls_abstract(sorted_list_of_titles_urls, start_idx, end_idx)

    # set up previous, next and random for title viewing
    previous_button_lower, next_button_lower, _ = st.columns([1, 1, 2.5])
    with previous_button_lower:
        st.button(
            "Previous articles",
            key="lower_preivous_button",
            on_click=previous_next_random_update,
            args=("previous",),
        )
    with next_button_lower:
        st.button(
            "Next articles",
            key="lower_next_button",
            on_click=previous_next_random_update,
            args=("next",),
        )

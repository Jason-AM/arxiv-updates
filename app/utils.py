from pathlib import Path
from typing import List

import streamlit as st

from rss_extraction import get_title_link_from_rss

DATA_DIR = Path("./data")


@st.cache(suppress_st_warning=True)
def read_todays_data(topics: List[str] = ["cs.LG", "stat.ML"]):
    title_link_set = set()
    for topic in topics:
        title_link_set = title_link_set.union(get_title_link_from_rss(topic))
    return title_link_set

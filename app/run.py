import streamlit as st

from analysis_page import analysis_page
from main_page import main_page

st.set_page_config(page_title="ArXiv Summary")

page_names_to_funcs = {
    "Main Page": main_page,
    "Analysis page": analysis_page,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

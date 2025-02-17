import streamlit as st

st.title("남양주양지초등학교")

option_menu = st.sidebar.selectbox(
    'Menu',
     ('페이지1', '페이지2', '페이지3'))


with st.sidebar:
    choice = option_menu("Menu", ["페이지1", "페이지2", "페이지3"],
                         icons=['house', 'kanban', 'bi bi-robot'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )
import streamlit as st
from utils.menu import Menu

# Redirect to app.py if not logged in, otherwise show the navigation menu
Menu().render_menu()

st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
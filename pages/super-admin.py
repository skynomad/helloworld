import streamlit as st
from utils.menu import Menu 

# Redirect to app.py if not logged in, otherwise show the navigation menu
Menu().render_menu_with_redirect()
# Verify the user's role
if st.session_state.role not in ["super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to super-admins")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
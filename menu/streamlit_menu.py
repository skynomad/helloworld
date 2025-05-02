import streamlit as st
import pathlib

from utils.menu import page2, page3, page4, north_star

current_dir = pathlib.Path(__file__).parent.resolve()
st.logo(str(current_dir / "images/oracle-cloud.png"), 
        size="large", 
        link="https://cloud.oracle.com", 
        icon_image=str(current_dir / "images/oracle-cloud.png"))

###############################################################################
###  LOGIN                                                                   
###

#if st.query_params.get("test_more_pages", False):
#    st.session_state.logged_in = True

from utils.keycloakutils import KeycloakUtils

if "logged_in" not in st.session_state:
    # Log in
    with st.form("login_form"):
        st.write("Welcome to the AI Chatbot Apps. You'll need to log in to continue.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        login_button = st.form_submit_button("Login")  # Submit button for the form
        if login_button:
            try:
                # Use the correct method for direct access grants
                keycloak = KeycloakUtils(
                    server_url=st.secrets["keycloak"]["server_url"],
                    realm_name=st.secrets["keycloak"]["realm_name"],
                    client_id=st.secrets["keycloak"]["client_id"],
                    client_secret=st.secrets["keycloak"]["client_secret"]
                )
                
                st.session_state.token = keycloak.get_token(
                    username=username,
                    password=password
                )
                
                st.session_state.user_info = keycloak.get_user_info(
                    st.session_state.token["access_token"]
                )
            except Exception as error:
                st.error(f"Login failed: {error}")
                st.stop()
            
            st.session_state.logged_in = True
            st.rerun()
        else:
            def empty_page():
                pass
            pg = st.navigation(
                [st.Page(empty_page, title="Streamlit AI Chatbot")], 
                position="hidden"
            )
            pg.run()
            st.stop()
###
### LOGIN 
###############################################################################

st.header("📖 AI Chatbot : Demo ")

"""
**Streamlit AI Chatbot With Oracle Cloud Infrastructure (OCI) and MCP Server**
"""

# 사용자 정보 및 로그아웃
with st.sidebar:
    # userinfo : User Info: {'sub': '1784f0b5-75e5-461e-8779-d4d73487f298', 'email_verified': False, 'name': 'Thomas Kim', 'preferred_username': 'thomaskim', 'given_name': 'Thomas', 'family_name': 'Kim', 'email': 'kimsh92@example.com'}
    st.subheader(f"Welcome, {st.session_state.user_info.get('name', [])}")
    # st.slider("Amount of fun", 0, 1000, 450, key="slide")
    # st.radio("Your thoughts", ["I agree", "I disagree"], key="radio")
    # st.text_input("Thoughts", placeholder="Add your thoughts", label_visibility="collapsed")
    # st.button("Submit")
    if st.button("Logout"):
        del st.session_state["logged_in"]
        st.session_state = {}
        st.rerun()


### Add pages as functions (can also point to separate files) ###
# Page Navigation
pg = st.navigation({
    "AI Chatbot": [
        # Load pages from functions
        st.Page("pages/chatbot.py", title="Home", default=True, icon=":material/home:", url_path=""),
        st.Page("pages/langchain_chatbot.py", title="Chatbot w/ MCP", icon=":material/star_border:", url_path="chatbot"),
        ],
    "Others": [
        # You can also load pages from files, as usual
        st.Page("pages/movies.py", title="Movie Explorer", icon=":material/movie_filter:", url_path="movie"),
        st.Page("pages/apps.py", title="App statuses over time", icon=":material/access_time:", url_path="apps"),
        st.Page("pages/dialogs.py", title="Dialogs", icon=":material/feedback:"),
        ],
})
##########################################################################################
# pg = st.navigation({
#     "Overview": [
#         # Load pages from functions
#         st.Page(north_star, title="Home", default=True, icon=":material/home:", url_path=""),
#         st.Page(north_star, title="North Star", icon=":material/star_border:", url_path="north_star2"),
#         ],
#     "Metrics": [
#         st.Page(page2, title="Core Metrics", icon=":material/hourglass_top:"),
#         # You can also load pages from files, as usual
#         st.Page("movies.py", title="Movie Explorer", icon=":material/movie_filter:"),
#         st.Page(page3, title="App statuses over time", icon=":material/access_time:"),
#         st.Page(page3, title="Cloud apps leaderboard", icon=":material/share:", url_path="cloud_apps_leaderboard"),
#         st.Page(page4, title="Dialogs", icon=":material/feedback:"),
#         ],
# })
##########################################################################################

try:
    pg.run()
except Exception as error:
   st.error(f"Page Navigation went wrong: {str(error)}", icon=":material/error:")
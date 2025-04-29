import streamlit as st
import logging
from datetime import datetime

# Configure logging
log_filename = f"user_activity_{datetime.now().strftime('%Y-%m-%d')}.log"  # Log file with current date
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Log to a date-specific file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

st.title("Streamlit with Keycloak Authentication")

# Check if the user is logged in
if not st.experimental_user.is_logged_in:
    st.write("You are not logged in.")
    if st.button("Log in with Keycloak"):
        st.login("keycloak")  # matches [auth.keycloak] in secrets.toml
else:
    # User is logged in
    user_info = {key: st.experimental_user.get(key, "N/A") for key in st.experimental_user.keys()}
    logger.info("User info: %s", user_info)  # Log all user properties to file and console
    
    st.write(f"Hello, {st.experimental_user.name}!")
    st.write("Email:", st.experimental_user.get("email", "N/A"))
    # ... any other user info from st.experimental_user

    if st.button("Log out"):
        st.logout()


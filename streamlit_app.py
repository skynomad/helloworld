from dataclasses import asdict
from streamlit_keycloak import login
import streamlit as st


def main():
    st.subheader(f"Welcome {keycloak.user_info['preferred_username']}!")
    st.write(f"Here is your user information:")
    st.write(asdict(keycloak))

    if st.button("Disconnect"):
        keycloak.authenticated = False


st.title("Streamlit Keycloak example")
keycloak = login(
    url="http://150.230.98.136:18080",
    realm="myrealm",
    client_id="myclient",
    auto_refresh=False,
    init_options={
        "checkLoginIframe": False,
        "enableLogging": True,
        "onLoad": "login-required"  # Force login
    },
    custom_labels={
        "labelButton": "Sign in",
        "labelLogin": "Please sign in to your account.",
        "errorNoPopup": "Unable to open the authentication popup. Allow popups and refresh the page to proceed.",
        "errorPopupClosed": "Authentication popup was closed manually.",
        "errorFatal": "Unable to connect to Keycloak using the current configuration."   
    }
)

st.write(keycloak.authenticated)

if keycloak.authenticated:
    st.write("test")
    main()
else:
    st.warning("login required")
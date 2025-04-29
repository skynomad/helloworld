from streamlit_keycloak import login
import streamlit as st

st.title("Keycloak example")
keycloak = login(
    url="http://150.230.98.136:18080",
    realm="myrealm",
    client_id="myclient",
    auto_refresh=False,
    key="keycloak"
)

if keycloak.authenticated:
    print(keycloak.user_info)
    st.write(keycloak)
else:
    st.warning("login required")
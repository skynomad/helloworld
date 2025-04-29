import streamlit as st
from time import sleep
from keycloak import KeycloakOpenID
from utils.menu import Menu

Menu().render_menu()

# Keycloak configuration variables
KEYCLOAK_SERVER_URL = "http://150.230.98.136:18080/"  # Base URL of the Keycloak server
KEYCLOAK_REALM = "myrealm"
KEYCLOAK_CLIENT_ID = "myclient"
KEYCLOAK_CLIENT_SECRET = "F1M3Im4i6yFZ9LG49LauBgC4PbasqRv9"
KEYCLOAK_REDIRECT_URI = "http://150.230.98.136:8501"

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
)

# Login button
if "token" not in st.session_state:
    st.session_state["token"] = None

if st.session_state["token"] is None:
    # Option to log in using username and password
    st.write("Log In using your username and password")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            # Use the correct method for direct access grants
            token = keycloak_openid.token(
                username=username,
                password=password,
                grant_type="password",
                client_id=KEYCLOAK_CLIENT_ID,
                client_secret_key=KEYCLOAK_CLIENT_SECRET,
            )
            st.session_state.token = token
            
            st.success("Login successful!")
            
            # User Info: {'sub': '1784f0b5-75e5-461e-8779-d4d73487f298', 'email_verified': False, 'name': 'Thomas Kim', 'preferred_username': 'thomaskim', 'given_name': 'Thomas', 'family_name': 'Kim', 'email': 'kimsh92@example.com'}
            userinfo = keycloak_openid.userinfo(token['access_token'])
            st.session_state.username = userinfo.get("username", [])
            st.session_state.role = userinfo.get("realm_access", {}).get("roles", ["user"])[0]
            st.session_state.token = token['access_token']
            
            st.write(f"User Info: {userinfo}")
            st.write(f"Token: {st.session_state.token}")
            st.write(f"Role: {userinfo.get("realm_access", {})}")
            #sleep(1)
            
            # Redirect to the main page
            #Menu().set_role("user")
            #Menu().render_menu_with_redirect()
            
        except Exception as error:
            st.error(f"Login failed: {error}")
            pass
else:
    # If already logged in, show the token and role
    st.info("You are already logged in.")
    Menu().render_menu_with_redirect()
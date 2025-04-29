import streamlit as st
from keycloak import KeycloakOpenID

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
    #login_url = keycloak_openid.auth_url(redirect_uri=KEYCLOAK_REDIRECT_URI)

    # if st.button("Login"):
    #     st.write(f"Please visit the following URL to log in: {login_url}")

    # Option to log in using username and password
    st.write("Log In using your username and password")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.info("Please log in to continue.")
    
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
            st.session_state["token"] = token
            st.success("Login successful!")
            
            # Redirect to another page
            st.query_params(page="dashboard")
        except Exception as error:
            st.error(f"Login failed: {error}")

    # if auth_code:
    #     try:
    #         token = keycloak_openid.token(auth_code=auth_code)
    #         st.session_state["token"] = token
    #         st.success("Login successful!")
    #     except Exception as error:
    #         st.error(f"Login failed: {error}")
    # else:
    #     st.info("Waiting for authorization code...")
else:
    st.write("You are logged in!")
    st.write(st.session_state["token"])
    
        # Use st.query_params to get query parameters
    query_params = st.query_params
    st.write("Query Parameters:", query_params)

    auth_code = query_params.get("code", [None])[0]
    st.write("Authorization Code:", auth_code)

    if st.button("Logout"):
        st.session_state["token"] = None
        st.success("Logged out successfully!")

# Handle redirection to other pages
query_params = st.query_params  # Replace experimental_get_query_params with query_params
if query_params.get("page") == ["dashboard"]:
    st.write("Welcome to the Dashboard!")
    st.write("This is another page after successful login.")
    # Add dashboard content here

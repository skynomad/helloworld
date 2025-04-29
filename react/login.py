from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import List
from keycloak import KeycloakOpenID

app = FastAPI()

# Keycloak settings
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8180/auth/",
    realm_name="FastApi",
    client_id="fast_api",
    client_secret_key="secret",
)

# OAuth2 scheme using Keycloak
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://localhost:8180/auth/realms/FastApi/protocol/openid-connect/auth",
    tokenUrl="http://localhost:8180/auth/realms/FastApi/protocol/openid-connect/token")


# Dependency to validate token and get user roles
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        d = keycloak_openid.userinfo(token)
        userinfo = keycloak_openid.userinfo(token)
        user_roles = userinfo.get("roles", [])
        if 'admin' not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not authorized to access this resource",
            )
        return user_roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@app.get("/public", tags=["public"])
async def public_endpoint():
    token = keycloak_openid.token("test", "test")
    return {"token": token}


# Protected endpoint
@app.get("/protected", tags=["protected"])
async def protected_endpoint(current_user_roles: List[str] = Depends(get_current_user)):
    return {"message": "This is a protected endpoint", "user_roles": current_user_roles}

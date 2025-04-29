from keycloak import KeycloakOpenID

class KeycloakUtils:
    def __init__(self, server_url, realm_name, client_id, client_secret):
        """
        Keycloak 클라이언트를 초기화합니다.

        Args:
            server_url (str): Keycloak 서버의 URL (예: "http://localhost:8080/auth/").
            realm_name (str): Keycloak Realm 이름.
            client_id (str): Keycloak 클라이언트 ID.
            client_secret (str): Keycloak 클라이언트 비밀 키.
        """
        self.keycloak_openid = KeycloakOpenID(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
            client_secret_key=client_secret,
        )

    def get_token(self, username, password):
        """
        사용자 이름과 비밀번호를 사용하여 액세스 토큰을 가져옵니다.

        Args:
            username (str): Keycloak 사용자 이름.
            password (str): Keycloak 사용자 비밀번호.

        Returns:
            dict: 액세스 토큰 정보가 포함된 딕셔너리.

        Raises:
            Exception: 토큰 가져오기에 실패한 경우 예외를 발생시킵니다.
        """
        try:
            token = self.keycloak_openid.token(
                username=username,
                password=password,
                grant_type="password",  # 비밀번호 인증 방식 사용
            )
            return token
        except Exception as e:
            raise Exception(f"Failed to get token: {e}")

    def get_user_info(self, access_token):
        """
        액세스 토큰을 사용하여 사용자 정보를 가져옵니다.

        Args:
            access_token (str): Keycloak에서 발급된 액세스 토큰.

        Returns:
            dict: 사용자 정보가 포함된 딕셔너리.

        Raises:
            Exception: 사용자 정보 가져오기에 실패한 경우 예외를 발생시킵니다.
        """
        try:
            user_info = self.keycloak_openid.userinfo(access_token)
            return user_info
        except Exception as e:
            raise Exception(f"Failed to get user info: {e}")
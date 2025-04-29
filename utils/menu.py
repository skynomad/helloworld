import streamlit as st

class Menu:
    def __init__(self):
        # 세션 상태에서 역할(role)이 초기화되지 않은 경우 기본값으로 None 설정
        if "role" not in st.session_state:
            st.session_state.role = None

    def set_role(self, role: str):
        """사용자의 역할을 세션 상태에 저장하는 콜백 함수"""
        st.session_state.role = role

    def authenticated_menu(self):
        """인증된 사용자(로그인된 사용자)를 위한 네비게이션 메뉴 렌더링"""
        with st.sidebar:
            # 사이드바에 헤더 추가
            st.markdown(f"### **Welcome.! {st.session_state.role}**")
            
            # 사용자 역할 표시
            st.markdown(f"**Name:** `{st.session_state.username.capitalize()}`")
            st.markdown(f"**Role:** `{st.session_state.role.capitalize()}`")
            st.markdown("---")  # 구분선을 추가하여 시각적으로 분리
            
            # 로그아웃 버튼
            # if st.button("🚪 Logout", key="logout"):
            #     st.session_state["token"] = None  # 토큰 초기화
            #     st.session_state["role"] = None  # 역할 초기화
            #     st.success("Logged out successfully!")  # 성공 메시지 표시
            #     st.experimental_rerun()  # 페이지 새로고침

            # st.markdown("---")  # 또 다른 구분선 추가
            
            # 네비게이션 링크
            st.markdown("### 📂 **Navigation**")
            st.markdown("🔄 [Switch Accounts](app.py)")  # 계정 전환
            st.markdown("👤 [Your Profile](pages/user.py)")  # 사용자 프로필
            
            # 역할에 따라 추가 메뉴 표시
            if st.session_state.role in ["admin"]:
                st.markdown("🛠️ [Manage Users](pages/admin.py)")  # 사용자 관리
            elif st.session_state.role in ["super-admin"]:
                st.markdown("🛠️ [Manage Users](pages/admin.py)")  # 사용자 관리
                st.markdown("🔑 [Manage Admin Access](pages/super-admin.py)")  # 관리자 접근 관리

    def unauthenticated_menu(self):
        """인증되지 않은 사용자(로그인하지 않은 사용자)를 위한 네비게이션 메뉴 렌더링"""
        with st.sidebar:
            st.markdown("### 🔒 **Please Log In**")  # 로그인 요청 메시지
            st.markdown("---")  # 구분선 추가

            st.markdown("🔑 [Log In](./)")  # 로그인 링크

    def render_menu(self):
        """사용자의 인증 상태에 따라 적절한 메뉴 렌더링"""
        if st.session_state.role is None:
            self.unauthenticated_menu()  # 인증되지 않은 사용자 메뉴 렌더링
        else:
            self.authenticated_menu()  # 인증된 사용자 메뉴 렌더링

    def render_menu_with_redirect(self):
        """인증되지 않은 사용자를 메인 페이지로 리디렉션하거나, 적절한 메뉴 렌더링"""
        self.render_menu()  # 메뉴 렌더링
        
        # 역할에 따라 페이지 리디렉션
        if st.session_state.role is None:
            st.switch_page("app.py")  # 메인 페이지로 리디렉션
        elif st.session_state.role in ["user"]:
            st.switch_page("pages/user.py")  # 사용자 페이지로 리디렉션
        elif st.session_state.role in ["admin"]:
            st.switch_page("pages/admin.py")  # 관리자 페이지로 리디렉션
        elif st.session_state.role in ["super-admin"]:
            st.switch_page("pages/super-admin.py")  # 슈퍼 관리자 페이지로 리디렉션
        else:
            st.error("Invalid role")  # 잘못된 역할에 대한 오류 메시지

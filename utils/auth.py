import streamlit as st

ROLES = ["doctor", "patient", "nurse", "lab_tech"]

def init_session():
    defaults = {
        "logged_in": False,
        "username": None,
        "role": None,
        "page": "landing",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def login(username: str, role: str):
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.role = role

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "landing"

def require_role(allowed_roles: list):
    """Call at the top of a page to enforce role-based access."""
    if not st.session_state.get("logged_in"):
        st.warning("Please sign in to access this page.")
        st.stop()
    if st.session_state.role not in allowed_roles:
        st.error(f"Access denied. This page is restricted to: {', '.join(allowed_roles)}.")
        st.stop()

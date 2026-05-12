import streamlit as st

ROLES = ["doctor", "patient", "nurse", "lab_tech"]

def init_session():
    defaults = {
        "logged_in": False,
        "username":  None,
        "role":      None,
        "page":      "landing",
        "_session_token": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Restore session from URL token on every fresh Streamlit load
    if not st.session_state.logged_in:
        token = st.query_params.get("s")
        if token:
            from utils.db import restore_session
            session = restore_session(token)
            if session:
                st.session_state.logged_in = True
                st.session_state.username  = session["username"]
                st.session_state.role      = session["role"]
                st.session_state._session_token = token
                # Honour the page stored in URL (e.g. doctor_portal)
                saved_page = st.query_params.get("page")
                if saved_page:
                    st.session_state.page = saved_page
            else:
                # Token expired or invalid — clear it from URL
                st.query_params.clear()

def login(username: str, role: str):
    from utils.db import create_session
    token = create_session(username, role)
    st.session_state.logged_in = True
    st.session_state.username  = username
    st.session_state.role      = role
    st.session_state._session_token = token
    # Write token to URL so the browser keeps it across reloads
    st.query_params["s"] = token

def logout():
    token = st.session_state.get("_session_token")
    if token:
        from utils.db import delete_session
        delete_session(token)
    st.session_state.logged_in = False
    st.session_state.username  = None
    st.session_state.role      = None
    st.session_state.page      = "landing"
    st.session_state._session_token = None
    st.query_params.clear()

def require_role(allowed_roles: list):
    """Call at the top of a page to enforce role-based access."""
    if not st.session_state.get("logged_in"):
        st.warning("Please sign in to access this page.")
        st.stop()
    if st.session_state.role not in allowed_roles:
        st.error(f"Access denied. This page is restricted to: {', '.join(allowed_roles)}.")
        st.stop()

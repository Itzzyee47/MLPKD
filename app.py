import streamlit as st
from utils.auth import init_session

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="MLPKD — Kidney Disease Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",   # collapsed by default on mobile
)

init_session()

# ── Global theme CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

/* Global font & background */
html, body, [class*="css"] {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background-color: #f7fdfb;
}

/* Fluid container — override Streamlit's narrow default */
.block-container, .stMainBlockContainer {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: max(1rem, 2vw) !important;
    padding-right: max(1rem, 2vw) !important;
    padding-bottom: 2rem !important;
}

/* ── Teal primary buttons ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0a8a74, #0fbfa0);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 0.55rem 1.4rem;
    font-weight: 700;
    font-size: 0.9rem;
    transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(10,138,116,0.3);
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0fbfa0, #0a8a74);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(10,138,116,0.4);
}
/* Secondary buttons */
div.stButton > button:not([kind="primary"]) {
    border-radius: 30px;
    border: 2px solid #0a8a74;
    color: #0a8a74;
    font-weight: 600;
    background: transparent;
    transition: all 0.2s;
}
div.stButton > button:not([kind="primary"]):hover {
    background: #e6faf6;
    transform: translateY(-1px);
}
/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #063d34 0%, #0a5c4e 60%, #0d7a67 100%);
}
section[data-testid="stSidebar"] * { color: #e0f5f1 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
section[data-testid="stSidebar"] div.stButton > button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #fff !important;
    border-radius: 10px !important;
    font-weight: 500;
    text-align: left;
    transition: all 0.2s;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(255,255,255,0.18) !important;
}
/* Inputs */
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
    border-radius: 10px !important;
    border: 1.5px solid #cde8e3 !important;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
    border-color: #0a8a74 !important;
    box-shadow: 0 0 0 3px rgba(10,138,116,0.12) !important;
}
/* Tabs */
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #0a8a74 !important;
    border-bottom: 3px solid #0a8a74 !important;
    font-weight: 700;
}
/* Metrics */
div[data-testid="metric-container"] {
    background: #fff;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-top: 3px solid #0a8a74;
}
div[data-testid="metric-container"] label { color: #6b7b78 !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #0a8a74 !important; font-weight: 800;
}
/* Expander */
details summary { color: #0a8a74 !important; font-weight: 600; }
/* Divider */
hr { border-color: #e0f0ed !important; }
/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ────────────────────────────────────────────
   MOBILE  < 640px
──────────────────────────────────────────── */
@media (max-width: 639px) {
    /* Stack Streamlit columns vertically */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    /* Metric cards: 2-per-row on phone */
    div[data-testid="metric-container"] {
        padding: 0.7rem 0.9rem;
    }
    /* Tabs: scrollable, don't shrink */
    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        white-space: nowrap;
        font-size: 0.82rem;
        padding: 0.5rem 0.8rem;
    }
    /* Forms: full-width inputs */
    div[data-testid="stTextInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"] {
        width: 100% !important;
    }
    /* Sidebar: full width overlay on mobile */
    section[data-testid="stSidebar"] {
        width: 80vw !important;
        min-width: unset !important;
    }
    /* Reduce heading sizes in portals */
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.05rem !important; }
    /* Button sizing */
    div.stButton > button {
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
    }
    /* Plotly charts: allow horizontal scroll */
    div[data-testid="stPlotlyChart"] {
        overflow-x: auto;
    }
}

/* ────────────────────────────────────────────
   TABLET  640px – 1023px
──────────────────────────────────────────── */
@media (min-width: 640px) and (max-width: 1023px) {
    div[data-testid="metric-container"] {
        padding: 0.8rem 1rem;
    }
    h1 { font-size: 1.9rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Lazy-import pages to avoid circular issues ─────────────────────────────
from pages import (
    landing, about, register, signin,
    doctor_portal, patient_portal, nurse_portal, labtech_portal,
    ml_prediction, patient_insights,
)

# ── Sidebar navigation ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:0.5rem 0 0.2rem 0;">
        <span style="font-size:2rem">🩺</span>
        <div>
            <div style="font-size:1.3rem;font-weight:800;color:#fff;letter-spacing:1px">MLPKD</div>
            <div style="font-size:0.72rem;color:rgba(255,255,255,0.6);letter-spacing:2px">KIDNEY AI PLATFORM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Public nav links
    if st.button("🏠  Home", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()
    if st.button("📖  About", use_container_width=True):
        st.session_state.page = "about"
        st.rerun()

    st.divider()

    if not st.session_state.logged_in:
        st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.5);letter-spacing:1.5px;margin-bottom:6px'>ACCOUNT</div>", unsafe_allow_html=True)
        if st.button("🔐  Sign In", use_container_width=True):
            st.session_state.page = "signin"
            st.rerun()
        if st.button("📋  Register", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    else:
        role = st.session_state.role
        uname = st.session_state.username
        role_icons = {"doctor": "🩺", "patient": "🧑", "nurse": "💉", "lab_tech": "🔬"}

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.10);border-radius:12px;padding:0.8rem 1rem;margin-bottom:0.5rem">
            <div style="font-size:1rem;font-weight:700;color:#fff">{role_icons.get(role,'')} {uname}</div>
            <div style="font-size:0.78rem;color:rgba(255,255,255,0.65);margin-top:2px">{role.replace('_',' ').title()}</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.5);letter-spacing:1.5px;margin-bottom:6px'>MY WORKSPACE</div>", unsafe_allow_html=True)

        portal_map = {
            "doctor":   ("🩺  Doctor Portal",   "doctor_portal"),
            "patient":  ("🧑  Patient Portal",  "patient_portal"),
            "nurse":    ("💉  Nurse Portal",     "nurse_portal"),
            "lab_tech": ("🔬  Lab Portal",       "labtech_portal"),
        }
        label, page_key = portal_map.get(role, ("My Portal", "landing"))
        if st.button(label, use_container_width=True):
            st.session_state.page = page_key
            st.rerun()

        if role == "doctor":
            if st.button("📈  ML Prediction", use_container_width=True):
                st.session_state.page = "ml_prediction"
                st.rerun()

        if role == "patient":
            if st.button("🔍  My Insights", use_container_width=True):
                st.session_state.page = "patient_insights"
                st.rerun()

        st.divider()
        if st.button("🚪  Sign Out", use_container_width=True):
            from utils.auth import logout
            logout()
            st.rerun()

# ── Page routing ───────────────────────────────────────────────────────────
PAGE_MAP = {
    "landing":          landing.show,
    "about":            about.show,
    "register":         register.show,
    "signin":           signin.show,
    "doctor_portal":    doctor_portal.show,
    "patient_portal":   patient_portal.show,
    "nurse_portal":     nurse_portal.show,
    "labtech_portal":   labtech_portal.show,
    "ml_prediction":    ml_prediction.show,
    "patient_insights": patient_insights.show,
}

page_fn = PAGE_MAP.get(st.session_state.page, landing.show)
page_fn()

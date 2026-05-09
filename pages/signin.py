import streamlit as st
from utils.db import authenticate
from utils.auth import login

ROLE_PORTAL = {
    "doctor": "doctor_portal",
    "patient": "patient_portal",
    "nurse": "nurse_portal",
    "lab_tech": "labtech_portal",
}

def show():
    st.markdown("""
    <style>
    *, *::before, *::after { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    #MainMenu, footer, header { visibility: hidden; }

    /* Push Streamlit's main block to the right half */
    .block-container, .stMainBlockContainer {
        margin-left: 50vw !important;
        max-width: 50vw !important;
        padding: 3rem 2.5rem 2rem !important;
        background: #fff;
        min-height: 100vh;
    }

    /* Hero panel fixed on the left half */
    .signin-hero {
        position: fixed;
        top: 0; left: 0;
        width: 50vw;
        height: 100vh;
        background: linear-gradient(135deg, #063d34 0%, #0a8a74 55%, #0fbfa0 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 2.5rem;
        text-align: center;
        overflow: hidden;
        z-index: 0;
    }
    .signin-hero::before {
        content: '';
        position: absolute;
        width: 320px; height: 320px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
        bottom: -100px; left: -100px;
    }
    .signin-hero::after {
        content: '';
        position: absolute;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
        top: -60px; right: -60px;
    }
    .signin-hero-content { position: relative; z-index: 2; }
    .signin-hero-icon {
        width: 100px; height: 100px;
        background: rgba(255,255,255,0.18);
        border: 3px solid rgba(255,255,255,0.35);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 3rem;
        margin: 0 auto 2rem;
    }
    .signin-hero h1 {
        color: #fff;
        font-size: 2.4rem; font-weight: 800;
        margin: 0 0 1rem; line-height: 1.2;
    }
    .signin-hero p {
        color: rgba(255,255,255,0.82);
        font-size: 1rem; line-height: 1.6;
        max-width: 280px; margin: 0 auto;
    }

    /* Form-area headers */
    .form-header h2 {
        color: #1a2e2b; font-size: 1.8rem;
        font-weight: 800; margin: 0 0 0.3rem;
    }
    .form-header p { color: #6b7b78; font-size: 0.9rem; margin: 0 0 2rem; }

    /* Streamlit input styling */
    div[data-testid="stTextInput"] label { font-size: 0.75rem !important; font-weight: 700 !important; letter-spacing: 1px !important; text-transform: uppercase; color: #6b7b78 !important; }
    div[data-testid="stTextInput"] input {
        padding: 0.8rem 1rem !important;
        border: 1.5px solid #e0e8e6 !important;
        border-radius: 8px !important;
        background: #f7fdfb !important;
        font-size: 0.95rem !important;
        color: #1a2e2b !important;
        transition: all 0.2s;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #0a8a74 !important;
        box-shadow: 0 0 0 3px rgba(10,138,116,0.12) !important;
        background: #fff !important;
    }

    /* Submit button */
    div.stForm button[kind="secondaryFormSubmit"],
    div.stForm button[data-testid="baseButton-secondaryFormSubmit"] {
        width: 100% !important;
        background: linear-gradient(135deg, #0a8a74, #0fbfa0) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        padding: 0.85rem !important;
        margin-top: 0.5rem;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(10,138,116,0.25) !important;
        transition: all 0.2s;
    }
    div.stForm button[kind="secondaryFormSubmit"]:hover,
    div.stForm button[data-testid="baseButton-secondaryFormSubmit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(10,138,116,0.35) !important;
    }

    /*  Demo creds box */
    .demo-creds {
        margin-top: 2rem; padding: 1rem 1.2rem;
        background: #f7fdfb;
        border-radius: 8px;
        border-left: 4px solid #0a8a74;
    }
    .demo-creds h4 { color: #1a2e2b; margin: 0 0 0.6rem; font-size: 0.88rem; }
    .demo-creds p  { color: #4a6a65; font-size: 0.82rem; margin: 0.3rem 0; font-family: monospace; }

    /* Responsive */
    @media (max-width: 768px) {
        .signin-hero { display: none; }
        .block-container, .stMainBlockContainer {
            margin-left: 0 !important;
            max-width: 100% !important;
            padding: 2rem 1.2rem !important;
        }
    }
    </style>

    <div class="signin-hero">
        <div class="signin-hero-content">
            <div class="signin-hero-icon">🔐</div>
            <h1>Welcome Back</h1>
            <p>Sign in to access your MLPKD medical dashboard and AI-powered kidney predictions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Right-panel content (native Streamlit)
    st.markdown('<div class="form-header"><h2>Sign In</h2><p>Access your account</p></div>', unsafe_allow_html=True)

    with st.form(key="signin_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    if submitted:
        if username.strip() and password:
            ok, user = authenticate(username.strip(), password)
            if ok:
                login(username.strip(), user["role"])
                st.success(f" Welcome, {user['name']}!")
                import time; time.sleep(0.8)
                st.session_state.page = ROLE_PORTAL[user["role"]]
                st.rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter your username and password.")

    st.markdown("""
    <div class="demo-creds">
        <h4>🔑 Demo Credentials</h4>
        <p><strong>Doctor:</strong> dr_john / doc123</p>
        <p><strong>Nurse:</strong> nurse_amy / nur123</p>
        <p><strong>Lab Tech:</strong> lab_kai / lab123</p>
        <p><strong>Patient:</strong> patient_bob / pat123</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("â† Back to Home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        if st.button("Create Account â†’", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

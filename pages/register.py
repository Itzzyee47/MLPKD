import streamlit as st
from utils.db import register_user

ROLE_OPTIONS = {
    "patient": "Patient",
    "nurse": "Nurse", 
    "lab_tech": "Lab Technician",
    "doctor": "Doctor"
}

def show():
    st.markdown("""
    <style>
    *, *::before, *::after { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; height: 100%; }
    .block-container, .stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }
    .main { background: #fff; padding: 0 !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    
    .register-layout {
        display: flex;
        min-height: 100vh;
        background: #fff;
    }
    
    .register-hero {
        flex: 1;
        background: linear-gradient(135deg, #063d34 0%, #0a8a74 50%, #0fbfa0 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .register-hero::before {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        bottom: -100px;
        left: -100px;
    }
    
    .register-hero::after {
        content: '';
        position: absolute;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
        top: -50px;
        right: -50px;
    }
    
    .register-hero-content {
        position: relative;
        z-index: 2;
    }
    
    .register-icon {
        width: 100px;
        height: 100px;
        background: rgba(255,255,255,0.2);
        border: 3px solid rgba(255,255,255,0.4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: #fff;
        margin: 0 auto 2rem;
    }
    
    .register-hero h1 {
        color: #fff;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 1rem;
        line-height: 1.2;
    }
    
    .register-hero p {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin: 0;
        line-height: 1.6;
        max-width: 300px;
    }
    
    .register-form-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding: 3rem 2rem;
        overflow-y: auto;
        background: #fff;
    }
    
    .register-form-box {
        width: 100%;
        max-width: 400px;
        margin-top: 2rem;
    }
    
    .register-title {
        color: #1a2e2b;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0 0 0.5rem;
        padding: 0;
    }
    
    .register-subtitle {
        color: #6b7b78;
        font-size: 0.9rem;
        margin: 0 0 2rem;
        padding: 0;
    }
    
    .html-form {
        width: 100%;
    }
    
    .form-group {
        margin-bottom: 1.2rem;
    }
    
    .field-label {
        display: block;
        color: #6b7b78;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    
    .form-input,
    .form-select {
        width: 100%;
        padding: 0.85rem 1rem;
        border: 1px solid #e0e8e6;
        border-radius: 6px;
        background: #f7fdfb;
        font-size: 0.95rem;
        color: #1a2e2b;
        font-family: inherit;
        transition: all 0.2s;
        box-sizing: border-box;
    }
    
    .form-input::placeholder,
    .form-select::placeholder {
        color: #999;
    }
    
    .form-input:focus,
    .form-select:focus {
        outline: none;
        border-color: #0a8a74;
        background: #fff;
        box-shadow: 0 0 0 3px rgba(10,138,116,0.1);
    }
    
    .field-hint {
        font-size: 0.8rem;
        color: #6b7b78;
        margin-top: 0.4rem;
        display: block;
    }
    
    .form-button {
        width: 100%;
        padding: 0.95rem 1.5rem;
        background: linear-gradient(135deg, #0a8a74 0%, #0fbfa0 100%);
        color: #fff;
        border: none;
        border-radius: 6px;
        font-size: 0.95rem;
        font-weight: 700;
        cursor: pointer;
        margin-top: 1.8rem;
        box-shadow: 0 4px 14px rgba(10,138,116,0.2);
        transition: all 0.2s;
    }
    
    .form-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(10,138,116,0.3);
    }
    
    .form-alert {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    
    .form-alert.error {
        background: #fef2f2;
        color: #991b1b;
        border-left: 4px solid #dc2626;
    }
    
    .form-alert.success {
        background: #f0fdf4;
        color: #166534;
        border-left: 4px solid #22c55e;
    }
    
    .signin-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7b78;
        font-size: 0.9rem;
    }
    
    .signin-link a {
        color: #0a8a74;
        font-weight: 700;
        text-decoration: none;
        cursor: pointer;
        transition: color 0.2s;
    }
    
    .signin-link a:hover {
        color: #0fbfa0;
    }
    
    /* Hide Streamlit form completely */
    div.stForm {
        display: none !important;
        visibility: hidden !important;
    }
    
    @media (max-width: 768px) {
        .register-layout {
            flex-direction: column;
        }
        
        .register-hero {
            min-height: 50vh;
            padding: 2rem 1.5rem;
        }
        
        .register-hero h1 {
            font-size: 2rem;
        }
        
        .register-form-area {
            padding: 2rem 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .register-hero {
            padding: 1.5rem 1rem;
            min-height: 45vh;
        }
        
        .register-icon {
            width: 80px;
            height: 80px;
            font-size: 2.5rem;
        }
        
        .register-hero h1 {
            font-size: 1.6rem;
        }
        
        .register-form-area {
            padding: 1.5rem 1rem;
        }
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
    
    # ─ Initialize alert state
    if 'register_alert' not in st.session_state:
        st.session_state.register_alert = None
    
    # Render the ENTIRE page (HTML + form + JavaScript) in ONE markdown call to preserve layout
    st.markdown('''
    <div class="register-layout">
        <div class="register-hero">
            <div class="register-hero-content">
                <div class="register-icon">✓</div>
                <h1>Join MLPKD</h1>
                <p>To use all features of the application and access AI-powered kidney disease predictions.</p>
            </div>
        </div>
        <div class="register-form-area">
            <div class="register-form-box">
                <h2 class="register-title">Sign up</h2>
                <p class="register-subtitle">Create your account to get started</p>
                <form id="htmlRegisterForm" class="html-form">
                    <div class="form-group">
                        <label class="field-label">Full Name</label>
                        <input type="text" id="html_name" class="form-input" placeholder="e.g. Dr. Jane Doe" required>
                    </div>
                    <div class="form-group">
                        <label class="field-label">Username</label>
                        <input type="text" id="html_username" class="form-input" placeholder="Choose your username" required>
                    </div>
                    <div class="form-group">
                        <label class="field-label">Email</label>
                        <input type="email" id="html_email" class="form-input" placeholder="your.email@example.com" required>
                    </div>
                    <div class="form-group">
                        <label class="field-label">Role</label>
                        <select id="html_role" class="form-select" required>
                            <option value="">Select your role</option>
                            <option value="patient">Patient</option>
                            <option value="nurse">Nurse</option>
                            <option value="lab_tech">Lab Technician</option>
                            <option value="doctor">Doctor</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="field-label">Password</label>
                        <input type="password" id="html_password" class="form-input" placeholder="At least 6 characters" required>
                        <span class="field-hint">Minimum 6 characters</span>
                    </div>
                    <div class="form-group">
                        <label class="field-label">Confirm Password</label>
                        <input type="password" id="html_confirm" class="form-input" placeholder="Re-enter your password" required>
                    </div>
                    <button type="submit" class="form-button" id="htmlSubmitBtn">Create Account</button>
                </form>
                <div id="alertBox"></div>
                <div class="signin-link">
                    Already have an account? <a onclick="handlePageChange('signin')">Log in</a>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function handlePageChange(page) {
        const url = new URL(window.location);
        url.searchParams.set('page', page);
        window.location.href = url.toString();
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('htmlRegisterForm');
        const alertBox = document.getElementById('alertBox');
        
        if (!form) {
            console.error('Form not found');
            return;
        }
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('html_name').value.trim();
            const username = document.getElementById('html_username').value.trim();
            const email = document.getElementById('html_email').value.trim();
            const role = document.getElementById('html_role').value;
            const password = document.getElementById('html_password').value;
            const confirm = document.getElementById('html_confirm').value;
            
            if (!name || !username || !email || !role || !password || !confirm) {
                showAlert('All fields are required.', 'error');
                return;
            }
            
            if (password !== confirm) {
                showAlert('Passwords do not match.', 'error');
                return;
            }
            
            if (password.length < 6) {
                showAlert('Password must be at least 6 characters.', 'error');
                return;
            }
            
            const formData = {
                name: name,
                username: username,
                email: email,
                role: role,
                password: password
            };
            
            showAlert('Creating account...', 'success');
            
            // Find and populate the hidden Streamlit input fields
            const textInputs = document.querySelectorAll('input[type="text"]');
            const passwordInputs = document.querySelectorAll('input[type="password"]');
            const selects = document.querySelectorAll('select');
            
            // Find the inputs in the hidden Streamlit form (skip our visible ones)
            let stNameInput = null;
            let stUsernameInput = null;
            let stEmailInput = null;
            let stPasswordInput = null;
            let stConfirmInput = null;
            let stRoleSelect = null;
            
            textInputs.forEach(input => {
                if (input.id !== 'html_name' && input.id !== 'html_username' && input.id !== 'html_email') {
                    if (!stNameInput && input.placeholder !== 'Choose your username' && input.placeholder !== 'your.email@example.com') {
                        stNameInput = input;
                    } else if (!stUsernameInput && !stNameInput) {
                        stUsernameInput = input;
                    } else if (!stEmailInput && !stNameInput && !stUsernameInput) {
                        stEmailInput = input;
                    }
                }
            });
            
            passwordInputs.forEach(input => {
                if (input.id !== 'html_password' && input.id !== 'html_confirm') {
                    if (!stPasswordInput && !input.value) {
                        stPasswordInput = input;
                    } else if (!stConfirmInput && stPasswordInput && !input.value) {
                        stConfirmInput = input;
                    }
                }
            });
            
            selects.forEach(select => {
                if (select.id !== 'html_role' && !select.value) {
                    stRoleSelect = select;
                }
            });
            
            // Set values on the hidden Streamlit inputs
            if (stNameInput) {
                stNameInput.value = name;
                stNameInput.dispatchEvent(new Event('input', { bubbles: true }));
                stNameInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (stUsernameInput) {
                stUsernameInput.value = username;
                stUsernameInput.dispatchEvent(new Event('input', { bubbles: true }));
                stUsernameInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (stEmailInput) {
                stEmailInput.value = email;
                stEmailInput.dispatchEvent(new Event('input', { bubbles: true }));
                stEmailInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (stPasswordInput) {
                stPasswordInput.value = password;
                stPasswordInput.dispatchEvent(new Event('input', { bubbles: true }));
                stPasswordInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (stConfirmInput) {
                stConfirmInput.value = confirm;
                stConfirmInput.dispatchEvent(new Event('input', { bubbles: true }));
                stConfirmInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (stRoleSelect) {
                stRoleSelect.value = role;
                stRoleSelect.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Trigger the hidden Streamlit form submit button
            const streamlitBtns = document.querySelectorAll('div.stForm button[type="submit"]');
            if (streamlitBtns.length > 0) {
                setTimeout(() => {
                    streamlitBtns[0].click();
                }, 300);
            }
        });
        
        function showAlert(message, type) {
            const icon = type === 'error' ? '❌' : '✓';
            alertBox.innerHTML = '<div class="form-alert ' + type + '">' + icon + ' ' + message + '</div>';
        }
    });
    </script>
    ''', unsafe_allow_html=True)
    
    # ─ Hidden Streamlit form that processes the data
    with st.form(key="register_form_backend", clear_on_submit=False):
        name = st.text_input("Name", value="", label_visibility="collapsed", key="st_name")
        username = st.text_input("Username", value="", label_visibility="collapsed", key="st_username")
        email = st.text_input("Email", value="", label_visibility="collapsed", key="st_email")
        role = st.selectbox("Role", list(ROLE_OPTIONS.keys()), label_visibility="collapsed", key="st_role")
        password = st.text_input("Password", value="", type="password", label_visibility="collapsed", key="st_password")
        confirm = st.text_input("Confirm", value="", type="password", label_visibility="collapsed", key="st_confirm")
        
        submitted = st.form_submit_button("Submit", key="st_submit_hidden")
    
    # Process form submission
    if submitted:
        # Get data from session state
        form_name = st.session_state.get('st_name', '').strip()
        form_username = st.session_state.get('st_username', '').strip()
        form_password = st.session_state.get('st_password', '')
        form_role = st.session_state.get('st_role', '')
        
        if form_name and form_username and form_password and form_role:
            success, msg = register_user(form_username, form_password, form_role, form_name)
            if success:
                st.success(f"✓ {msg} Redirecting to sign in...")
                import time
                time.sleep(1.5)
                st.session_state.page = 'signin'
                st.rerun()
            else:
                st.error(f"❌ {msg}")
    
    # Navigation buttons
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Sign In", use_container_width=True):
            st.session_state.page = "signin"
            st.rerun()
    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

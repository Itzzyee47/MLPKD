import streamlit as st
from utils.auth import require_role, logout
from utils.db import get_users, get_profile, upsert_profile, update_user

_CSS = """
<style>
.portal-banner {
    background: linear-gradient(135deg, #063d34 0%, #0a8a74 55%, #0fbfa0 100%);
    border-radius: 20px; padding: 2rem 2.5rem; color: #fff;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
}
.portal-banner::before {
    content:''; position:absolute; width:240px; height:240px;
    background:rgba(255,255,255,0.07); border-radius:50%; bottom:-70px; right:100px;
}
.portal-banner::after {
    content:''; position:absolute; width:150px; height:150px;
    background:rgba(255,255,255,0.05); border-radius:50%; top:-40px; right:20px;
}
.banner-inner { position:relative; z-index:2; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
.banner-tag { background:rgba(255,255,255,0.18); border-radius:20px; display:inline-block; padding:0.25rem 0.9rem; font-size:0.75rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.6rem; }
.banner-inner h2 { margin:0 0 0.4rem; font-size:1.7rem; font-weight:800; }
.banner-inner p { margin:0; color:rgba(255,255,255,0.82); font-size:0.95rem; }
.banner-icon { font-size:4.5rem; opacity:0.9; flex-shrink:0; }
.stat-card { background:#fff; border-radius:16px; padding:1.2rem 1.4rem; box-shadow:0 2px 16px rgba(10,138,116,0.08); border-top:4px solid #0a8a74; }
.stat-icon { font-size:1.8rem; margin-bottom:0.5rem; }
.stat-label { color:#6b7b78; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.9px; margin-bottom:0.3rem; }
.stat-value { color:#1a2e2b; font-size:1.9rem; font-weight:800; margin-bottom:0.2rem; line-height:1; }
.stat-trend { font-size:0.76rem; font-weight:600; }
.trend-up { color:#0a8a74; } .trend-neutral { color:#6b7b78; }
.section-card { background:#fff; border-radius:16px; padding:1.4rem 1.6rem; box-shadow:0 2px 16px rgba(0,0,0,0.05); margin-bottom:1rem; }
.section-card h4 { color:#1a2e2b; font-size:1rem; font-weight:700; margin:0 0 1rem; padding-bottom:0.6rem; border-bottom:2px solid #e8f5f2; }
.ref-row { display:flex; justify-content:space-between; align-items:center; padding:0.55rem 0.8rem; border-radius:8px; background:#f7fdfb; margin-bottom:0.4rem; }
.ref-name { font-size:0.82rem; color:#6b7b78; font-weight:600; }
.ref-range { font-size:0.82rem; color:#1a2e2b; font-weight:700; }
.file-item { display:flex; align-items:center; gap:0.8rem; padding:0.8rem 1rem; border-radius:10px; background:#f7fdfb; margin-bottom:0.5rem; border-left:3px solid #0a8a74; }
.file-icon { font-size:1.4rem; }
.file-name { font-weight:700; color:#1a2e2b; font-size:0.88rem; }
.file-size { font-size:0.75rem; color:#6b7b78; }
</style>
"""

def show():
    require_role(["lab_tech"])
    db = get_users()
    user = db.get(st.session_state.username, {})
    name = user.get("name", st.session_state.username)
    patients = {u: d for u, d in db.items() if d["role"] == "patient"}
    patient_names = {d["name"]: u for u, d in patients.items()}

    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Welcome banner ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="portal-banner">
        <div class="banner-inner">
            <div>
                <div class="banner-tag">Lab Dashboard</div>
                <h2>Welcome, {name}! 🔬</h2>
                <p>Submit kidney function panels, upload reports, and view patient lab data.</p>
            </div>
            <div class="banner-icon">🔬</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat cards ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">👥</div>
        <div class="stat-label">Patients</div>
        <div class="stat-value">{len(patients)}</div>
        <div class="stat-trend trend-up">↑ On record</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown("""<div class="stat-card" style="border-color:#0fbfa0">
        <div class="stat-icon">🧪</div>
        <div class="stat-label">Tests Run</div>
        <div class="stat-value">—</div>
        <div class="stat-trend trend-neutral">This session</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown("""<div class="stat-card" style="border-color:#6b7b78">
        <div class="stat-icon">🏥</div>
        <div class="stat-label">Department</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.4rem">Clinical Lab</div>
        <div class="stat-trend trend-neutral">Nephrology unit</div>
    </div>""", unsafe_allow_html=True)
    c4.markdown("""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">📁</div>
        <div class="stat-label">Reports</div>
        <div class="stat-value">—</div>
        <div class="stat-trend trend-neutral">Uploaded</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏠  Overview", "🧪  Submit Results", "👤  My Profile"])

    with tab1:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown('<div class="section-card"><h4>👥 Patient Overview</h4>', unsafe_allow_html=True)
            if patients:
                for uname, data in patients.items():
                    preds = data.get("data", {}).get("predictions", [])
                    last_r = preds[-1].get("result", "—") if preds else "No data"
                    badge_c = "#e53e3e" if last_r == "CKD" else ("#0a8a74" if last_r == "Not CKD" else "#6b7b78")
                    st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;
                        padding:0.8rem 1rem;border-radius:10px;background:#f7fdfb;margin-bottom:0.6rem;border-left:3px solid #0a8a74">
                        <div>
                            <div style="font-weight:700;color:#1a2e2b;font-size:0.9rem">🧑 {data['name']}</div>
                            <div style="color:#6b7b78;font-size:0.78rem;margin-top:2px">@{uname} · {len(preds)} prediction(s)</div>
                        </div>
                        <span style="background:{badge_c}22;color:{badge_c};font-size:0.75rem;font-weight:700;padding:0.2rem 0.8rem;border-radius:20px">{last_r}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("No patients registered yet.")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-card"><h4>📁 Health Reports Document</h4>', unsafe_allow_html=True)
            # Simulated report list (as in the reference image)
            reports = [
                ("📄", "Medical Check Up Report.pdf", "2 Mb"),
                ("📑", "Blood Count Report.docs", "4 Mb"),
                ("📑", "Glucose Level Report.docs", "12 Mb"),
                ("📄", "Heart Rate Report.pdf", "2.5 Mb"),
            ]
            for icon, fname, size in reports:
                st.markdown(f"""<div class="file-item">
                    <span class="file-icon">{icon}</span>
                    <div style="flex:1"><div class="file-name">{fname}</div><div class="file-size">{size}</div></div>
                    <span style="color:#6b7b78;font-size:1.1rem;cursor:pointer;margin:0 0.4rem">🗑</span>
                    <span style="color:#0a8a74;font-size:1.1rem;cursor:pointer">⬇</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("""<div class="section-card"><h4>📏 Normal Reference Ranges</h4>
            <div class="ref-row"><span class="ref-name">Serum Creatinine</span><span class="ref-range">0.6–1.2 mg/dL</span></div>
            <div class="ref-row"><span class="ref-name">Blood Urea</span><span class="ref-range">7–25 mg/dL</span></div>
            <div class="ref-row"><span class="ref-name">Hemoglobin</span><span class="ref-range">12–17 g/dL</span></div>
            <div class="ref-row"><span class="ref-name">Albumin</span><span class="ref-range">3.5–5.0 g/dL</span></div>
            <div class="ref-row"><span class="ref-name">Specific Gravity</span><span class="ref-range">1.005–1.025</span></div>
            <div class="ref-row"><span class="ref-name">Sodium</span><span class="ref-range">135–145 mEq/L</span></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("""<div class="section-card"><h4>⚡ Quick Guide</h4>
            <div style="font-size:0.85rem;color:#4a6a65;line-height:1.8">
            🔬 <b>Creatinine ↑</b> — kidney filtration impaired<br>
            💧 <b>Urea ↑</b> — protein metabolism or renal failure<br>
            🩸 <b>Hemo ↓</b> — anaemia common in CKD<br>
            🧬 <b>Albumin ↓</b> — protein loss via kidneys<br>
            🧪 <b>Sp.Gravity ↓</b> — dilute urine, kidney dysfunction
            </div></div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><h4>🧪 Kidney Function Panel</h4>', unsafe_allow_html=True)
        if not patient_names:
            st.info("No patients registered yet.")
        else:
            selected = st.selectbox("Select Patient", list(patient_names.keys()))

            st.markdown("**Kidney Function Markers**")
            col1, col2, col3 = st.columns(3)
            creatinine = col1.number_input("Serum Creatinine (mg/dL)", 0.1, 20.0, 1.2, step=0.1)
            urea = col2.number_input("Blood Urea (mg/dL)", 5.0, 200.0, 30.0, step=1.0)
            hemo = col3.number_input("Hemoglobin (g/dL)", 3.0, 20.0, 13.5, step=0.1)

            st.markdown("**Other Markers**")
            col4, col5, col6 = st.columns(3)
            albumin = col4.number_input("Albumin (g/dL)", 1.0, 6.0, 4.0, step=0.1)
            sg = col5.number_input("Specific Gravity", 1.000, 1.030, 1.015, step=0.001, format="%.3f")
            sodium = col6.number_input("Sodium (mEq/L)", 100.0, 160.0, 137.0, step=1.0)

            st.markdown("**Upload Report (optional)**")
            uploaded = st.file_uploader("Upload Lab Report (PDF/CSV)", type=["pdf", "csv"], label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📤  Submit Lab Results", type="primary", use_container_width=False):
                flags = []
                if not (0.6 <= creatinine <= 1.2): flags.append(f"⚠️ Creatinine ({creatinine}) out of range")
                if not (7 <= urea <= 25): flags.append(f"⚠️ Urea ({urea}) out of range")
                if not (12 <= hemo <= 17): flags.append(f"⚠️ Hemoglobin ({hemo}) out of range")
                if not (3.5 <= albumin <= 5.0): flags.append(f"⚠️ Albumin ({albumin}) out of range")

                st.success(f"✓ Lab results submitted for **{selected}**.")
                if uploaded:
                    st.info(f"📁 File uploaded: {uploaded.name}")
                for f in flags:
                    st.warning(f)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        profile = get_profile(st.session_state.username)
        st.markdown('<div class="section-card"><h4>👤 My Profile</h4>', unsafe_allow_html=True)

        st.markdown("**Account Information**")
        with st.form(key="labtech_account_form"):
            col_a1, col_a2 = st.columns(2)
            acc_name     = col_a1.text_input("Display Name", value=name)
            acc_username = col_a2.text_input("Username", value=st.session_state.username)
            col_a3, col_a4 = st.columns(2)
            acc_pw  = col_a3.text_input("New Password (leave blank to keep current)", type="password")
            acc_pw2 = col_a4.text_input("Confirm New Password", type="password")
            acc_saved = st.form_submit_button("💾  Save Account Info", type="primary", use_container_width=True)
        if acc_saved:
            new_u = acc_username.strip()
            new_n = acc_name.strip()
            if not new_u:
                st.error("Username cannot be empty.")
            elif not new_n:
                st.error("Display name cannot be empty.")
            elif acc_pw and acc_pw != acc_pw2:
                st.error("Passwords do not match.")
            else:
                ok, msg = update_user(st.session_state.username, new_u, new_n, acc_pw or None)
                if ok:
                    st.session_state.username = new_u
                    st.success(f"✓ {msg}")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("---")
        st.markdown("**Extended Profile**")
        with st.form(key="labtech_profile_form"):
            col1, col2 = st.columns(2)
            pf_email = col1.text_input("Email",  value=profile.get("email", ""))
            pf_phone = col2.text_input("Phone",  value=profile.get("phone", ""))
            col3, col4 = st.columns(2)
            pf_sex   = col3.selectbox("Sex", ["Prefer not to say","Male","Female","Other"],
                          index=["Prefer not to say","Male","Female","Other"].index(profile.get("sex", "Prefer not to say")))
            pf_dob   = col4.text_input("Date of Birth (YYYY-MM-DD)", value=profile.get("dob", "") or "")
            col5, col6 = st.columns(2)
            pf_dept  = col5.text_input("Department",    value=profile.get("department", ""))
            pf_lic   = col6.text_input("Lab Reg. No.",  value=profile.get("license_no", ""))
            pf_loc   = st.text_input("Location / City", value=profile.get("location", ""))
            pf_addr  = st.text_area("Address",          value=profile.get("address", ""), height=70)
            saved = st.form_submit_button("💾  Save Profile", type="primary", use_container_width=True)
        if saved:
            upsert_profile(st.session_state.username, {
                "email":      pf_email.strip() or None,
                "phone":      pf_phone.strip() or None,
                "sex":        pf_sex,
                "dob":        pf_dob.strip() or None,
                "department": pf_dept.strip() or None,
                "license_no": pf_lic.strip() or None,
                "location":   pf_loc.strip() or None,
                "address":    pf_addr.strip() or None,
            })
            st.success("✓ Profile updated.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col_so, _ = st.columns([1, 5])
    with col_so:
        if st.button("🚪  Sign Out", use_container_width=True):
            logout()
            st.rerun()

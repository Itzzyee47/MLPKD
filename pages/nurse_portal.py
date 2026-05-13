import streamlit as st
from utils.auth import require_role, logout
from utils.db import get_users, register_user, add_vitals, get_vitals, get_profile, upsert_profile

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
.vital-item { display:flex; align-items:center; gap:0.8rem; padding:0.7rem 1rem; background:#f7fdfb; border-radius:10px; margin-bottom:0.5rem; border-left:3px solid #0a8a74; }
.vital-label { color:#6b7b78; font-size:0.82rem; font-weight:600; flex:1; }
.vital-value { color:#1a2e2b; font-weight:800; font-size:0.95rem; }
</style>
"""

def show():
    require_role(["nurse"])
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
                <div class="banner-tag">Nurse Dashboard</div>
                <h2>Welcome, {name}! 💉</h2>
                <p>Record patient vitals, monitor health metrics, and submit care notes.</p>
            </div>
            <div class="banner-icon">💉</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat cards ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">👥</div>
        <div class="stat-label">Patients</div>
        <div class="stat-value">{len(patients)}</div>
        <div class="stat-trend trend-up">↑ Registered</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown("""<div class="stat-card" style="border-color:#0fbfa0">
        <div class="stat-icon">📋</div>
        <div class="stat-label">Vitals Forms</div>
        <div class="stat-value">—</div>
        <div class="stat-trend trend-neutral">This session</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown("""<div class="stat-card" style="border-color:#6b7b78">
        <div class="stat-icon">🏥</div>
        <div class="stat-label">Ward</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.4rem">Nephrology</div>
        <div class="stat-trend trend-neutral">Active shift</div>
    </div>""", unsafe_allow_html=True)
    c4.markdown("""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">⏰</div>
        <div class="stat-label">Shift</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.4rem">Day</div>
        <div class="stat-trend trend-neutral">08:00 – 20:00</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠  Overview", "📋  Record Vitals", "📝  Care Notes", "➕  Add Patient", "👤  My Profile"])

    with tab1:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown('<div class="section-card"><h4>👥 Patient List</h4>', unsafe_allow_html=True)
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

        with col_right:
            st.markdown(f"""<div class="section-card"><h4>👤 My Profile</h4>
            <div style="text-align:center;padding:1rem 0">
                <div style="width:72px;height:72px;background:linear-gradient(135deg,#0a8a74,#0fbfa0);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 0.8rem">💉</div>
                <div style="font-weight:800;color:#1a2e2b;font-size:1rem">{name}</div>
                <div style="color:#6b7b78;font-size:0.82rem;margin-top:2px">@{st.session_state.username}</div>
                <div style="margin-top:0.8rem;background:#e6faf6;color:#0a8a74;display:inline-block;
                    padding:0.25rem 1rem;border-radius:20px;font-size:0.78rem;font-weight:700">Nurse · Nephrology Ward</div>
            </div></div>""", unsafe_allow_html=True)

            st.markdown("""<div class="section-card"><h4>⚠️ Reference Ranges</h4>
            <div class="vital-item"><span class="vital-label">Blood Pressure</span><span class="vital-value">90–120 mmHg</span></div>
            <div class="vital-item"><span class="vital-label">Heart Rate</span><span class="vital-value">60–100 bpm</span></div>
            <div class="vital-item"><span class="vital-label">Temperature</span><span class="vital-value">36.5–37.5 °C</span></div>
            <div class="vital-item"><span class="vital-label">SpO2</span><span class="vital-value">&gt; 95%</span></div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><h4>📋 Record Patient Vitals</h4>', unsafe_allow_html=True)
        if not patient_names:
            st.info("No patients registered yet.")
        else:
            selected = st.selectbox("Select Patient", list(patient_names.keys()))
            col1, col2, col3 = st.columns(3)
            bp = col1.number_input("Blood Pressure (mmHg)", 60, 200, 120)
            hr = col2.number_input("Heart Rate (bpm)", 40, 200, 72)
            temp = col3.number_input("Temperature (°C)", 35.0, 42.0, 37.0, step=0.1)
            col4, col5, col6 = st.columns(3)
            weight = col4.number_input("Weight (kg)", 20.0, 200.0, 70.0, step=0.5)
            spo2 = col5.number_input("SpO2 (%)", 85, 100, 98)
            resp = col6.number_input("Resp. Rate (/min)", 10, 40, 16)

            st.markdown("<br>", unsafe_allow_html=True)
            vitals_note = st.text_input("Nurse note (optional)", placeholder="e.g. Patient appears anxious")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾  Save Vitals", type="primary", use_container_width=False):
                alerts = []
                if not (90 <= bp <= 120): alerts.append(f"⚠️ BP ({bp} mmHg) out of normal range")
                if not (60 <= hr <= 100): alerts.append(f"⚠️ HR ({hr} bpm) out of normal range")
                if not (36.5 <= temp <= 37.5): alerts.append(f"⚠️ Temp ({temp}°C) out of normal range")
                if spo2 < 95: alerts.append(f"⚠️ SpO2 ({spo2}%) below normal")
                add_vitals(
                    patient_username=patient_names[selected],
                    recorded_by=st.session_state.username,
                    reading={
                        "bp": bp, "heart_rate": hr, "temperature": temp,
                        "weight": weight, "spo2": spo2, "respiratory_rate": resp,
                        "notes": vitals_note.strip() or None,
                    }
                )
                st.success(f"✓ Vitals saved for **{selected}**.")
                for a in alerts:
                    st.warning(a)

            # ── Vitals history for selected patient ─────────────────────
            if patient_names:
                st.markdown("---")
                st.markdown("**📜 Vitals History**")
                history = get_vitals(patient_names[selected])
                if not history:
                    st.info("No vitals recorded yet for this patient.")
                else:
                    import pandas as pd
                    df = pd.DataFrame(history)
                    df = df.rename(columns={
                        "recorded_at": "Date/Time", "recorded_by": "Nurse",
                        "bp": "BP (mmHg)", "heart_rate": "HR (bpm)",
                        "temperature": "Temp (°C)", "weight": "Weight (kg)",
                        "spo2": "SpO2 (%)", "respiratory_rate": "RR (/min)",
                        "notes": "Note",
                    })
                    st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-card"><h4>📝 Care Notes</h4>', unsafe_allow_html=True)
        note = st.text_area("Observation / Care note:", placeholder="Enter patient observations, interventions, follow-up actions...", height=180, label_visibility="collapsed")
        col_b1, col_b2, _ = st.columns([1, 1, 4])
        with col_b1:
            if st.button("💾  Submit Note", type="primary", use_container_width=True):
                if note.strip():
                    st.success("✓ Note submitted successfully.")
                else:
                    st.warning("Note cannot be empty.")
        with col_b2:
            if st.button("🗑  Clear", use_container_width=True):
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="section-card"><h4>➕ Register New Patient</h4>', unsafe_allow_html=True)
        with st.form(key="add_patient_form", clear_on_submit=True):
            p_name     = st.text_input("Full Name", placeholder="e.g. Jane Doe")
            p_username = st.text_input("Username", placeholder="e.g. jane_doe (used to log in)")
            col_p1, col_p2 = st.columns(2)
            p_password  = col_p1.text_input("Password", type="password", placeholder="Minimum 6 characters")
            p_password2 = col_p2.text_input("Confirm Password", type="password", placeholder="Repeat password")
            submitted = st.form_submit_button("Register Patient", type="primary", use_container_width=True)

        if submitted:
            if not p_name.strip():
                st.error("Full name is required.")
            elif not p_username.strip():
                st.error("Username is required.")
            elif len(p_password) < 6:
                st.error("Password must be at least 6 characters.")
            elif p_password != p_password2:
                st.error("Passwords do not match.")
            else:
                ok, msg = register_user(p_username.strip(), p_password, "patient", p_name.strip())
                if ok:
                    st.success(f"✓ Patient **{p_name.strip()}** registered successfully. They can now sign in with username `{p_username.strip()}`.")
                else:
                    st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        profile = get_profile(st.session_state.username)
        st.markdown('<div class="section-card"><h4>👤 My Profile</h4>', unsafe_allow_html=True)
        with st.form(key="nurse_profile_form"):
            col1, col2 = st.columns(2)
            pf_email  = col1.text_input("Email",    value=profile.get("email", ""))
            pf_phone  = col2.text_input("Phone",    value=profile.get("phone", ""))
            col3, col4 = st.columns(2)
            pf_sex    = col3.selectbox("Sex", ["Prefer not to say","Male","Female","Other"],
                          index=["Prefer not to say","Male","Female","Other"].index(profile.get("sex", "Prefer not to say")))
            pf_dob    = col4.text_input("Date of Birth (YYYY-MM-DD)", value=profile.get("dob", "") or "")
            col5, col6 = st.columns(2)
            pf_dept   = col5.text_input("Department",  value=profile.get("department", ""))
            pf_lic    = col6.text_input("License No.", value=profile.get("license_no", ""))
            pf_loc    = st.text_input("Location / City", value=profile.get("location", ""))
            pf_addr   = st.text_area("Address", value=profile.get("address", ""), height=80)
            saved = st.form_submit_button("💾  Save Profile", type="primary", use_container_width=True)
        if saved:
            upsert_profile(st.session_state.username, {
                "email": pf_email.strip() or None,
                "phone": pf_phone.strip() or None,
                "sex":   pf_sex,
                "dob":   pf_dob.strip() or None,
                "department": pf_dept.strip() or None,
                "license_no": pf_lic.strip() or None,
                "location": pf_loc.strip() or None,
                "address":  pf_addr.strip() or None,
            })
            st.success("✓ Profile updated.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col_so, _ = st.columns([1, 5])
    with col_so:
        if st.button("🚪  Sign Out", use_container_width=True):
            logout()
            st.rerun()

import streamlit as st
from utils.auth import require_role, logout
from utils.db import get_users, get_profile, upsert_profile, update_user

_CSS = """
<style>
.portal-banner {
    background: linear-gradient(135deg, #063d34 0%, #0a8a74 55%, #0fbfa0 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    color: #fff;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.portal-banner::before {
    content:''; position:absolute; width:260px; height:260px;
    background:rgba(255,255,255,0.07); border-radius:50%;
    bottom:-80px; right:80px;
}
.portal-banner::after {
    content:''; position:absolute; width:160px; height:160px;
    background:rgba(255,255,255,0.05); border-radius:50%;
    top:-40px; right:20px;
}
.banner-inner { position:relative; z-index:2; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
.banner-tag { background:rgba(255,255,255,0.18); border-radius:20px; display:inline-block; padding:0.25rem 0.9rem; font-size:0.75rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.6rem; }
.banner-inner h2 { margin:0 0 0.4rem; font-size:1.7rem; font-weight:800; }
.banner-inner p { margin:0 0 1.2rem; color:rgba(255,255,255,0.82); font-size:0.95rem; }
.banner-icon { font-size:4.5rem; opacity:0.9; flex-shrink:0; }
.banner-btn {
    display:inline-block; background:#fff; color:#0a8a74;
    border-radius:30px; padding:0.5rem 1.4rem; font-size:0.88rem;
    font-weight:700; text-decoration:none; cursor:pointer;
    box-shadow:0 4px 14px rgba(0,0,0,0.12);
}
.stat-card {
    background:#fff; border-radius:16px; padding:1.2rem 1.4rem;
    box-shadow:0 2px 16px rgba(10,138,116,0.08);
    border-top:4px solid #0a8a74; height:100%;
}
.stat-icon { font-size:1.8rem; margin-bottom:0.5rem; }
.stat-label { color:#6b7b78; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.9px; margin-bottom:0.3rem; }
.stat-value { color:#1a2e2b; font-size:1.9rem; font-weight:800; margin-bottom:0.2rem; line-height:1; }
.stat-trend { font-size:0.76rem; font-weight:600; }
.trend-up { color:#0a8a74; }
.trend-neutral { color:#6b7b78; }
.section-card {
    background:#fff; border-radius:16px; padding:1.4rem 1.6rem;
    box-shadow:0 2px 16px rgba(0,0,0,0.05); margin-bottom:1rem;
}
.section-card h4 { color:#1a2e2b; font-size:1rem; font-weight:700; margin:0 0 1rem; padding-bottom:0.6rem; border-bottom:2px solid #e8f5f2; }
.patient-row {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.8rem 1rem; border-radius:10px; background:#f7fdfb;
    margin-bottom:0.6rem; border-left:3px solid #0a8a74;
}
.patient-name { font-weight:700; color:#1a2e2b; font-size:0.92rem; }
.patient-meta { color:#6b7b78; font-size:0.78rem; margin-top:2px; }
.pred-badge { background:#e6faf6; color:#0a8a74; font-size:0.75rem; font-weight:700; padding:0.2rem 0.7rem; border-radius:20px; }
.action-card {
    background:linear-gradient(135deg,#0a8a74,#0fbfa0); color:#fff;
    border-radius:14px; padding:1.2rem; text-align:center; cursor:pointer;
    transition:transform 0.2s, box-shadow 0.2s;
    box-shadow:0 4px 14px rgba(10,138,116,0.25);
}
.action-card:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(10,138,116,0.35); }
.action-card .ac-icon { font-size:2rem; margin-bottom:0.4rem; }
.action-card .ac-label { font-size:0.88rem; font-weight:700; }
</style>
"""

def show():
    require_role(["doctor"])
    db = get_users()
    user = db.get(st.session_state.username, {})
    name = user.get("name", st.session_state.username)
    patients = {u: d for u, d in db.items() if d["role"] == "patient"}
    total_preds = sum(len(d.get("data", {}).get("predictions", [])) for d in patients.values())
    ckd_cases = sum(
        1 for d in patients.values()
        for p in d.get("data", {}).get("predictions", [])
        if p.get("result") == "CKD"
    )

    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Welcome banner ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="portal-banner">
        <div class="banner-inner">
            <div>
                <div class="banner-tag">Doctor Dashboard</div>
                <h2>Welcome back, {name}! 👋</h2>
                <p>Monitor patients, run ML predictions, and manage clinical data.</p>
            </div>
            <div class="banner-icon">🩺</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat cards ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">👥</div>
        <div class="stat-label">Total Patients</div>
        <div class="stat-value">{len(patients)}</div>
        <div class="stat-trend trend-up">↑ Active records</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="stat-card" style="border-color:#0fbfa0">
        <div class="stat-icon">🤖</div>
        <div class="stat-label">ML Predictions</div>
        <div class="stat-value">{total_preds}</div>
        <div class="stat-trend trend-up">↑ All time</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="stat-card" style="border-color:#e53e3e">
        <div class="stat-icon">🔴</div>
        <div class="stat-label">CKD Cases</div>
        <div class="stat-value">{ckd_cases}</div>
        <div class="stat-trend trend-neutral">Flagged high risk</div>
    </div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="stat-card" style="border-color:#6b7b78">
        <div class="stat-icon">🏥</div>
        <div class="stat-label">Department</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.4rem">Nephrology</div>
        <div class="stat-trend trend-neutral">Kidney Care Unit</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["🏠  Overview", "👥  Patients", "📋  Notes", "👤  My Profile"])

    with tab1:
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown('<div class="section-card"><h4>⚡ Quick Actions</h4>', unsafe_allow_html=True)
            a1, a2 = st.columns(2)
            with a1:
                if st.button("🔬  Run ML Prediction", use_container_width=True, type="primary"):
                    st.session_state.page = "ml_prediction"
                    st.rerun()
            with a2:
                if st.button("👥  View All Patients", use_container_width=True):
                    st.session_state.page = "doctor_portal"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-card"><h4>📊 Recent Patients</h4>', unsafe_allow_html=True)
            if patients:
                for uname, data in list(patients.items())[:3]:
                    preds = data.get("data", {}).get("predictions", [])
                    last = preds[-1].get("result", "—") if preds else "No data"
                    badge_color = "#e53e3e" if last == "CKD" else ("#0a8a74" if last == "Not CKD" else "#6b7b78")
                    st.markdown(f"""<div class="patient-row">
                        <div>
                            <div class="patient-name">🧑 {data['name']}</div>
                            <div class="patient-meta">@{uname} · {len(preds)} prediction(s)</div>
                        </div>
                        <span style="background:{badge_color}22;color:{badge_color};font-size:0.75rem;font-weight:700;padding:0.2rem 0.8rem;border-radius:20px">{last}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("No patients registered yet.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown(f"""<div class="section-card"><h4>👤 My Profile</h4>
            <div style="text-align:center;padding:1rem 0">
                <div style="width:72px;height:72px;background:linear-gradient(135deg,#0a8a74,#0fbfa0);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 0.8rem">🩺</div>
                <div style="font-weight:800;color:#1a2e2b;font-size:1rem">{name}</div>
                <div style="color:#6b7b78;font-size:0.82rem;margin-top:2px">@{st.session_state.username}</div>
                <div style="margin-top:0.8rem;background:#e6faf6;color:#0a8a74;display:inline-block;
                    padding:0.25rem 1rem;border-radius:20px;font-size:0.78rem;font-weight:700">Doctor · Nephrology</div>
            </div></div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-card"><h4>📈 Prediction Summary</h4>', unsafe_allow_html=True)
            if total_preds:
                ckd_pct = int(ckd_cases / total_preds * 100) if total_preds else 0
                st.markdown(f"""
                <div style="margin-bottom:0.8rem">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-size:0.82rem;color:#6b7b78">CKD Positive</span>
                        <span style="font-size:0.82rem;font-weight:700;color:#e53e3e">{ckd_pct}%</span>
                    </div>
                    <div style="background:#f0f0f0;border-radius:10px;height:8px">
                        <div style="background:#e53e3e;width:{ckd_pct}%;height:8px;border-radius:10px"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-size:0.82rem;color:#6b7b78">Not CKD</span>
                        <span style="font-size:0.82rem;font-weight:700;color:#0a8a74">{100-ckd_pct}%</span>
                    </div>
                    <div style="background:#f0f0f0;border-radius:10px;height:8px">
                        <div style="background:#0a8a74;width:{100-ckd_pct}%;height:8px;border-radius:10px"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("No predictions yet.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><h4>👥 All Patients</h4>', unsafe_allow_html=True)
        if patients:
            for uname, data in patients.items():
                preds = data.get("data", {}).get("predictions", [])
                with st.expander(f"🧑 {data['name']}  (@{uname})  ·  {len(preds)} prediction(s)"):
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Name", data["name"])
                    col_b.metric("Username", uname)
                    col_c.metric("Predictions", len(preds))
                    if preds:
                        st.markdown("**Last 3 Predictions:**")
                        import pandas as pd
                        st.dataframe(pd.DataFrame(preds[-3:]), use_container_width=True)
                    else:
                        st.info("No predictions recorded for this patient yet.")
        else:
            st.info("No patients registered yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-card"><h4>📋 Clinical Notes</h4>', unsafe_allow_html=True)
        note = st.text_area("Observations / Follow-up notes:", placeholder="Enter clinical observations, follow-up instructions, or referrals...", height=180, label_visibility="collapsed")
        col_btn1, col_btn2, _ = st.columns([1, 1, 3])
        with col_btn1:
            if st.button("💾  Save Note", type="primary", use_container_width=True):
                if note.strip():
                    st.success("Note saved successfully.")
                else:
                    st.warning("Note is empty.")
        with col_btn2:
            if st.button("🗑  Clear", use_container_width=True):
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        profile = get_profile(st.session_state.username)
        st.markdown('<div class="section-card"><h4>👤 My Profile</h4>', unsafe_allow_html=True)

        st.markdown("**Account Information**")
        with st.form(key="doctor_account_form"):
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
        with st.form(key="doctor_profile_form"):
            col1, col2 = st.columns(2)
            pf_email = col1.text_input("Email",  value=profile.get("email", ""))
            pf_phone = col2.text_input("Phone",  value=profile.get("phone", ""))
            col3, col4 = st.columns(2)
            pf_sex   = col3.selectbox("Sex", ["Prefer not to say","Male","Female","Other"],
                          index=["Prefer not to say","Male","Female","Other"].index(profile.get("sex", "Prefer not to say")))
            pf_dob   = col4.text_input("Date of Birth (YYYY-MM-DD)", value=profile.get("dob", "") or "")
            col5, col6 = st.columns(2)
            pf_dept  = col5.text_input("Department",    value=profile.get("department", ""))
            pf_lic   = col6.text_input("Medical Reg. No.", value=profile.get("license_no", ""))
            pf_loc   = st.text_input("Location / City",   value=profile.get("location", ""))
            pf_addr  = st.text_area("Address",            value=profile.get("address", ""), height=70)
            saved = st.form_submit_button("💾  Save Profile", type="primary", use_container_width=True)
        if saved:
            upsert_profile(st.session_state.username, {
                "email":       pf_email.strip() or None,
                "phone":       pf_phone.strip() or None,
                "sex":         pf_sex,
                "dob":         pf_dob.strip() or None,
                "department":  pf_dept.strip() or None,
                "license_no":  pf_lic.strip() or None,
                "location":    pf_loc.strip() or None,
                "address":     pf_addr.strip() or None,
            })
            st.success("✓ Profile updated.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col_so, _ = st.columns([1, 5])
    with col_so:
        if st.button("🚪  Sign Out", use_container_width=True):
            logout()
            st.rerun()

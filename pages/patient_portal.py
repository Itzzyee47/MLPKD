import streamlit as st
from utils.auth import require_role, logout
from utils.db import get_users

_CSS = """
<style>
.portal-banner {
    background: linear-gradient(135deg, #063d34 0%, #0a8a74 55%, #0fbfa0 100%);
    border-radius: 20px; padding: 2rem 2.5rem; color: #fff;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
}
.portal-banner::before {
    content:''; position:absolute; width:240px; height:240px;
    background:rgba(255,255,255,0.07); border-radius:50%;
    bottom:-70px; right:100px;
}
.portal-banner::after {
    content:''; position:absolute; width:150px; height:150px;
    background:rgba(255,255,255,0.05); border-radius:50%;
    top:-40px; right:20px;
}
.banner-inner { position:relative; z-index:2; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
.banner-tag { background:rgba(255,255,255,0.18); border-radius:20px; display:inline-block; padding:0.25rem 0.9rem; font-size:0.75rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.6rem; }
.banner-inner h2 { margin:0 0 0.4rem; font-size:1.7rem; font-weight:800; }
.banner-inner p { margin:0; color:rgba(255,255,255,0.82); font-size:0.95rem; }
.banner-icon { font-size:4.5rem; opacity:0.9; flex-shrink:0; }
.stat-card {
    background:#fff; border-radius:16px; padding:1.2rem 1.4rem;
    box-shadow:0 2px 16px rgba(10,138,116,0.08); border-top:4px solid #0a8a74;
}
.stat-icon { font-size:1.8rem; margin-bottom:0.5rem; }
.stat-label { color:#6b7b78; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.9px; margin-bottom:0.3rem; }
.stat-value { color:#1a2e2b; font-size:1.9rem; font-weight:800; margin-bottom:0.2rem; line-height:1; }
.stat-trend { font-size:0.76rem; font-weight:600; }
.trend-up { color:#0a8a74; }
.trend-neutral { color:#6b7b78; }
.section-card { background:#fff; border-radius:16px; padding:1.4rem 1.6rem; box-shadow:0 2px 16px rgba(0,0,0,0.05); margin-bottom:1rem; }
.section-card h4 { color:#1a2e2b; font-size:1rem; font-weight:700; margin:0 0 1rem; padding-bottom:0.6rem; border-bottom:2px solid #e8f5f2; }
.pred-card {
    border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.8rem;
    border-left:4px solid; background:#f9f9f9;
}
.pred-card.ckd { border-color:#e53e3e; background:#fff5f5; }
.pred-card.notckd { border-color:#0a8a74; background:#f0fdf9; }
.pred-card.unknown { border-color:#6b7b78; background:#f7f7f7; }
.pred-result { font-size:1.1rem; font-weight:800; margin-bottom:0.3rem; }
.pred-meta { font-size:0.8rem; color:#6b7b78; }
.empty-state { text-align:center; padding:3rem 1rem; color:#6b7b78; }
.empty-state .es-icon { font-size:3.5rem; margin-bottom:1rem; }
.empty-state p { font-size:0.95rem; }
</style>
"""

def show():
    require_role(["patient"])
    db = get_users()
    user = db.get(st.session_state.username, {})
    name = user.get("name", st.session_state.username)
    predictions = user.get("data", {}).get("predictions", [])
    last_result = predictions[-1].get("result", "—") if predictions else "—"
    last_date = predictions[-1].get("date", "—") if predictions else "—"

    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Welcome banner ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="portal-banner">
        <div class="banner-inner">
            <div>
                <div class="banner-tag">Patient Dashboard</div>
                <h2>Hello, {name}! 🌿</h2>
                <p>Track your kidney health predictions and review your medical history.</p>
            </div>
            <div class="banner-icon">🧑‍⚕️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat cards ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="stat-card" style="border-color:#0a8a74">
        <div class="stat-icon">📊</div>
        <div class="stat-label">Total Predictions</div>
        <div class="stat-value">{len(predictions)}</div>
        <div class="stat-trend trend-up">↑ On record</div>
    </div>""", unsafe_allow_html=True)

    result_color = "#e53e3e" if last_result == "CKD" else ("#0a8a74" if last_result == "Not CKD" else "#6b7b78")
    c2.markdown(f"""<div class="stat-card" style="border-color:{result_color}">
        <div class="stat-icon">{"🔴" if last_result == "CKD" else ("🟢" if last_result == "Not CKD" else "⚪")}</div>
        <div class="stat-label">Last Result</div>
        <div class="stat-value" style="font-size:1.3rem;padding-top:0.3rem">{last_result}</div>
        <div class="stat-trend trend-neutral">{last_date}</div>
    </div>""", unsafe_allow_html=True)

    c3.markdown(f"""<div class="stat-card" style="border-color:#0fbfa0">
        <div class="stat-icon">👤</div>
        <div class="stat-label">Account</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.4rem">@{st.session_state.username}</div>
        <div class="stat-trend trend-neutral">Patient</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["🏠  Overview", "🔍  My Predictions"])

    with tab1:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown('<div class="section-card"><h4>ℹ️ About Your Health Dashboard</h4>', unsafe_allow_html=True)
            st.markdown("""
            Your dashboard shows predictions from kidney disease screening assessments 
            conducted by your doctor using our AI-powered ML model.

            - 🟢 **Not CKD** – No signs of Chronic Kidney Disease detected
            - 🔴 **CKD** – Chronic Kidney Disease indicators found — please consult your doctor
            - Predictions are added by your doctor after each assessment
            """)
            st.markdown("</div>", unsafe_allow_html=True)

            if predictions:
                st.markdown('<div class="section-card"><h4>📈 Recent Predictions</h4>', unsafe_allow_html=True)
                for pred in reversed(predictions[-3:]):
                    r = pred.get("result", "Unknown")
                    cls = "ckd" if r == "CKD" else ("notckd" if r == "Not CKD" else "unknown")
                    icon = "🔴" if r == "CKD" else ("🟢" if r == "Not CKD" else "⚪")
                    st.markdown(f"""<div class="pred-card {cls}">
                        <div class="pred-result">{icon} {r}</div>
                        <div class="pred-meta">Date: {pred.get('date','N/A')} · Risk Score: {pred.get('risk_score','N/A')}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown(f"""<div class="section-card"><h4>👤 My Profile</h4>
            <div style="text-align:center;padding:1rem 0">
                <div style="width:72px;height:72px;background:linear-gradient(135deg,#0a8a74,#0fbfa0);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 0.8rem">🧑</div>
                <div style="font-weight:800;color:#1a2e2b;font-size:1rem">{name}</div>
                <div style="color:#6b7b78;font-size:0.82rem;margin-top:2px">@{st.session_state.username}</div>
                <div style="margin-top:0.8rem;background:#e6faf6;color:#0a8a74;display:inline-block;
                    padding:0.25rem 1rem;border-radius:20px;font-size:0.78rem;font-weight:700">Patient</div>
            </div></div>""", unsafe_allow_html=True)

            if predictions:
                ckd_count = sum(1 for p in predictions if p.get("result") == "CKD")
                ok_count = len(predictions) - ckd_count
                st.markdown(f"""<div class="section-card"><h4>📊 My Summary</h4>
                <div style="display:flex;gap:0.8rem">
                    <div style="flex:1;text-align:center;background:#fff5f5;border-radius:10px;padding:0.8rem">
                        <div style="font-size:1.5rem;font-weight:800;color:#e53e3e">{ckd_count}</div>
                        <div style="font-size:0.75rem;color:#6b7b78">CKD</div>
                    </div>
                    <div style="flex:1;text-align:center;background:#f0fdf9;border-radius:10px;padding:0.8rem">
                        <div style="font-size:1.5rem;font-weight:800;color:#0a8a74">{ok_count}</div>
                        <div style="font-size:0.75rem;color:#6b7b78">Healthy</div>
                    </div>
                </div>
                </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><h4>🔍 All Prediction Results</h4>', unsafe_allow_html=True)
        if not predictions:
            st.markdown("""<div class="empty-state">
                <div class="es-icon">🩺</div>
                <p>No prediction results yet.<br>Your doctor will add them after your assessment.</p>
            </div>""", unsafe_allow_html=True)
        else:
            for i, pred in enumerate(reversed(predictions), start=1):
                r = pred.get("result", "Unknown")
                cls = "ckd" if r == "CKD" else ("notckd" if r == "Not CKD" else "unknown")
                icon = "🔴" if r == "CKD" else ("🟢" if r == "Not CKD" else "⚪")
                with st.expander(f"{icon} Prediction #{len(predictions)-i+1}  ·  {pred.get('date','N/A')}"):
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Result", r)
                    col_b.metric("Risk Score", pred.get("risk_score", "N/A"))
                    col_c.metric("Date", pred.get("date", "N/A"))
                    if pred.get("notes"):
                        st.info(f"📝 {pred['notes']}")
                    if pred.get("features"):
                        st.markdown("**Input Features:**")
                        st.json(pred["features"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col_so, _ = st.columns([1, 5])
    with col_so:
        if st.button("🚪  Sign Out", use_container_width=True):
            logout()
            st.rerun()

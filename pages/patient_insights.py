import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.auth import require_role, logout
from utils.db import get_user

def show():
    require_role(["patient"])
    user = get_user(st.session_state.username) or {}
    name = user.get("name", st.session_state.username)
    predictions = user.get("data", {}).get("predictions", [])

    st.title("🔍 My Disease Insights")
    st.markdown(f"Personalized prediction insights for **{name}**")
    st.divider()

    if not predictions:
        st.warning("No prediction results on record yet. Please check back after your doctor has run an assessment.")
        st.divider()
        if st.button("← Back to Portal"):
            st.session_state.page = "patient_portal"
            st.rerun()
        return

    # ── Summary Metrics ───────────────────────────────────────────────────────
    latest = predictions[-1]
    latest_result = latest.get("result", "Unknown")
    latest_risk = float(str(latest.get("risk_score", "0%")).replace("%", ""))
    total = len(predictions)
    ckd_count = sum(1 for p in predictions if p.get("result") == "CKD")

    result_color = "red" if latest_result == "CKD" else "green"
    st.markdown(f"### Latest Diagnosis: :{result_color}[**{latest_result}**]")
    st.caption(f"Assessment date: {latest.get('date', 'N/A')}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assessments", total)
    col2.metric("CKD Positive Results", ckd_count)
    col3.metric("Latest Risk Score", f"{latest_risk}%")

    st.divider()

    # ── Risk Gauge ────────────────────────────────────────────────────────────
    st.subheader("Current Risk Score")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=latest_risk,
        title={"text": "CKD Risk (%)"},
        delta={"reference": 50, "increasing": {"color": "red"}, "decreasing": {"color": "green"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "crimson" if latest_result == "CKD" else "#2ecc71"},
            "steps": [
                {"range": [0, 40],  "color": "#d4edda"},
                {"range": [40, 65], "color": "#fff3cd"},
                {"range": [65, 100],"color": "#f8d7da"},
            ],
            "threshold": {"line": {"color": "black", "width": 4}, "value": 50},
        },
    ))
    gauge.update_layout(height=300)
    st.plotly_chart(gauge, use_container_width=True)

    # ── Risk Trend Over Time ──────────────────────────────────────────────────
    if total > 1:
        st.subheader("📈 Risk Score Trend")
        trend_df = pd.DataFrame([{
            "Assessment": f"#{i+1} ({p.get('date','?')})",
            "Risk Score (%)": float(str(p.get("risk_score", "0%")).replace("%", "")),
            "Result": p.get("result", "Unknown"),
        } for i, p in enumerate(predictions)])

        line = px.line(
            trend_df, x="Assessment", y="Risk Score (%)",
            markers=True, title="Risk Score Over Time",
            color_discrete_sequence=["#1f77b4"],
        )
        line.add_hline(y=50, line_dash="dash", line_color="red",
                       annotation_text="Risk Threshold (50%)")
        st.plotly_chart(line, use_container_width=True)

    # ── Latest Clinical Features ──────────────────────────────────────────────
    st.subheader("🧪 Latest Lab Values")
    feats = latest.get("features", {})
    if feats:
        feat_df = pd.DataFrame(feats.items(), columns=["Measurement", "Value"])
        st.table(feat_df)
    else:
        st.info("No feature data available.")

    # ── Doctor's Notes ────────────────────────────────────────────────────────
    notes = latest.get("notes", "—")
    if notes and notes != "—":
        st.subheader("📋 Doctor's Notes")
        st.info(notes)

    # ── Health Advice ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("💡 General Recommendations")
    if latest_result == "CKD":
        st.error("""
        **Your latest assessment indicates CKD risk.** Please follow your doctor's guidance.
        - 🥗 Follow a low-protein, low-sodium diet
        - 💧 Monitor fluid intake as advised
        - 💊 Take prescribed medications consistently
        - 🩺 Schedule regular follow-up appointments
        - 🚫 Avoid NSAIDs and nephrotoxic drugs
        """)
    else:
        st.success("""
        **Your latest assessment is within normal range.** Keep up the healthy habits!
        - 🥦 Maintain a balanced diet and healthy weight
        - 🚰 Stay well hydrated (6–8 glasses/day)
        - 🏃 Exercise regularly
        - 🩺 Continue annual kidney function screening
        - 🚭 Avoid smoking and limit alcohol
        """)

    # ── Full History ──────────────────────────────────────────────────────────
    with st.expander("📂 Full Prediction History"):
        for i, rec in enumerate(reversed(predictions), start=1):
            res = rec.get("result", "Unknown")
            icon = "🔴" if res == "CKD" else "🟢"
            st.markdown(f"**{icon} Assessment #{total - i + 1}** — {rec.get('date','N/A')} &nbsp; | &nbsp; Result: `{res}` &nbsp; | &nbsp; Risk: {rec.get('risk_score','N/A')}")

    st.divider()
    if st.button("← Back to Portal"):
        st.session_state.page = "patient_portal"
        st.rerun()
    if st.button("🚪 Sign Out"):
        logout()
        st.rerun()

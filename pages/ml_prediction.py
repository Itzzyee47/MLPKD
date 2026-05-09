import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from utils.auth import require_role, logout
from utils.db import get_users, add_prediction

# ---------------------------------------------------------------------------
# Lightweight mock model — replace with joblib.load("model.pkl") in production
# ---------------------------------------------------------------------------
def mock_predict(features: dict) -> tuple[str, float]:
    """Returns (label, risk_probability). Replace with real model inference."""
    risk_score = (
        (features["creatinine"] / 10) +
        (features["urea"] / 200) +
        (1 - features["hemoglobin"] / 18) +
        (features["albumin_flag"] * 0.2) +
        (features["htn_flag"] * 0.15) +
        (features["dm_flag"] * 0.15)
    ) / 1.75
    risk_score = float(np.clip(risk_score, 0.0, 1.0))
    label = "CKD" if risk_score >= 0.5 else "Not CKD"
    return label, round(risk_score * 100, 2)

# ---------------------------------------------------------------------------
def show():
    require_role(["doctor"])
    st.title("🔬 ML Prediction & Analytics")
    st.markdown("Accessible by **Doctors only**. Run CKD predictions and explore population analytics.")
    st.divider()

    tab1, tab2 = st.tabs(["🧠 Run Prediction", "📊 Analytics Dashboard"])

    # ── TAB 1: Prediction ────────────────────────────────────────────────────
    with tab1:
        st.subheader("Patient CKD Risk Prediction")

        db = get_users()
        patients = {u: d for u, d in db.items() if d["role"] == "patient"}
        patient_map = {d["name"]: u for u, d in patients.items()}

        if not patient_map:
            st.warning("No patients registered yet.")
        else:
            selected_name = st.selectbox("Select Patient", list(patient_map.keys()))
            selected_uname = patient_map[selected_name]

            st.markdown("#### Clinical Input Features")
            col1, col2, col3 = st.columns(3)
            creatinine = col1.number_input("Serum Creatinine (mg/dL)", 0.1, 20.0, 1.2)
            urea       = col2.number_input("Blood Urea (mg/dL)", 5.0, 200.0, 30.0)
            hemoglobin = col3.number_input("Hemoglobin (g/dL)", 3.0, 20.0, 13.5)

            col4, col5, col6 = st.columns(3)
            bp         = col4.number_input("Blood Pressure (mmHg)", 50, 200, 80)
            sg         = col5.number_input("Specific Gravity", 1.000, 1.030, 1.015, step=0.001, format="%.3f")
            albumin    = col6.selectbox("Albumin Level (0–5)", [0, 1, 2, 3, 4, 5], index=0)

            col7, col8 = st.columns(2)
            htn = col7.checkbox("Hypertension")
            dm  = col8.checkbox("Diabetes Mellitus")

            notes = st.text_area("Doctor's Notes (optional)", placeholder="Observations, context...")

            if st.button("▶ Run Prediction", type="primary", use_container_width=True):
                features = {
                    "creatinine": creatinine,
                    "urea": urea,
                    "hemoglobin": hemoglobin,
                    "bp": bp,
                    "sg": float(sg),
                    "albumin_flag": 1 if albumin >= 2 else 0,
                    "htn_flag": int(htn),
                    "dm_flag": int(dm),
                }
                result, risk_pct = mock_predict(features)
                color = "red" if result == "CKD" else "green"

                st.divider()
                st.markdown(f"### Prediction Result: :{color}[**{result}**]")
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_pct,
                    title={"text": "CKD Risk Score (%)"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "crimson" if result == "CKD" else "green"},
                        "steps": [
                            {"range": [0, 40], "color": "#d4edda"},
                            {"range": [40, 65], "color": "#fff3cd"},
                            {"range": [65, 100], "color": "#f8d7da"},
                        ],
                        "threshold": {"line": {"color": "black", "width": 4}, "value": 50},
                    },
                ))
                gauge.update_layout(height=300)
                st.plotly_chart(gauge, use_container_width=True)

                # Save to patient record
                record = {
                    "date": str(date.today()),
                    "result": result,
                    "risk_score": f"{risk_pct}%",
                    "notes": notes or "—",
                    "features": {
                        "Creatinine": creatinine, "Urea": urea,
                        "Hemoglobin": hemoglobin, "BP": bp,
                        "SG": sg, "Albumin": albumin,
                        "HTN": htn, "DM": dm,
                    },
                }
                add_prediction(selected_uname, record)
                st.success(f"Result saved to **{selected_name}**'s record.")

    # ── TAB 2: Analytics ─────────────────────────────────────────────────────
    with tab2:
        st.subheader("Population Analytics")
        db = get_users()
        all_preds = []
        for uname, data in db.items():
            if data["role"] == "patient":
                for p in data.get("data", {}).get("predictions", []):
                    all_preds.append({
                        "Patient": data["name"],
                        "Date": p.get("date"),
                        "Result": p.get("result"),
                        "Risk Score": float(str(p.get("risk_score", "0%")).replace("%", "")),
                    })

        if not all_preds:
            st.info("No predictions recorded yet. Run predictions to see analytics here.")
        else:
            df = pd.DataFrame(all_preds)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Predictions", len(df))
            col2.metric("CKD Cases", int((df["Result"] == "CKD").sum()))
            col3.metric("Avg Risk Score", f"{df['Risk Score'].mean():.1f}%")

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                pie = px.pie(df, names="Result", title="CKD vs Not CKD Distribution",
                             color="Result",
                             color_discrete_map={"CKD": "#e74c3c", "Not CKD": "#2ecc71"})
                st.plotly_chart(pie, use_container_width=True)

            with c2:
                bar = px.bar(df, x="Patient", y="Risk Score", color="Result",
                             title="Risk Scores by Patient",
                             color_discrete_map={"CKD": "#e74c3c", "Not CKD": "#2ecc71"})
                st.plotly_chart(bar, use_container_width=True)

            st.markdown("### Full Prediction Log")
            st.dataframe(df, use_container_width=True)

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Back to Portal"):
            st.session_state.page = "doctor_portal"
            st.rerun()
    with col_b:
        if st.button("🚪 Sign Out"):
            logout()
            st.rerun()

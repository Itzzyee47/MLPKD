import streamlit as st

def show():
    st.title("📖 About MLPKD")
    st.divider()

    st.markdown("""
    ## What is MLPKD?
    **MLPKD** (Machine Learning for Polycystic Kidney Disease) is a clinical decision-support
    web application that harnesses the power of machine learning to assist healthcare professionals
    in the **early detection and management** of kidney-related conditions.

    ---
    ## 🎯 Project Objectives
    - Provide real-time **ML-powered disease risk predictions** based on patient lab values and vitals.
    - Deliver a **multi-role platform** accessible to doctors, nurses, lab technicians, and patients.
    - Offer **transparent visual analytics** to support evidence-based clinical decisions.
    - Empower patients with clear, understandable **insight reports** on their health status.

    ---
    ## 🏥 Supported User Roles
    | Role | Access |
    |------|--------|
    | **Doctor** | Full access: predictions, analytics, patient records |
    | **Nurse** | Patient vitals, care notes, patient list |
    | **Lab Technician** | Upload and manage lab results |
    | **Patient** | Personal profile, prediction insights |

    ---
    ## 🤖 The ML Model
    The prediction engine uses a trained **Random Forest / XGBoost** classifier trained on the
    [UCI CKD Dataset](https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease), achieving
    over **97% accuracy** on hold-out test data.

    **Key features used:**
    - Serum creatinine, blood urea, hemoglobin
    - Blood pressure, specific gravity, albumin
    - Diabetes mellitus, hypertension flags

    ---
    ## 👨‍💻 Development Team
    Built with ❤️ using **Python · Streamlit · scikit-learn · Pandas · Plotly**.
    """)

    st.info("Navigate to **Sign In** to access your role-specific portal, or **Register** if you are a new user.")

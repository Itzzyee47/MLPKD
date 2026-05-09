"""
Simulated in-memory user database.
In production, replace with a real DB (SQLite, PostgreSQL, etc.).
Schema: { username: { "password": str, "role": str, "name": str, "data": dict } }
"""

import streamlit as st

_USERS: dict = {
    # Pre-seeded demo accounts
    "dr_john": {"password": "doc123", "role": "doctor", "name": "Dr. John Smith", "data": {}},
    "nurse_amy": {"password": "nur123", "role": "nurse", "name": "Nurse Amy Lee", "data": {}},
    "lab_kai": {"password": "lab123", "role": "lab_tech", "name": "Kai Brooks (Lab)", "data": {}},
    "patient_bob": {"password": "pat123", "role": "patient", "name": "Bob Martin", "data": {"predictions": []}},
}

def get_users() -> dict:
    if "users_db" not in st.session_state:
        st.session_state.users_db = _USERS.copy()
    return st.session_state.users_db

def register_user(username: str, password: str, role: str, name: str) -> tuple[bool, str]:
    db = get_users()
    if username in db:
        return False, "Username already exists."
    db[username] = {"password": password, "role": role, "name": name, "data": {"predictions": []}}
    return True, "Registration successful!"

def authenticate(username: str, password: str) -> tuple[bool, dict | None]:
    db = get_users()
    user = db.get(username)
    if user and user["password"] == password:
        return True, user
    return False, None

def get_user(username: str) -> dict | None:
    return get_users().get(username)

def add_prediction(username: str, record: dict):
    db = get_users()
    if username in db:
        db[username]["data"].setdefault("predictions", []).append(record)

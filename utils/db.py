"""
Supabase-backed user, profile, prediction, and vitals store.

Required Supabase tables (run the SQL in supabase_schema.sql):
  users       (id, username, password_hash, role, name, created_at)
  profiles    (username PK, email, phone, sex, dob, blood_group, location,
               address, department, license_no, allergies, conditions,
               emergency_contact_name, emergency_contact_phone, updated_at)
  predictions (id, username, date, result, risk_score, notes, features, created_at)
  vitals      (id, patient_username, recorded_by, recorded_at, bp, heart_rate,
               temperature, weight, spo2, respiratory_rate, notes)
"""

from collections import defaultdict
import uuid
import bcrypt
from datetime import datetime, timedelta, timezone
from utils.supabase_client import get_client

_SESSION_TTL_DAYS = 7


# -- internal helpers ------------------------------------------------------

def _row_to_user(row: dict, preds: list) -> dict:
    return {
        "role": row["role"],
        "name": row["name"],
        "data": {"predictions": preds},
    }


def _format_pred(p: dict) -> dict:
    return {
        "date":       p.get("date"),
        "result":     p.get("result"),
        "risk_score": p.get("risk_score"),
        "notes":      p.get("notes"),
        "features":   p.get("features") or {},
    }


def _format_vitals(v: dict) -> dict:
    return {
        "recorded_at":      v.get("recorded_at"),
        "recorded_by":      v.get("recorded_by"),
        "bp":               v.get("bp"),
        "heart_rate":       v.get("heart_rate"),
        "temperature":      v.get("temperature"),
        "weight":           v.get("weight"),
        "spo2":             v.get("spo2"),
        "respiratory_rate": v.get("respiratory_rate"),
        "notes":            v.get("notes"),
    }


# -- users -----------------------------------------------------------------

def get_users() -> dict:
    """Return { username: { role, name, data: { predictions: [] } } } for all users."""
    sb = get_client()
    users_res = sb.table("users").select("username, role, name").execute()
    preds_res = sb.table("predictions").select("*").order("created_at").execute()

    pred_map: dict[str, list] = defaultdict(list)
    for p in (preds_res.data or []):
        pred_map[p["username"]].append(_format_pred(p))

    return {
        row["username"]: _row_to_user(row, pred_map[row["username"]])
        for row in (users_res.data or [])
    }


def get_user(username: str) -> dict | None:
    """Fetch a single user with their predictions."""
    sb = get_client()
    res = sb.table("users").select("username, role, name").eq("username", username).execute()
    if not res.data:
        return None
    preds_res = (
        sb.table("predictions")
        .select("*")
        .eq("username", username)
        .order("created_at")
        .execute()
    )
    preds = [_format_pred(p) for p in (preds_res.data or [])]
    return _row_to_user(res.data[0], preds)


def register_user(username: str, password: str, role: str, name: str) -> tuple[bool, str]:
    sb = get_client()
    existing = sb.table("users").select("username").eq("username", username).execute()
    if existing.data:
        return False, "Username already exists."
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    sb.table("users").insert({
        "username":      username,
        "password_hash": pw_hash,
        "role":          role,
        "name":          name,
    }).execute()
    return True, "Registration successful!"


def authenticate(username: str, password: str) -> tuple[bool, dict | None]:
    sb = get_client()
    res = (
        sb.table("users")
        .select("username, password_hash, role, name")
        .eq("username", username)
        .execute()
    )
    if not res.data:
        return False, None
    row = res.data[0]
    if bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        return True, {"role": row["role"], "name": row["name"]}
    return False, None


def update_user(
    old_username: str,
    new_username: str,
    new_name: str,
    new_password: str = None,
) -> tuple[bool, str]:
    """Update username, display name, and optionally password.
    Cascades username change across all related tables."""
    sb = get_client()

    if new_username != old_username:
        existing = sb.table("users").select("username").eq("username", new_username).execute()
        if existing.data:
            return False, "That username is already taken."

    payload: dict = {"name": new_name}
    if new_username != old_username:
        payload["username"] = new_username
    if new_password:
        payload["password_hash"] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    sb.table("users").update(payload).eq("username", old_username).execute()

    if new_username != old_username:
        sb.table("profiles").update({"username": new_username}).eq("username", old_username).execute()
        sb.table("predictions").update({"username": new_username}).eq("username", old_username).execute()
        sb.table("vitals").update({"patient_username": new_username}).eq("patient_username", old_username).execute()
        sb.table("vitals").update({"recorded_by": new_username}).eq("recorded_by", old_username).execute()
        sb.table("sessions").update({"username": new_username}).eq("username", old_username).execute()

    return True, "Account updated successfully."


# -- profiles --------------------------------------------------------------

def get_profile(username: str) -> dict:
    """Return the profile row for a user, or an empty dict if none exists yet."""
    sb = get_client()
    res = sb.table("profiles").select("*").eq("username", username).execute()
    return res.data[0] if res.data else {}


def upsert_profile(username: str, data: dict) -> None:
    """Create or update the profile row for a user (partial updates are fine)."""
    sb = get_client()
    payload = {"username": username, **data}
    sb.table("profiles").upsert(payload, on_conflict="username").execute()


# -- predictions -----------------------------------------------------------

def add_prediction(username: str, record: dict):
    sb = get_client()
    sb.table("predictions").insert({
        "username":   username,
        "date":       record.get("date"),
        "result":     record.get("result"),
        "risk_score": record.get("risk_score"),
        "notes":      record.get("notes"),
        "features":   record.get("features"),
    }).execute()


# -- vitals ----------------------------------------------------------------

def add_vitals(patient_username: str, recorded_by: str, reading: dict) -> None:
    """Save a vitals reading recorded by a nurse."""
    sb = get_client()
    sb.table("vitals").insert({
        "patient_username": patient_username,
        "recorded_by":      recorded_by,
        "bp":               reading.get("bp"),
        "heart_rate":       reading.get("heart_rate"),
        "temperature":      reading.get("temperature"),
        "weight":           reading.get("weight"),
        "spo2":             reading.get("spo2"),
        "respiratory_rate": reading.get("respiratory_rate"),
        "notes":            reading.get("notes"),
    }).execute()


def get_vitals(patient_username: str) -> list[dict]:
    """Return all vitals readings for a patient, newest first."""
    sb = get_client()
    res = (
        sb.table("vitals")
        .select("*")
        .eq("patient_username", patient_username)
        .order("recorded_at", desc=True)
        .execute()
    )
    return [_format_vitals(v) for v in (res.data or [])]


# ── sessions ──────────────────────────────────────────────────────────────

def create_session(username: str, role: str) -> str:
    """Create a server-side session and return its token."""
    sb = get_client()
    token = str(uuid.uuid4())
    expires_at = (datetime.now(timezone.utc) + timedelta(days=_SESSION_TTL_DAYS)).isoformat()
    sb.table("sessions").insert({
        "token":      token,
        "username":   username,
        "role":       role,
        "expires_at": expires_at,
    }).execute()
    return token


def restore_session(token: str) -> dict | None:
    """Return {username, role} if token is valid and unexpired, else None."""
    sb = get_client()
    res = sb.table("sessions").select("username, role, expires_at").eq("token", token).execute()
    if not res.data:
        return None
    row = res.data[0]
    expires_at = datetime.fromisoformat(row["expires_at"].replace("Z", "+00:00"))
    if datetime.now(timezone.utc) > expires_at:
        delete_session(token)
        return None
    return {"username": row["username"], "role": row["role"]}


def delete_session(token: str) -> None:
    """Invalidate a session (on logout)."""
    get_client().table("sessions").delete().eq("token", token).execute()

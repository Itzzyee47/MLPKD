-- ============================================================
-- MLPKD — Supabase Schema  (v2 — profiles + vitals)
-- Run this SQL in the Supabase SQL Editor for your project:
-- https://supabase.com/dashboard → SQL Editor → New query
-- ============================================================

-- ── Core users table ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('doctor', 'patient', 'nurse', 'lab_tech')),
    name          TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ── Profiles table (one row per user, optional extended info) ─────────────
-- Applies to ALL roles (doctors, nurses, patients, lab techs).
CREATE TABLE IF NOT EXISTS profiles (
    username    TEXT PRIMARY KEY REFERENCES users(username) ON DELETE CASCADE,
    email       TEXT,
    phone       TEXT,
    sex         TEXT CHECK (sex IN ('Male', 'Female', 'Other', 'Prefer not to say')),
    dob         DATE,                       -- date of birth
    blood_group TEXT,                       -- e.g. A+, O-
    location    TEXT,                       -- city / region
    address     TEXT,
    -- clinical staff extras
    department  TEXT,
    license_no  TEXT,
    -- patient extras
    allergies   TEXT,
    conditions  TEXT,                       -- known pre-existing conditions
    emergency_contact_name  TEXT,
    emergency_contact_phone TEXT,
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Predictions table ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS predictions (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username   TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    date       TEXT,
    result     TEXT,
    risk_score TEXT,
    notes      TEXT,
    features   JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Vitals table (nurse-recorded, one row per reading) ────────────────────
CREATE TABLE IF NOT EXISTS vitals (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_username  TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    recorded_by       TEXT NOT NULL REFERENCES users(username),   -- nurse username
    recorded_at       TIMESTAMPTZ DEFAULT NOW(),
    bp                INTEGER,      -- systolic blood pressure (mmHg)
    heart_rate        INTEGER,      -- bpm
    temperature       NUMERIC(4,1), -- °C
    weight            NUMERIC(5,1), -- kg
    spo2              INTEGER,      -- %
    respiratory_rate  INTEGER,      -- breaths/min
    notes             TEXT
);

-- ── Sessions table (persistent login across browser reloads) ─────────────
CREATE TABLE IF NOT EXISTS sessions (
    token       TEXT PRIMARY KEY,
    username    TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    role        TEXT NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Row Level Security ────────────────────────────────────────────────────
ALTER TABLE users       ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles    ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE vitals      ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions    ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow_all_users"       ON users       FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_profiles"    ON profiles    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_predictions" ON predictions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_vitals"      ON vitals      FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_sessions"    ON sessions    FOR ALL USING (true) WITH CHECK (true);

-- ── Optional: seed demo accounts ──────────────────────────────────────────
-- Passwords are bcrypt hashes. Generate fresh ones with:
--   python -c "import bcrypt; print(bcrypt.hashpw(b'doc123', bcrypt.gensalt()).decode())"
--
-- INSERT INTO users (username, password_hash, role, name) VALUES
--   ('dr_john',     '<hash>', 'doctor',   'Dr. John Smith'),
--   ('nurse_amy',   '<hash>', 'nurse',    'Nurse Amy Lee'),
--   ('lab_kai',     '<hash>', 'lab_tech', 'Kai Brooks (Lab)'),
--   ('patient_bob', '<hash>', 'patient',  'Bob Martin');

-- ── Migration: if you already created v1 tables, run this block instead ───
-- (Skip this if you are starting fresh — the CREATE TABLE IF NOT EXISTS above handles it)
--
-- ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;
-- (profiles and vitals are new — just run the CREATE TABLE statements above)

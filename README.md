# MLPKD — ML-Powered Kidney Disease Prediction Platform

A web-based clinical decision support system that leverages machine learning to enable early detection and management of Chronic Kidney Disease (CKD). The platform integrates a trained predictive model — built on patient lab values and vitals — into a role-based healthcare portal accessible to **doctors, nurses, lab technicians, and patients**.

---

## Features

- **CKD risk prediction** from routine lab results (creatinine, urea, hemoglobin, albumin, specific gravity, blood pressure, etc.)
- **Role-specific dashboards** for streamlined clinical workflows
- **Patient record management** with longitudinal prediction tracking
- **Lab result submission** with automatic out-of-range flagging
- **Vitals recording and monitoring** by nursing staff
- **Supabase-backed** persistent storage with bcrypt password hashing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| Database | Supabase (PostgreSQL) |
| ML | scikit-learn |
| Charts | Plotly |
| Auth | bcrypt + Streamlit session state |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Itzzyee47/MLPKD.git
cd MLPKD
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Supabase

1. Create a free project at [supabase.com](https://supabase.com)
2. In your Supabase dashboard go to **SQL Editor → New query**
3. Paste and run the entire contents of [`supabase_schema.sql`](supabase_schema.sql) — this creates the `users` and `predictions` tables with the correct policies
4. Go to **Settings → API** and copy your **Project URL** and **anon public key**

### 5. Configure credentials

Create the file `.streamlit/secrets.toml` (already gitignored):

```toml
[supabase]
url = "https://your-project-ref.supabase.co"
key = "your-anon-public-key"
```

### 6. Seed demo accounts (optional)

Register accounts directly through the app's **Register** page, or run the seed SQL at the bottom of `supabase_schema.sql` after generating bcrypt hashes:

```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())"
```

### 7. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Project Structure

```
MLPKD/
├── app.py                   # Entry point — page config, global CSS, router
├── requirements.txt
├── supabase_schema.sql      # Run this in Supabase SQL Editor
├── .streamlit/
│   └── secrets.toml         # Your credentials (gitignored — do not commit)
├── utils/
│   ├── auth.py              # Session management, login/logout, role guard
│   ├── db.py                # Supabase queries (users + predictions)
│   └── supabase_client.py   # Cached Supabase client
└── pages/
    ├── landing.py           # Public landing page
    ├── about.py             # About page
    ├── signin.py            # Authentication
    ├── register.py          # New user registration
    ├── doctor_portal.py     # Doctor dashboard
    ├── patient_portal.py    # Patient dashboard
    ├── nurse_portal.py      # Nurse dashboard
    ├── labtech_portal.py    # Lab technician dashboard
    ├── ml_prediction.py     # CKD prediction form (doctors)
    └── patient_insights.py  # Patient prediction insights
```

---

## User Roles

| Role | Access |
|---|---|
| `doctor` | Run ML predictions, view all patients, write notes |
| `nurse` | Record patient vitals, write care notes |
| `lab_tech` | Submit lab results, view kidney panel reference ranges |
| `patient` | View own prediction history and health insights |

---

## Environment Variables / Secrets

| Key | Description |
|---|---|
| `supabase.url` | Your Supabase project URL |
| `supabase.key` | Supabase anon public key |

Never commit `.streamlit/secrets.toml` — it is listed in `.gitignore`.

---

## License

See [LICENSE](LICENSE).

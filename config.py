import os

# ==================================================
# ================= BASE DIR =======================
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================================================
# ================= DATABASES ======================
# ==================================================

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USER_DB = os.path.join(DATA_DIR, "users.db")
OTP_DB = os.path.join(DATA_DIR, "otp.db")
WORKER_DB = os.path.join(DATA_DIR, "workers.db")

# ==================================================
# ================= EMAIL (TEMP) ===================
# ==================================================
# NOTE: Safe for local testing & college submission.
# Do NOT push real credentials to public repos.

EMAIL_ADDRESS = "co2023.vedant.gate@ves.ac.in"
EMAIL_PASSWORD = "cius tckr tpva tewf"  # TEMP

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ==================================================
# ================= JWT ============================
# ==================================================

JWT_SECRET = "super-secret-key"
JWT_EXP_MINUTES = 60

# ==================================================
# ================= OTP ============================
# ==================================================

OTP_EXPIRY_MINUTES = 2

# ==================================================
# ========== HEALTHCARE WORKER DOCUMENTS ===========
# ==================================================

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
HEALTHCARE_UPLOAD_DIR = os.path.join(UPLOAD_DIR, "healthcare_workers")

HEALTHCARE_REQUIRED_DOCS = [
    "license",
    "certificate",
    "id_proof"
]

os.makedirs(HEALTHCARE_UPLOAD_DIR, exist_ok=True)

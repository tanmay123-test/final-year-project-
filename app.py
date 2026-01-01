from flask import Flask, request, jsonify
from user_db import UserDB
from auth_utils import generate_token, verify_token
from otp_service import send_otp, verify_otp

app = Flask(__name__)
db = UserDB()


# ---------------- USER SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    """
    1. Create a new unverified user
    2. Send OTP to the email entered by the user
    """
    data = request.json

    required_fields = ["name", "username", "password", "email"]
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    # Check if user/email already exists
    if db.user_exists(data["username"], data["email"]):
        return jsonify({"error": "User already exists"}), 400

    # Create user as UNVERIFIED
    db.create_user(
        name=data["name"],
        username=data["username"],
        password=data["password"],
        email=data["email"]
    )

    # Send OTP to user's email
    send_otp(data["email"])

    return jsonify({
        "msg": f"OTP sent to {data['email']}"
    }), 201


# ---------------- OTP VERIFICATION ----------------
@app.route("/verify-otp", methods=["POST"])
def verify_user_otp():
    """
    Verify OTP sent to user's email and mark user as verified
    """
    data = request.json

    if "email" not in data or "otp" not in data:
        return jsonify({"error": "Email and OTP required"}), 400

    success, message = verify_otp(data["email"], data["otp"])

    if not success:
        return jsonify({"error": message}), 400

    db.mark_verified(data["email"])
    return jsonify({"msg": message}), 200


# ---------------- RESEND OTP ----------------
@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    """
    Resend OTP only if user exists AND is not verified
    """
    data = request.json

    if "email" not in data:
        return jsonify({"error": "Email required"}), 400

    # Check if user exists
    user = db.get_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Prevent resend if already verified
    if user["is_verified"]:
        return jsonify({"error": "User already verified"}), 400

    send_otp(data["email"])
    return jsonify({"msg": "OTP resent successfully"}), 200


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    """
    Login only allowed for verified users
    """
    data = request.json

    success, message = db.verify_user(
        data["username"],
        data["password"]
    )

    if not success:
        return jsonify({"error": message}), 401

    token = generate_token(data["username"])
    return jsonify({"token": token}), 200


# ---------------- PROTECTED ROUTE ----------------
@app.route("/expert-query", methods=["POST"])
def expert_query():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"error": "Invalid or expired token"}), 401

    query = request.json.get("query", "")
    return jsonify({
        "user": username,
        "answer": f"ExpertEase response to '{query}'"
    })


if __name__ == "__main__":
    app.run(debug=True)

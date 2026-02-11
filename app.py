from flask import Flask, request, jsonify
from flask_cors import CORS
from meeting_utils import create_meeting_link
import random
from user_db import UserDB
from worker_db import WorkerDB
from appointment_db import AppointmentDB
from subscription_db import SubscriptionDB
from message_db import MessageDB
from availability_db import AvailabilityDB
from event_db import EventDB
import sqlite3
from emergency_detector import is_emergency

from auth_utils import generate_token, verify_token
from otp_service import send_otp, verify_otp
from email_service import send_email

from video_db import VideoConsultDB

import appointment_db
print("🔥 USING appointment_db FROM:", appointment_db.__file__)

from video_db import VideoConsultDB
from notification_service import notify_user, notify_doctor

video_db = VideoConsultDB()
video_db.create_table()

from datetime import datetime

app = Flask(__name__)
# CORS: web (5173, 5174), Expo (8081), mobile (null), Android emulator
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://localhost:8081", "http://localhost:19006", "null"]}})

# ================= DATABASE =================
user_db = UserDB()
worker_db = WorkerDB()
appt_db = AppointmentDB()
message_db = MessageDB()
availability_db = AvailabilityDB()
event_db = EventDB()
subscription_db = SubscriptionDB()

# ================= AUTH =====================
def require_auth():
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    try:
        return verify_token(auth.split(" ")[1])
    except:
        return None


# ================= SERVICES =================
@app.route("/services")
def get_services():
    services = [
        {"id": "healthcare", "label": "Healthcare", "path": "/doctors"},
        {"id": "housekeeping", "label": "Housekeeping", "path": "/worker/housekeeping/login"},
        {"id": "resource", "label": "Resource Management", "path": "/worker/resource/login"},
        {"id": "car", "label": "Car Services", "path": "/worker/car/login"},
        {"id": "money", "label": "Money Management", "path": "/worker/money/login"}
    ]
    return jsonify({"services": services}), 200


# ================= USER AUTH =================
@app.route("/signup", methods=["POST"])
def signup():
    d = request.json
    if user_db.user_exists(d["username"], d["email"]):
        return jsonify({"error": "User exists"}), 400

    user_db.create_user(d["name"], d["username"], d["password"], d["email"])
    send_otp(d["email"])
    return jsonify({"msg": "OTP sent"}), 201


@app.route("/verify-otp", methods=["POST"])
def verify_user_otp():
    ok, msg = verify_otp(request.json["email"], request.json["otp"])
    if not ok:
        return jsonify({"error": msg}), 400
    user_db.mark_verified(request.json["email"])
    return jsonify({"msg": "Verified"}), 200


@app.route("/resend-otp", methods=["POST"])
def resend_user_otp():
    send_otp(request.json["email"])
    return jsonify({"msg": "OTP resent"}), 200


@app.route("/login", methods=["POST"])
def login():
    ok, msg = user_db.verify_user(
        request.json["username"],
        request.json["password"]
    )
    if not ok:
        return jsonify({"error": msg}), 401

    return jsonify({
        "token": generate_token(request.json["username"]),
        "user_id": user_db.get_user_by_username(request.json["username"])
    }), 200


@app.route("/user/info")
def user_info():
    username = require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get user details
    user_id = user_db.get_user_by_username(username)
    if not user_id:
        return jsonify({"error": "User not found"}), 404
    
    # Get user name from database
    conn = sqlite3.connect("data/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    user_name = result[0] if result else f"User_{user_id}"
    
    return jsonify({
        "user_id": user_id,
        "user_name": user_name,
        "username": username
    }), 200


# ================= HEALTHCARE =================
@app.route("/healthcare/specializations")
def get_specializations():
    DEFAULT = [
        "Dentist","Eye Specialist","Cardiologist","Orthopedic","ENT",
        "Dermatologist","Neurologist","Psychiatrist","Gynecologist",
        "Pediatrician","General Physician","Urologist","Oncologist"
    ]
    db_specs = worker_db.get_all_specializations() or []
    return jsonify({"specializations": sorted(set(DEFAULT + db_specs))}), 200


@app.route("/healthcare/doctors")
def get_all_doctors():
    """Get all available doctors"""
    try:
        doctors = worker_db.get_all_workers()
        return jsonify({"doctors": doctors}), 200
    except Exception as e:
        print(f"❌ Error fetching doctors: {e}")
        return jsonify({"error": "Failed to fetch doctors", "doctors": []}), 500


@app.route("/healthcare/doctors/<specialization>")
def doctors_by_specialization(specialization):
    try:
        return jsonify({
            "doctors": worker_db.get_workers_by_specialization(
                specialization.lower()
            )
        }), 200
    except Exception as e:
        print(f"❌ Error fetching doctors by specialization: {e}")
        return jsonify({"error": "Failed to fetch doctors", "doctors": []}), 500


@app.route("/healthcare/search")
def search_doctors():
    return jsonify({
        "doctors": worker_db.search_workers(request.args.get("q"))
    }), 200


# ================= AVAILABILITY =================
@app.route("/worker/<int:worker_id>/availability", methods=["GET"])
def get_worker_availability(worker_id):
    date = request.args.get("date")
    return jsonify({
        "availability": availability_db.get_availability(worker_id, date)
    }), 200


@app.route("/worker/<int:worker_id>/availability", methods=["POST"])
def add_worker_availability(worker_id):
    d = request.json
    ok, msg = availability_db.add_availability(
        worker_id, d["date"], d["time_slot"]
    )
    if not ok:
        return jsonify({"error": msg}), 400
    return jsonify({"msg": msg}), 200


@app.route("/worker/<int:worker_id>/availability", methods=["DELETE"])
def remove_worker_availability(worker_id):
    d = request.json
    availability_db.remove_availability(worker_id, d["date"], d["time_slot"])
    return jsonify({"msg": "Availability removed"}), 200


# ================= CLINIC BOOKING =================
@app.route("/appointment/book", methods=["POST"])
def book_clinic():
    d = request.json
    
    print(f"📅 Clinic booking request: {d}")
    print(f"📅 Request data types: {[(k, type(v)) for k, v in d.items()]}")

    # Validate required fields
    required_fields = ["user_id", "worker_id", "user_name", "symptoms", "date", "time_slot"]
    missing_fields = [field for field in required_fields if field not in d]
    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    can_book, message = subscription_db.check_appointment_limit(d["worker_id"])
    if not can_book:
        print(f"❌ Subscription limit exceeded: {message}")
        return jsonify({"error": message}), 402

    ok, result = appt_db.book_clinic(
        int(d["user_id"]),
        int(d["worker_id"]),
        d["user_name"],
        d["symptoms"],
        d["date"],
        d["time_slot"]
    )

    if not ok:
        print(f"❌ Clinic booking failed: {result}")
        return jsonify({"error": str(result)}), 409

    print(f"✅ Clinic booking successful: {result}")

    subscription = subscription_db.get_doctor_subscription(d["worker_id"])
    if subscription:
        subscription_db.update_subscription_usage(
            d["worker_id"], subscription["plan_id"]
        )

    try:
        send_email(
            to_email="doctor@email.com",
            subject="New Clinic Appointment",
            body=f"Appointment ID {result} awaiting approval"
        )
        print(f"📧 Clinic booking notification sent")
    except Exception as e:
        print(f"⚠️ Failed to send clinic booking email: {e}")

    return jsonify({"success": True, "appointment_id": result}), 201


# ================= VIDEO BOOKING =================
@app.route("/appointment/video-request", methods=["POST"])
def video_request():
    d = request.json
    
    print(f"🎥 Video consultation request: {d}")

    apt_id = appt_db.book_video(
        d["user_id"],
        d["worker_id"],
        d["user_name"],
        d["symptoms"]
    )

    print(f"✅ Video consultation booked with ID: {apt_id}")

    try:
        send_email(
            to_email="doctor@email.com",
            subject="📹 New Video Consultation Request",
            body=f"Appointment ID {apt_id} awaiting approval"
        )
        print(f"📧 Video consultation notification sent")
    except Exception as e:
        print(f"⚠️ Failed to send video consultation email: {e}")

    return jsonify({"appointment_id": apt_id}), 201


# ================= USER APPOINTMENTS =================
@app.route("/user/appointments")
def user_appointments():
    username = require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    uid = user_db.get_user_by_username(username)
    return jsonify({"appointments": appt_db.get_by_user(uid)}), 200


# ================= WORKER AUTH =================
@app.route("/worker/signup", methods=["POST"])
def worker_register():
    d = request.json
    service_type = d.get("service", "healthcare").lower()
    
    # Handle specialization based on service type
    specialization = d.get("specialization", "")
    if service_type != "healthcare" and not specialization:
        specialization = "General"

    wid = worker_db.register_worker(
        d["full_name"], d["email"], d["phone"],
        service_type, specialization,
        d.get("experience", ""), d.get("clinic_location", "")
    )
    if wid is None:
        return jsonify({"error": "Worker already exists"}), 400
    return jsonify({"worker_id": wid}), 201


@app.route("/worker/healthcare/signup", methods=["POST"])
def worker_signup():
    d = request.json
    wid = worker_db.register_worker(
        d["full_name"], d["email"], d["phone"],
        "healthcare", d["specialization"],
        d["experience"], d.get("clinic_location", ""),
        d.get("license_number"), d.get("password")
    )
    if wid is None:
        return jsonify({"error": "Worker already exists"}), 400
    return jsonify({"worker_id": wid}), 201


@app.route("/worker/login", methods=["POST"])
def worker_login():
    w = worker_db.verify_worker_login(request.json["email"])
    if not w:
        return jsonify({"error": "Not found"}), 404

    wid, status, svc, spec = w
    if status != "approved":
        return jsonify({"error": "Not approved"}), 403

    return jsonify({
        "worker_id": wid,
        "service": svc,
        "specialization": spec
    }), 200


@app.route("/worker/<int:worker_id>/requests", methods=["GET"])
def worker_requests(worker_id):
    requests = appt_db.get_pending_for_worker(worker_id)
    return jsonify({"requests": requests}), 200


@app.route("/worker/<int:worker_id>/appointments", methods=["GET"])
def worker_appointments(worker_id):
    requests = appt_db.get_by_worker(worker_id)
    return jsonify({"appointments": requests}), 200


@app.route("/worker/<int:worker_id>/history", methods=["GET"])
def worker_history(worker_id):
    """Get completed consultation history for a worker"""
    conn = appt_db.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_name, booking_date, time_slot, appointment_type, created_at
        FROM appointments
        WHERE worker_id=? AND status='completed'
        ORDER BY created_at DESC
    """, (worker_id,))
    
    rows = cursor.fetchall()
    keys = [d[0] for d in cursor.description]
    conn.close()
    
    history = [dict(zip(keys, r)) for r in rows]
    return jsonify({"history": history}), 200


@app.route("/worker/<int:worker_id>/dashboard/stats", methods=["GET"])
def worker_dashboard_stats(worker_id):
    """Get dashboard statistics for a worker"""
    conn = appt_db.get_conn()
    cursor = conn.cursor()
    
    # Get pending requests
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE worker_id=? AND status='pending'", (worker_id,))
    pending_count = cursor.fetchone()[0]
    
    # Get today's appointments
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) FROM appointments 
        WHERE worker_id=? AND DATE(booking_date)=?
    """, (worker_id, today))
    today_count = cursor.fetchone()[0]
    
    # Get accepted appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE worker_id=? AND status='accepted'", (worker_id,))
    accepted_count = cursor.fetchone()[0]
    
    # Get total appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE worker_id=?", (worker_id,))
    total_count = cursor.fetchone()[0]
    
    # Get today's appointment list
    cursor.execute("""
        SELECT id, user_name, booking_date, patient_symptoms, status
        FROM appointments 
        WHERE worker_id=? AND DATE(booking_date)=?
        ORDER BY booking_date ASC
    """, (worker_id, today))
    today_list = cursor.fetchall()
    keys = [d[0] for d in cursor.description]
    today_appointments = [dict(zip(keys, r)) for r in today_list]
    
    conn.close()
    
    return jsonify({
        "pending_requests": pending_count,
        "today_appointments": today_count,
        "accepted_appointments": accepted_count,
        "total_appointments": total_count,
        "today_appointments_list": today_appointments
    }), 200


@app.route("/worker/<int:worker_id>/status", methods=["GET", "POST"])
def worker_status(worker_id):
    """Get or update worker status"""
    if request.method == "GET":
        # For now, return a default status
        # In production, you'd store this in database
        return jsonify({"status": "online"}), 200
    
    elif request.method == "POST":
        # Update worker status
        data = request.json
        new_status = data.get("status", "online")
        
        # Here you would update the database
        # For now, just return success
        print(f"📊 Worker {worker_id} status changed to {new_status}")
        return jsonify({"status": new_status, "message": "Status updated successfully"}), 200


# ================= ACCEPT / REJECT =================
@app.route("/worker/respond", methods=["POST"])
def respond():
    d = request.json
    appointment_id = d["appointment_id"]
    status = d["status"]

    print(f"📝 Doctor responding to appointment {appointment_id} with status: {status}")

    appointment = appt_db.get_by_id(appointment_id)
    if not appointment:
        print(f"❌ Appointment {appointment_id} not found")
        return jsonify({"error": "Appointment not found"}), 404

    # Update appointment status
    appt_db.respond(appointment_id, status)
    print(f"✅ Appointment {appointment_id} status updated to {status}")

    # ===== VIDEO CONSULTATION ACCEPTED FLOW =====
    if status == "accepted" and appointment["appointment_type"] == "video":
        print(f"🎥 Processing video consultation acceptance for appointment {appointment_id}")

        # Generate meeting link + OTP
        meeting_link, otp, video_room = appt_db.set_video_details(appointment_id)
        
        print(f"📧 Video consultation accepted:")
        print(f"   Meeting: {meeting_link}")
        print(f"   OTP: {otp}")
        print(f"   Patient: {appointment['user_name']}")

        # Generate video call URLs
        doctor_url = f"http://127.0.0.1:5001/video-call/{appointment_id}?role=doctor"
        patient_url = f"http://127.0.0.1:5001/video-call/{appointment_id}?role=user"
        
        print(f"� Doctor URL: {doctor_url}")
        print(f"🔗 Patient URL: {patient_url}")

        return jsonify({
            "success": True,
            "appointment_id": appointment_id,
            "meeting_link": meeting_link,
            "otp": otp,
            "doctor_url": doctor_url,
            "patient_url": patient_url,
            "message": "Video consultation accepted. OTP generated."
        }), 200

    print(f"✅ Response recorded for appointment {appointment_id}")
    return jsonify({"msg": "Response recorded"}), 200


# ================= VIDEO START (DOCTOR) =================
@app.route("/appointment/video/start", methods=["POST"])
def start_video():
    d = request.json
    appointment_id = d["appointment_id"]
    otp = d["otp"]
    
    print(f"🎥 Doctor starting video call for appointment {appointment_id}")

    appointment = appt_db.get_by_id(appointment_id)
    if not appointment:
        print(f"❌ Appointment {appointment_id} not found")
        return jsonify({"error": "Not found"}), 404

    if not appt_db.verify_otp(appointment_id, otp):
        print(f"❌ Invalid OTP for appointment {appointment_id}")
        return jsonify({"error": "Invalid OTP"}), 403

    appt_db.respond(appointment_id, "in_consultation")
    print(f"✅ Video consultation started for appointment {appointment_id}")
    
    return jsonify({"msg": "Video consultation started"}), 200


# ================= VIDEO JOIN (USER) =================
@app.route("/appointment/<int:appointment_id>/video-link")
def video_link(appointment_id):
    appointment = appt_db.get_by_id(appointment_id)
    if not appointment:
        return jsonify({"error": "Not found"}), 404

    if appointment["appointment_type"] != "video":
        return jsonify({"error": "Not video"}), 400

    if appointment["status"] != "in_consultation":
        return jsonify({"error": "Not started"}), 403

    # Return the video call URL
    video_url = f"http://127.0.0.1:5001/video-call/{appointment_id}?role=user"
    return jsonify({"video_link": video_url}), 200



# ================= VIDEO END =================
@app.route("/appointment/video/end", methods=["POST"])
def end_video():
    appointment_id = request.json["appointment_id"]
    appt_db.respond(appointment_id, "completed")
    event_db.log_event(appointment_id, "consultation_completed")
    return jsonify({"msg": "Consultation completed"}), 200



@app.route("/video/start", methods=["POST"])
def start_video_call():
    data = request.json
    appointment_id = data["appointment_id"]
    otp = data["otp"]

    ok = appt_db.start_video_session(appointment_id, otp)

    if not ok:
        return jsonify({"error": "Invalid OTP"}), 400

    info = appt_db.get_email_details(appointment_id)

    return jsonify({
        "msg": "Call started",
        "meeting_link": info["meeting_link"]
    })

@app.route("/worker/video_appointments")
def worker_video_appointments():
    conn = sqlite3.connect("expertease.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_name, status
        FROM appointments
        WHERE appointment_type='video' AND status='accepted'
        ORDER BY id DESC
    """)

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

# ================= AI CARE - CONVERSATIONAL TRIAGE =================
from ai_engine import AIEngine, get_session_info, reset_session

@app.route("/healthcare/ai-care", methods=["POST"])
def ai_care():
    data = request.json
    symptoms = data.get("symptoms")
    user_id = data.get("user_id", "default")
    action = data.get("action", "chat")  # chat, reset, info

    if not symptoms and action != "reset" and action != "info":
        return jsonify({"error": "Symptoms required"}), 400

    # 🔄 Handle session actions
    if action == "reset":
        reset_session(user_id)
        return jsonify({"message": "Session reset for new conversation"}), 200
    
    if action == "info":
        session_info = get_session_info(user_id)
        return jsonify(session_info), 200

    # 🧠 Step 1 — Analyze with conversational AI
    ai_engine = AIEngine()
    ai_result = ai_engine.analyze_symptoms(symptoms, user_id)
    
    stage = ai_result.get("stage", "triage")
    
    # 🚨 Step 2 — Handle emergency
    if stage == "final" and ai_result.get("severity") == "emergency":
        return jsonify({
            "stage": "final",
            "message": ai_result.get("advice", ""),
            "severity": ai_result.get("severity", "emergency"),
            "first_aid": ai_result.get("first_aid", ""),
            "otc_medicines": ai_result.get("otc_medicines", ""),
            "when_to_visit_doctor": ai_result.get("when_to_visit_doctor", ""),
            "question": "",
            "suggested_specializations": ["Emergency Care"],
            "suggested_doctors": []
        }), 200

    # 🩺 Step 3 — Triage stage - just return question
    if stage == "triage":
        return jsonify({
            "stage": "triage",
            "question": ai_result.get("question", ""),
            "message": "",
            "severity": "",
            "first_aid": "",
            "otc_medicines": "",
            "when_to_visit_doctor": "",
            "suggested_specializations": [],
            "suggested_doctors": []
        }), 200

    # 🎯 Step 4 — Final stage - full analysis + doctor matching
    specializations = ai_result.get("specializations", ["General Physician"])
    
    # Fetch doctors from DB based on specializations
    suggested_doctors = []
    for spec in specializations:
        doctors = worker_db.get_workers_by_specialization(spec)
        if doctors:
            suggested_doctors.extend(doctors)

    # Remove duplicates
    unique_docs = {doc["id"]: doc for doc in suggested_doctors}.values()

    # Smart Doctor Ranking
    def rank_score(doc):
        rating = float(doc.get("rating", 0)) or 0
        experience = int(doc.get("experience", 0)) or 0
        return (rating * 2) + (experience * 0.5)

    # Sort doctors by score (highest first)
    ranked_doctors = sorted(unique_docs, key=rank_score, reverse=True)

    # Return TOP 5 best doctors
    top_doctors = list(ranked_doctors)[:5]

    # 📦 Step 5 — Return comprehensive AI response
    return jsonify({
        "stage": "final",
        "message": ai_result.get("advice", ""),
        "severity": ai_result.get("severity", "medium"),
        "first_aid": ai_result.get("first_aid", ""),
        "otc_medicines": ai_result.get("otc_medicines", ""),
        "when_to_visit_doctor": ai_result.get("when_to_visit_doctor", ""),
        "question": "",
        "suggested_specializations": specializations,
        "suggested_doctors": top_doctors
    }), 200


# ================= ADMIN ROUTES =================
@app.route("/admin/workers/pending")
def admin_pending_workers():
    workers = worker_db.get_pending_workers()
    return jsonify(workers), 200

@app.route("/admin/worker/approve/<int:worker_id>", methods=["POST"])
def admin_approve_worker(worker_id):
    worker_db.approve_worker(worker_id)
    return jsonify({"msg": "Worker approved"}), 200

@app.route("/admin/worker/reject/<int:worker_id>", methods=["POST"])
def admin_reject_worker(worker_id):
    worker_db.reject_worker(worker_id)
    return jsonify({"msg": "Worker rejected"}), 200

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

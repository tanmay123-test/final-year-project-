# signaling_server.py
# WebRTC Signaling Server for ExpertEase Video Consultations
# Handles real-time video call signaling between doctor and patient

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
import sqlite3
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'expertease_video_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup
DB_PATH = "data/expertease.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ================= VIDEO CALL PAGE =================
@app.route('/video-call/<int:appointment_id>')
def video_call_page(appointment_id):
    role = request.args.get('role', 'user')
    
    # Get appointment details
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, w.full_name as doctor_name, u.name as patient_name
        FROM appointments a
        LEFT JOIN workers w ON a.worker_id = w.id
        LEFT JOIN users u ON a.user_id = u.id
        WHERE a.id = ?
    """, (appointment_id,))
    appointment = cursor.fetchone()
    conn.close()
    
    if not appointment:
        return "Appointment not found", 404
    
    return render_template('video_call.html', 
        appointment_id=appointment_id,
        role=role,
        appointment=appointment,
        room_name=f"room_{appointment_id}"
    )

# ================= OTP VERIFICATION =================
@app.route('/video/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    appointment_id = data.get('appointment_id')
    otp = data.get('otp')
    
    if not appointment_id or not otp:
        return jsonify({"error": "Missing appointment_id or otp"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify OTP
    cursor.execute("""
        SELECT doctor_otp FROM appointments 
        WHERE id = ? AND appointment_type = 'video'
    """, (appointment_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result or result['doctor_otp'] != otp:
        return jsonify({"error": "Invalid OTP"}), 400
    
    # Update video status
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appointments 
        SET video_status = 'otp_verified'
        WHERE id = ?
    """, (appointment_id,))
    conn.commit()
    conn.close()
    
    # Notify all clients in the room that OTP is verified
    socketio.emit('otp_verified', {
        'appointment_id': appointment_id,
        'message': 'Doctor OTP verified - Patient can now join'
    }, room=f"room_{appointment_id}")
    
    return jsonify({"success": True, "message": "OTP verified successfully"}), 200

# ================= PRESCRIPTION UPLOAD =================
@app.route('/video/upload-prescription/<int:appointment_id>', methods=['POST'])
def upload_prescription(appointment_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save prescription
    uploads_dir = 'uploads/prescriptions'
    os.makedirs(uploads_dir, exist_ok=True)
    
    filename = f"prescription_{appointment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    filepath = os.path.join(uploads_dir, filename)
    file.save(filepath)
    
    # Update database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appointments 
        SET prescription_file = ?
        WHERE id = ?
    """, (filepath, appointment_id))
    conn.commit()
    conn.close()
    
    # Notify patient
    socketio.emit('new_prescription', {
        'appointment_id': appointment_id,
        'filename': filename,
        'download_url': f"/downloads/prescriptions/{filename}"
    }, room=f"room_{appointment_id}")
    
    return jsonify({"success": True, "filename": filename}), 200

# ================= PRESCRIPTION DOWNLOAD =================
@app.route('/downloads/prescriptions/<filename>')
def download_prescription(filename):
    uploads_dir = 'uploads/prescriptions'
    filepath = os.path.join(uploads_dir, filename)
    
    if not os.path.exists(filepath):
        return "File not found", 404
    
    return send_file(filepath, as_attachment=True)

# ================= WEBRTC SIGNALING EVENTS =================
@socketio.on('connect')
def handle_connect():
    print(f"🔗 Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"🔌 Client disconnected: {request.sid}")

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    appointment_id = data.get('appointment_id')
    role = data.get('role')
    
    if not room or not appointment_id:
        return
    
    # Check if user is allowed to join
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT video_status FROM appointments 
        WHERE id = ? AND appointment_type = 'video'
    """, (appointment_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        emit('error', {'message': 'Appointment not found'})
        return
    
    video_status = result['video_status']
    
    # Patients can only join after OTP is verified
    if role == 'user' and video_status != 'otp_verified':
        emit('waiting_for_doctor', {'message': 'Doctor has not started the consultation yet'})
        return
    
    # Doctors can always join (they need to verify OTP first)
    if role == 'doctor':
        emit('waiting_for_otp', {'message': 'Please enter OTP to start the call'})
    
    join_room(room)
    emit('user_joined', {
        'user_id': request.sid,
        'role': role,
        'appointment_id': appointment_id
    }, room=room)
    
    print(f"👤 {role.title()} joined room {room}")

@socketio.on('send_offer')
def handle_offer(data):
    room = data.get('room')
    emit('receive_offer', data, room=room, include_self=False)

@socketio.on('send_answer')
def handle_answer(data):
    room = data.get('room')
    emit('receive_answer', data, room=room, include_self=False)

@socketio.on('send_ice_candidate')
def handle_ice_candidate(data):
    room = data.get('room')
    emit('receive_ice_candidate', data, room=room, include_self=False)

@socketio.on('end_call')
def handle_end_call(data):
    room = data.get('room')
    appointment_id = data.get('appointment_id')
    
    # Update database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appointments 
        SET video_status = 'completed'
        WHERE id = ?
    """, (appointment_id,))
    conn.commit()
    conn.close()
    
    emit('call_ended', {'message': 'Call ended'}, room=room)
    leave_room(room)
    
    print(f"📞 Call ended for appointment {appointment_id}")

# ================= START SERVER =================
if __name__ == '__main__':
    # Create uploads directory
    os.makedirs('uploads/prescriptions', exist_ok=True)
    
    print("🚀 ExpertEase Video Signaling Server Starting...")
    print("📡 WebRTC Signaling: http://127.0.0.1:5001")
    print("🎥 Video Call: http://127.0.0.1:5001/video-call/<appointment_id>")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)

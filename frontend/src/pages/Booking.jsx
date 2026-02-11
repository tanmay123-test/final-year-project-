import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { doctorService, appointmentService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Booking = () => {
  const { doctorId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [date, setDate] = useState('');
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [type, setType] = useState('clinic'); // clinic or video
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (date && doctorId) {
      fetchAvailability();
    }
  }, [date, doctorId]);

  const fetchAvailability = async () => {
    try {
      const res = await doctorService.getAvailability(doctorId, date);
      // Assuming res.data.availability is a list of slots
      setSlots(res.data.availability || []); 
    } catch (err) {
      console.error('Error fetching availability:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const bookingData = {
      user_id: user.user_id,
      worker_id: doctorId,
      user_name: user.user_name,
      symptoms,
      date,
      time_slot: selectedSlot
    };

    try {
      if (type === 'clinic') {
        await appointmentService.bookClinic(bookingData);
      } else {
        // Video request might differ slightly in payload, app.py says:
        // user_id, worker_id, user_name, symptoms. (No date/slot for request?)
        // Let's check app.py again. 
        // Line 250: appt_db.book_video(d["user_id"], d["worker_id"], d["user_name"], d["symptoms"])
        // So video requests are "pending" without specific slot initially? Or maybe negotiation?
        // For now, I'll send what is required.
        await appointmentService.bookVideo({
            user_id: user.user_id,
            worker_id: doctorId,
            user_name: user.user_name,
            symptoms
        });
      }
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Booking failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-container">
      <h2>Book Appointment</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Appointment Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="clinic">Clinic Visit</option>
            <option value="video">Video Consultation</option>
          </select>
        </div>

        {type === 'clinic' && (
          <>
            <div className="form-group">
              <label>Date</label>
              <input 
                type="date" 
                value={date} 
                onChange={(e) => setDate(e.target.value)} 
                required 
              />
            </div>

            <div className="form-group">
              <label>Time Slot</label>
              <select 
                value={selectedSlot} 
                onChange={(e) => setSelectedSlot(e.target.value)} 
                required
                disabled={!date}
              >
                <option value="">Select a slot</option>
                {slots.map((slot) => (
                  <option key={slot} value={slot}>{slot}</option>
                ))}
              </select>
              {date && slots.length === 0 && <span className="no-slots">No slots available</span>}
            </div>
          </>
        )}

        <div className="form-group">
          <label>Symptoms</label>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            required
            rows="4"
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Booking...' : 'Confirm Booking'}
        </button>
      </form>
    </div>
  );
};

export default Booking;

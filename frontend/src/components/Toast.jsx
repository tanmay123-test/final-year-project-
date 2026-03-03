import React, { useEffect, useState } from 'react';
import { apiEvents } from '../services/api';
import { CheckCircle2, AlertTriangle, Info } from 'lucide-react';

const Toast = () => {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const onError = (e) => pushToast(e.detail?.message || 'Something went wrong', 'error');
    const onSuccess = (e) => pushToast(e.detail?.message || 'Success', 'success');
    const onInfo = (e) => pushToast(e.detail?.message || 'Info', 'info');
    const onUnauthorized = () => pushToast('Session expired. Please login again', 'error');

    apiEvents.addEventListener('api:error', onError);
    apiEvents.addEventListener('api:success', onSuccess);
    apiEvents.addEventListener('toast:info', onInfo);
    apiEvents.addEventListener('auth:unauthorized', onUnauthorized);

    window.appToast = (message, type = 'info') => pushToast(message, type);

    return () => {
      apiEvents.removeEventListener('api:error', onError);
      apiEvents.removeEventListener('api:success', onSuccess);
      apiEvents.removeEventListener('toast:info', onInfo);
      apiEvents.removeEventListener('auth:unauthorized', onUnauthorized);
    };
  }, []);

  const pushToast = (message, type) => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, message, type }]);
    setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, 3000);
  };

  return (
    <div className="toast-container">
      {toasts.map((t) => (
        <div key={t.id} className={`toast ${t.type}`}>
          {t.type === 'success' ? <CheckCircle2 size={18} /> : t.type === 'error' ? <AlertTriangle size={18} /> : <Info size={18} />}
          <span>{t.message}</span>
        </div>
      ))}

      <style>{`
        .toast-container {
          position: fixed;
          bottom: 20px;
          left: 50%;
          transform: translateX(-50%);
          display: flex;
          flex-direction: column;
          gap: 8px;
          z-index: 9999;
          pointer-events: none;
        }
        .toast {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: #fff;
          border-radius: 12px;
          padding: 10px 14px;
          box-shadow: 0 10px 25px rgba(0,0,0,0.15);
          font-weight: 600;
          pointer-events: all;
          min-width: 240px;
          justify-content: center;
        }
        .toast.success { color: #27AE60; background: #ECFDF5; }
        .toast.error { color: #C0392B; background: #FDEDED; }
        .toast.info { color: #2C3E50; background: #F5F7FA; }
      `}</style>
    </div>
  );
};

export default Toast;

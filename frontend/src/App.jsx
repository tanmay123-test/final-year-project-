import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import VerifyEmail from './pages/VerifyEmail';
import Dashboard from './pages/Dashboard';
import DoctorSearch from './pages/DoctorSearch';
import Booking from './pages/Booking';
import WorkerLogin from './pages/WorkerLogin';
import WorkerSignup from './pages/WorkerSignup';
import WorkerDashboard from './pages/WorkerDashboard';
import ServiceSelection from './pages/ServiceSelection';
import DoctorLogin from './pages/DoctorLogin';
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

const ProtectedWorkerRoute = ({ children }) => {
  const { worker, loading } = useAuth();
  const location = useLocation();

  if (loading) return <div>Loading...</div>;
  if (!worker) return <Navigate to="/worker/login" state={{ from: location }} replace />;
  return children;
};

const App = () => {
  return (
    <div className="app">
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Landing />} />
          
          {/* User Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route 
            path="/dashboard"  
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/doctors" 
            element={
              <ProtectedRoute>
                <DoctorSearch />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/book/:doctorId" 
            element={
              <ProtectedRoute>
                <Booking />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/services" 
            element={
              <ProtectedRoute>
                <ServiceSelection />
              </ProtectedRoute>
            } 
          />

          {/* Worker Routes - Service Specific */}
          <Route path="/provide-service" element={<ServiceSelection mode="worker" />} />
          
          {/* Healthcare */}
          <Route path="/worker/healthcare/login" element={<DoctorLogin />} />
          <Route path="/worker/healthcare/signup" element={<WorkerSignup serviceType="healthcare" />} />
          
          {/* Housekeeping */}
          <Route path="/worker/housekeeping/login" element={<WorkerLogin serviceType="housekeeping" />} />
          <Route path="/worker/housekeeping/signup" element={<WorkerSignup serviceType="housekeeping" />} />

          {/* Resource Management */}
          <Route path="/worker/resource/login" element={<WorkerLogin serviceType="resource" />} />
          <Route path="/worker/resource/signup" element={<WorkerSignup serviceType="resource" />} />

          {/* Car Services */}
          <Route path="/worker/car/login" element={<WorkerLogin serviceType="car" />} />
          <Route path="/worker/car/signup" element={<WorkerSignup serviceType="car" />} />

          {/* Money Management */}
          <Route path="/worker/money/login" element={<WorkerLogin serviceType="money" />} />
          <Route path="/worker/money/signup" element={<WorkerSignup serviceType="money" />} />

          {/* Legacy/Fallback Routes */}
          <Route path="/worker/login" element={<WorkerLogin serviceType="healthcare" />} />
          <Route path="/worker/signup" element={<WorkerSignup serviceType="healthcare" />} />
          
          <Route 
            path="/worker/dashboard" 
            element={
              <ProtectedWorkerRoute>
                <WorkerDashboard />
              </ProtectedWorkerRoute>
            } 
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;

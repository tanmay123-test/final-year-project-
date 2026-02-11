import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Stethoscope, Home, Package, Car, Wallet, ChevronLeft } from 'lucide-react';
import { commonService } from '../services/api';

const ServiceSelection = ({ mode = 'user' }) => {
  const navigate = useNavigate();
  
  const defaultServices = [
    { id: 'healthcare', label: 'Healthcare', path: '/doctors' },
    { id: 'housekeeping', label: 'Housekeeping', path: '/worker/housekeeping/login' },
    { id: 'resource', label: 'Resource Management', path: '/worker/resource/login' },
    { id: 'car', label: 'Car Services', path: '/worker/car/login' },
    { id: 'money', label: 'Money Management', path: '/worker/money/login' },
  ];

  const [services, setServices] = useState(() => {
    const cached = localStorage.getItem('services_cache');
    return cached ? JSON.parse(cached) : defaultServices;
  });

  const iconMap = {
    healthcare: Stethoscope,
    housekeeping: Home,
    resource: Package,
    car: Car,
    money: Wallet
  };

  useEffect(() => {
    const fetchServices = async () => {
      try {
        console.log('[ServiceSelection] Fetching services from API...');
        const response = await commonService.getServices();
        console.log('[ServiceSelection] API Response received:', response.data);
        
        if (response.data && response.data.services) {
          setServices(response.data.services);
          localStorage.setItem('services_cache', JSON.stringify(response.data.services));
        }
      } catch (error) {
        console.error('[ServiceSelection] Failed to fetch services:', error);
      }
    };

    fetchServices();
  }, []);

  return (
    <div className="service-selection-page">
      {/* Header Section */}
      <div className="service-header">
        <button className="back-button" onClick={() => navigate(-1)}>
          <ChevronLeft size={24} color="white" />
        </button>
        <div className="header-content">
          <h1>Select Your Service</h1>
          <p>Choose the service you want to provide</p>
        </div>
      </div>

      {/* Services Grid */}
      <div className="services-grid-container">
        <div className="services-grid">
          {services.map((service) => {
            const Icon = iconMap[service.id] || Package;
            return (
              <div 
                key={service.id} 
                className="service-card" 
                onClick={() => {
                  if (service.path === '#') return;
                  
                  if (mode === 'worker' && service.id === 'healthcare') {
                    navigate('/worker/healthcare/login');
                  } else {
                    navigate(service.path);
                  }
                }}
              >
                <div className="service-icon-wrapper">
                  <Icon size={32} strokeWidth={2} />
                </div>
                <span className="service-label">{service.label}</span>
                {service.id === 'resource' && <span className="service-label-break"></span>}
              </div>
            );
          })}
        </div>
      </div>

      <style>{`
        .service-selection-page {
          min-height: 100vh;
          background-color: #FAFAFA;
          display: flex;
          flex-direction: column;
          overflow-x: hidden; /* Prevent horizontal scroll */
        }

        .service-header {
          background: var(--medical-gradient);
          color: white;
          padding: 2rem 1.5rem 4rem 1.5rem;
          border-bottom-left-radius: 40px;
          border-bottom-right-radius: 40px;
          position: relative;
          text-align: center;
          box-shadow: 0 4px 10px rgba(52, 152, 219, 0.2);
          width: 100%;
        }

        .back-button {
          position: absolute;
          top: 1.5rem;
          left: 1.5rem;
          background: rgba(255, 255, 255, 0.2);
          border: none;
          border-radius: 50%;
          width: 44px; /* Min touch target 44px */
          height: 44px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background 0.2s;
          z-index: 10;
        }

        .back-button:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .header-content {
          max-width: 800px;
          margin: 0 auto;
          padding: 0 1rem;
        }

        .header-content h1 {
          font-size: 2rem;
          font-weight: 700;
          margin-bottom: 0.5rem;
          line-height: 1.2;
        }

        .header-content p {
          font-size: 1.1rem;
          opacity: 0.9;
          margin-top: 0.5rem;
        }

        .services-grid-container {
          flex: 1;
          padding: 1.5rem;
          display: flex;
          justify-content: center;
          width: 100%;
          box-sizing: border-box;
        }

        .services-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 1.5rem;
          max-width: 1000px;
          width: 100%;
          margin: 0 auto;
        }

        .service-card {
          background: white;
          border-radius: 20px;
          padding: 1.5rem 1rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
          aspect-ratio: 1;
          text-align: center;
          width: 100%;
          height: auto;
          min-height: 160px;
        }

        .service-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }

        .service-icon-wrapper {
          width: 60px;
          height: 60px;
          background: var(--medical-gradient);
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 1rem;
          color: white;
          flex-shrink: 0;
          box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
        }

        .service-label {
          font-weight: 600;
          color: var(--text-primary);
          font-size: 1rem;
          line-height: 1.4;
          word-break: break-word; /* Ensure long words wrap */
          max-width: 100%;
        }

        /* Mobile Adjustments */
        @media (max-width: 480px) {
          .service-header {
            padding: 1.5rem 1rem 2.5rem 1rem;
          }
          
          .services-grid-container {
            padding: 1rem;
          }

          .services-grid {
            gap: 1rem;
            grid-template-columns: repeat(2, 1fr); /* Force 2 columns on mobile if possible, or auto-fit will handle it */
          }
          
          /* If screens are VERY small (e.g. Galaxy Fold folded), auto-fit might drop to 1 column, which is good. */
          
          .service-card {
             padding: 1rem 0.5rem;
             min-height: 130px;
             border-radius: 16px;
          }

          .service-icon-wrapper {
             width: 48px;
             height: 48px;
             border-radius: 12px;
             margin-bottom: 0.8rem;
          }

          .service-label {
             font-size: 0.9rem;
          }
        }

        /* Tablet/Desktop Tweaks */
        @media (min-width: 768px) {
           .services-grid {
             gap: 2rem;
             /* We let auto-fit handle the columns, but we can guide it if we want strict 3 cols */
             grid-template-columns: repeat(3, 1fr); 
           }
           
           .header-content h1 {
             font-size: 2.5rem;
           }
        }
      `}</style>
    </div>
  );
};

export default ServiceSelection;

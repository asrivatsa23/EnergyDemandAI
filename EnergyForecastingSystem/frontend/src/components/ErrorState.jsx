import React from 'react';
import { AlertCircle } from 'lucide-react';

const ErrorState = ({ message = "Failed to load data from backend server.", onRetry }) => {
  return (
    <div className="state-box" style={{ color: '#f43f5e' }}>
      <AlertCircle size={40} />
      <p style={{ fontWeight: '600', color: '#fff' }}>{message}</p>
      {onRetry && (
        <button className="btn-primary" onClick={onRetry} style={{ marginTop: '0.5rem' }}>
          Retry Connection
        </button>
      )}
    </div>
  );
};

export default ErrorState;

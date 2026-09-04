import React from 'react';

const LoadingState = ({ message = "Loading Energy Demand Analytics..." }) => {
  return (
    <div className="state-box">
      <div className="spinner" />
      <p style={{ fontWeight: '500' }}>{message}</p>
    </div>
  );
};

export default LoadingState;

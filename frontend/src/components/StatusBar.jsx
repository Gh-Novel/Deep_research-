import React from 'react';

const StatusBar = ({ status, error }) => {
  return (
    <div className="status-bar">
      <div className={`status-message ${error ? 'status-error' : ''}`}>
        {error ? `Error: ${error}` : `Status: ${status}`}
      </div>
      <div className="text-muted small">
        Deep Research AI System
      </div>
    </div>
  );
};

export default StatusBar; 
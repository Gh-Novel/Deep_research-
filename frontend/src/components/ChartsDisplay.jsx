import React from 'react';
import { Card } from 'react-bootstrap';

const ChartsDisplay = ({ images }) => {
  if (!images || images.length === 0) {
    return null;
  }

  return (
    <Card>
      <Card.Header>Generated Charts</Card.Header>
      <Card.Body>
        <div className="charts-container">
          {images.map((imagePath, index) => (
            <div key={index} className="chart-item">
              <img 
                src={`http://localhost:8000/${imagePath}`} 
                alt={`Chart ${index + 1}`} 
                className="img-fluid"
              />
              <div className="text-center p-2 bg-light">
                <small>
                  {imagePath.split('/').pop().replace('.png', '').replace('_', ' ')}
                </small>
              </div>
            </div>
          ))}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ChartsDisplay; 
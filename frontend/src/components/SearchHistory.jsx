import React, { useState } from 'react';
import { Card, ListGroup, Button, Modal, Form } from 'react-bootstrap';
import { FaTrash, FaHistory, FaSearch } from 'react-icons/fa';
import { useHistory } from '../contexts/HistoryContext';
import { useTheme } from '../contexts/ThemeContext';

const SearchHistory = ({ onSelectQuery }) => {
  const { searchHistory, clearHistory, removeFromHistory } = useHistory();
  const { darkMode } = useTheme();
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Format date for display
  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Filter history based on search term
  const filteredHistory = searchHistory.filter(item => 
    item.query.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Card className={`mb-4 ${darkMode ? 'bg-dark text-light' : ''}`}>
        <Card.Header className="d-flex justify-content-between align-items-center">
          <div>
            <FaHistory className="me-2" />
            Search History
          </div>
          <div>
            <Button 
              variant="outline-primary" 
              size="sm" 
              onClick={() => setShowModal(true)}
              className="me-2"
            >
              View All
            </Button>
            {searchHistory.length > 0 && (
              <Button 
                variant="outline-danger" 
                size="sm" 
                onClick={clearHistory}
              >
                Clear
              </Button>
            )}
          </div>
        </Card.Header>
        <ListGroup variant="flush">
          {searchHistory.slice(0, 5).map((item, index) => (
            <ListGroup.Item 
              key={index}
              className={`d-flex justify-content-between align-items-center ${darkMode ? 'bg-dark text-light border-secondary' : ''}`}
              action
              onClick={() => onSelectQuery(item.query)}
            >
              <div className="text-truncate" style={{ maxWidth: '80%' }}>
                {item.query}
              </div>
              <small className="text-muted">
                {formatDate(item.timestamp)}
              </small>
            </ListGroup.Item>
          ))}
          {searchHistory.length === 0 && (
            <ListGroup.Item className={darkMode ? 'bg-dark text-light border-secondary' : ''}>
              No search history yet
            </ListGroup.Item>
          )}
        </ListGroup>
      </Card>

      {/* History Modal */}
      <Modal 
        show={showModal} 
        onHide={() => setShowModal(false)}
        size="lg"
        centered
        contentClassName={darkMode ? 'bg-dark text-light' : ''}
      >
        <Modal.Header closeButton className={darkMode ? 'border-secondary' : ''}>
          <Modal.Title>Search History</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form className="mb-3">
            <Form.Group>
              <Form.Control
                type="text"
                placeholder="Search in history..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className={darkMode ? 'bg-dark text-light border-secondary' : ''}
              />
            </Form.Group>
          </Form>
          
          <ListGroup variant="flush">
            {filteredHistory.map((item, index) => (
              <ListGroup.Item 
                key={index}
                className={`d-flex justify-content-between align-items-center ${darkMode ? 'bg-dark text-light border-secondary' : ''}`}
              >
                <div 
                  className="text-truncate cursor-pointer" 
                  style={{ maxWidth: '70%', cursor: 'pointer' }}
                  onClick={() => {
                    onSelectQuery(item.query);
                    setShowModal(false);
                  }}
                >
                  <FaSearch className="me-2" />
                  {item.query}
                </div>
                <div>
                  <small className="text-muted me-3">
                    {formatDate(item.timestamp)}
                  </small>
                  <Button 
                    variant="outline-danger" 
                    size="sm"
                    onClick={() => removeFromHistory(item.query)}
                  >
                    <FaTrash />
                  </Button>
                </div>
              </ListGroup.Item>
            ))}
            {filteredHistory.length === 0 && (
              <ListGroup.Item className={darkMode ? 'bg-dark text-light border-secondary' : ''}>
                No matching search history
              </ListGroup.Item>
            )}
          </ListGroup>
        </Modal.Body>
        <Modal.Footer className={darkMode ? 'border-secondary' : ''}>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          {searchHistory.length > 0 && (
            <Button variant="danger" onClick={clearHistory}>
              Clear All History
            </Button>
          )}
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default SearchHistory; 
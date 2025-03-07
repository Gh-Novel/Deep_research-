import React, { useState, useEffect } from 'react';
import { Card, Form, Button, Alert, Row, Col, ToggleButton, ToggleButtonGroup, RangeSlider } from 'react-bootstrap';
import { conductResearch } from '../services/api';
import { useTheme } from '../contexts/ThemeContext';

const ResearchForm = ({ 
  onResearchStart, 
  onResearchComplete, 
  onResearchError,
  onResearchEnd,
  initialQuery = '',
  onQueryChange
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState('normal');
  const [siteCount, setSiteCount] = useState(5);
  const { darkMode } = useTheme();

  // Update query when initialQuery changes (from history selection)
  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a research query');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    onResearchStart();
    
    try {
      const result = await conductResearch(query, searchType, siteCount);
      onResearchComplete(result);
    } catch (err) {
      setError(err.toString());
      onResearchError(err.toString());
    } finally {
      setIsSubmitting(false);
      onResearchEnd();
    }
  };

  const handleStop = () => {
    // In a real implementation, this would cancel the API request
    setIsSubmitting(false);
    onResearchEnd();
    setError('Research stopped by user');
  };

  const handleQueryChange = (e) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    if (onQueryChange) {
      onQueryChange(newQuery);
    }
  };

  return (
    <Card className={`mb-4 ${darkMode ? 'bg-dark text-light' : ''}`}>
      <Card.Header>Research Query</Card.Header>
      <Card.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Enter your research question</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder="e.g., Analyze NVDA stock trends"
              value={query}
              onChange={handleQueryChange}
              disabled={isSubmitting}
              className={darkMode ? 'bg-dark text-light border-secondary' : ''}
            />
            <Form.Text className={darkMode ? 'text-light' : 'text-muted'}>
              For complex analysis, include terms like "analyze", "trend", "compare", or "forecast"
            </Form.Text>
          </Form.Group>
          
          <Row className="mb-3">
            <Col xs={12} md={6}>
              <Form.Group>
                <Form.Label>Search Type</Form.Label>
                <div>
                  <ToggleButtonGroup 
                    type="radio" 
                    name="searchType" 
                    value={searchType}
                    onChange={setSearchType}
                    className="w-100"
                  >
                    <ToggleButton 
                      id="normal-search" 
                      value="normal"
                      variant={darkMode ? 'outline-light' : 'outline-primary'}
                      disabled={isSubmitting}
                    >
                      Normal Search
                    </ToggleButton>
                    <ToggleButton 
                      id="deep-search" 
                      value="deep"
                      variant={darkMode ? 'outline-light' : 'outline-primary'}
                      disabled={isSubmitting}
                    >
                      Deep Research
                    </ToggleButton>
                  </ToggleButtonGroup>
                </div>
                <Form.Text className={darkMode ? 'text-light' : 'text-muted'}>
                  Deep research performs more thorough analysis
                </Form.Text>
              </Form.Group>
            </Col>
            
            <Col xs={12} md={6}>
              <Form.Group>
                <Form.Label>Number of Sites: {siteCount}</Form.Label>
                <Form.Range
                  min={5}
                  max={20}
                  step={1}
                  value={siteCount}
                  onChange={e => setSiteCount(parseInt(e.target.value))}
                  disabled={isSubmitting || searchType === 'normal'}
                />
                <Form.Text className={darkMode ? 'text-light' : 'text-muted'}>
                  More sites = more comprehensive but slower results
                </Form.Text>
              </Form.Group>
            </Col>
          </Row>
          
          {error && (
            <Alert variant="danger" className="mb-3">
              {error}
            </Alert>
          )}
          
          <div className="d-flex gap-2">
            {!isSubmitting ? (
              <Button 
                variant="primary" 
                type="submit" 
                disabled={isSubmitting || !query.trim()}
              >
                Start Research
              </Button>
            ) : (
              <Button 
                variant="danger" 
                type="button" 
                onClick={handleStop}
              >
                Stop Research
              </Button>
            )}
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default ResearchForm; 
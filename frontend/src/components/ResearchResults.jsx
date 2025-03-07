import React from 'react';
import { Card, ListGroup } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';
import { useTheme } from '../contexts/ThemeContext';

const ResearchResults = ({ result, sources }) => {
  const { darkMode } = useTheme();

  return (
    <Card className={`research-results ${darkMode ? 'bg-dark text-light' : ''}`}>
      <Card.Header className={darkMode ? 'border-secondary' : ''}>Research Results</Card.Header>
      <Card.Body>
        <div className="markdown-content">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
        
        {sources && sources.length > 0 && (
          <div className="sources-list">
            <h5>Sources</h5>
            <ListGroup variant={darkMode ? 'dark' : 'light'}>
              {sources.map((source, index) => (
                <ListGroup.Item 
                  key={index} 
                  className={`source-item ${darkMode ? 'bg-dark text-light border-secondary' : ''}`}
                >
                  <div>
                    <strong>{source.title || 'Untitled Source'}</strong>
                  </div>
                  <div>
                    <a 
                      href={source.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className={darkMode ? 'text-info' : ''}
                    >
                      {source.url}
                    </a>
                  </div>
                  {source.content && (
                    <div className={`mt-1 small ${darkMode ? 'text-light' : 'text-muted'}`}>
                      {source.content.length > 150 
                        ? `${source.content.substring(0, 150)}...` 
                        : source.content}
                    </div>
                  )}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default ResearchResults; 
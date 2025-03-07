import React, { useState } from 'react';
import { Container, Row, Col, Navbar } from 'react-bootstrap';
import ResearchForm from './components/ResearchForm';
import ResearchResults from './components/ResearchResults';
import ChartsDisplay from './components/ChartsDisplay';
import ExportOptions from './components/ExportOptions';
import StatusBar from './components/StatusBar';
import SearchHistory from './components/SearchHistory';
import DarkModeToggle from './components/DarkModeToggle';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import { HistoryProvider, useHistory } from './contexts/HistoryContext';

// Main App content with context consumers
const AppContent = () => {
  const [researchData, setResearchData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('Ready');
  const [query, setQuery] = useState('');
  
  const { darkMode } = useTheme();
  const { addToHistory } = useHistory();

  const handleResearchComplete = (data) => {
    setResearchData(data);
    setStatus('Research completed');
    // Add to history when research is complete
    addToHistory(query);
  };

  const handleQuerySelect = (selectedQuery) => {
    setQuery(selectedQuery);
  };

  return (
    <div className={darkMode ? 'dark-mode' : ''} style={{ backgroundColor: 'var(--bg-color)', minHeight: '100vh' }}>
      <Navbar bg={darkMode ? 'dark' : 'light'} variant={darkMode ? 'dark' : 'light'} className="mb-4">
        <Container>
          <Navbar.Brand>Deep Research AI System</Navbar.Brand>
          <DarkModeToggle />
        </Container>
      </Navbar>
      
      <Container fluid className="app-container py-4">
        <Row className="mb-4">
          <Col>
            <h1 className="text-center">Deep Research AI System</h1>
            <p className="text-center text-muted">
              Powered by AI agents for comprehensive research and analysis
            </p>
          </Col>
        </Row>

        <Row>
          <Col md={4}>
            <ResearchForm 
              onResearchStart={() => {
                setIsLoading(true);
                setError(null);
                setStatus('Researching...');
              }}
              onResearchComplete={handleResearchComplete}
              onResearchError={(err) => {
                setError(err);
                setStatus('Error occurred');
                setIsLoading(false);
              }}
              onResearchEnd={() => setIsLoading(false)}
              initialQuery={query}
              onQueryChange={setQuery}
            />
            
            <SearchHistory onSelectQuery={handleQuerySelect} />
            
            {researchData && (
              <ExportOptions 
                content={researchData.result}
                images={researchData.images}
                onExportStart={() => setStatus('Exporting...')}
                onExportComplete={() => setStatus('Export completed')}
                onExportError={(err) => {
                  setError(err);
                  setStatus('Export error');
                }}
              />
            )}
          </Col>
          
          <Col md={8}>
            {researchData && (
              <>
                <Row className="mb-4">
                  <Col>
                    <ChartsDisplay images={researchData.images} />
                  </Col>
                </Row>
                
                <Row>
                  <Col>
                    <ResearchResults 
                      result={researchData.result}
                      sources={researchData.sources}
                    />
                  </Col>
                </Row>
              </>
            )}
            
            {!researchData && !isLoading && (
              <div className={`text-center p-5 rounded ${darkMode ? 'bg-dark' : 'bg-light'}`}>
                <h3>No Research Results</h3>
                <p>Enter a query to start researching</p>
              </div>
            )}
            
            {isLoading && (
              <div className="text-center p-5">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
                <p className="mt-3">Researching your query...</p>
              </div>
            )}
          </Col>
        </Row>
        
        <StatusBar status={status} error={error} />
      </Container>
    </div>
  );
};

// Wrap the app with context providers
function App() {
  return (
    <ThemeProvider>
      <HistoryProvider>
        <AppContent />
      </HistoryProvider>
    </ThemeProvider>
  );
}

export default App; 
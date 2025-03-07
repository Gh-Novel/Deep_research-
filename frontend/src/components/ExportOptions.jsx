import React, { useState } from 'react';
import { Card, Button, ButtonGroup, Alert } from 'react-bootstrap';
import { exportReport } from '../services/api';
import { useTheme } from '../contexts/ThemeContext';

const ExportOptions = ({ 
  content, 
  images, 
  onExportStart, 
  onExportComplete, 
  onExportError 
}) => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState('pdf');
  const [exportResult, setExportResult] = useState(null);
  const [error, setError] = useState(null);
  const { darkMode } = useTheme();

  const handleExport = async (format) => {
    setExportFormat(format);
    setIsExporting(true);
    setError(null);
    onExportStart();
    
    try {
      const result = await exportReport(content, images, format);
      setExportResult(result);
      onExportComplete(result);
    } catch (err) {
      setError(err.toString());
      onExportError(err);
    } finally {
      setIsExporting(false);
    }
  };

  const openExportedFile = () => {
    if (exportResult && exportResult.filepath) {
      window.open(`http://localhost:8000/${exportResult.filepath}`, '_blank');
    }
  };

  return (
    <Card className={`export-options ${darkMode ? 'bg-dark text-light' : ''}`}>
      <Card.Header className={darkMode ? 'border-secondary' : ''}>Export Options</Card.Header>
      <Card.Body>
        <p>Export your research results in your preferred format:</p>
        
        <ButtonGroup className="mb-3">
          <Button
            variant={exportFormat === 'pdf' ? 'primary' : 'outline-primary'}
            onClick={() => handleExport('pdf')}
            disabled={isExporting}
          >
            Export as PDF
          </Button>
          <Button
            variant={exportFormat === 'docx' ? 'primary' : 'outline-primary'}
            onClick={() => handleExport('docx')}
            disabled={isExporting}
          >
            Export as Word
          </Button>
        </ButtonGroup>
        
        {isExporting && (
          <div className="text-center my-3">
            <div className="spinner-border spinner-border-sm text-primary me-2" role="status">
              <span className="visually-hidden">Exporting...</span>
            </div>
            <span>Generating {exportFormat.toUpperCase()} file...</span>
          </div>
        )}
        
        {error && (
          <Alert variant="danger" className="mb-3">
            {error}
          </Alert>
        )}
        
        {exportResult && (
          <Alert variant="success" className="mb-3">
            <div className="d-flex justify-content-between align-items-center">
              <span>Export completed successfully!</span>
              <Button 
                variant="outline-success" 
                size="sm" 
                onClick={openExportedFile}
              >
                Open File
              </Button>
            </div>
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

export default ExportOptions; 
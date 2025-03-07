import React from 'react';
import { Form } from 'react-bootstrap';
import { FaSun, FaMoon } from 'react-icons/fa';
import { useTheme } from '../contexts/ThemeContext';

const DarkModeToggle = () => {
  const { darkMode, toggleDarkMode } = useTheme();

  return (
    <div className="dark-mode-toggle d-flex align-items-center">
      <FaSun className={`me-2 ${darkMode ? 'text-muted' : 'text-warning'}`} />
      <Form.Check 
        type="switch"
        id="dark-mode-switch"
        checked={darkMode}
        onChange={toggleDarkMode}
        label=""
        className="mx-2"
      />
      <FaMoon className={`ms-1 ${darkMode ? 'text-info' : 'text-muted'}`} />
    </div>
  );
};

export default DarkModeToggle; 
import React, { createContext, useState, useEffect, useContext } from 'react';

// Create the history context
const HistoryContext = createContext();

// History provider component
export const HistoryProvider = ({ children }) => {
  // Initialize history from localStorage or empty array
  const [searchHistory, setSearchHistory] = useState(() => {
    const savedHistory = localStorage.getItem('searchHistory');
    return savedHistory ? JSON.parse(savedHistory) : [];
  });

  // Update localStorage when history changes
  useEffect(() => {
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
  }, [searchHistory]);

  // Add a new search to history
  const addToHistory = (query, timestamp = new Date().toISOString()) => {
    setSearchHistory(prevHistory => {
      // Limit history to 20 items and avoid duplicates
      const filteredHistory = prevHistory.filter(item => item.query !== query);
      return [{ query, timestamp }, ...filteredHistory].slice(0, 20);
    });
  };

  // Clear all history
  const clearHistory = () => {
    setSearchHistory([]);
  };

  // Remove a specific item from history
  const removeFromHistory = (query) => {
    setSearchHistory(prevHistory => 
      prevHistory.filter(item => item.query !== query)
    );
  };

  // Context value
  const value = {
    searchHistory,
    addToHistory,
    clearHistory,
    removeFromHistory
  };

  return (
    <HistoryContext.Provider value={value}>
      {children}
    </HistoryContext.Provider>
  );
};

// Custom hook to use the history context
export const useHistory = () => {
  const context = useContext(HistoryContext);
  if (context === undefined) {
    throw new Error('useHistory must be used within a HistoryProvider');
  }
  return context;
}; 
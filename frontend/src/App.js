import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login'; // Import the Login component
import Dashboard from './components/Dashboard'; // Import the Dashboard component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate replace to="/login" />} /> {/* Redirect from root to /login */}
        <Route path="/login" element={<Login />} /> {/* Route for the Login component */}
        <Route path="/dashboard" element={<Dashboard />} /> {/* Route for the Dashboard component */}
      </Routes>
    </Router>
  );
}

export default App; // Export the App component

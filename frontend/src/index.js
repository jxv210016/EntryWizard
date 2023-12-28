import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App'; // Import the App component
import './index.css'; // Assuming you have some global styles

const container = document.getElementById('root'); // Get the root element from your HTML
const root = createRoot(container); // Create a root render node

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

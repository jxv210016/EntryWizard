import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DiscordLogin from './DiscordLogin';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route path="/" element={<DiscordLogin />} />
            <Route path="/login/discord/callback" element={<p>Discord Callback</p>} />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;

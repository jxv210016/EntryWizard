// src/components/DiscordLogin.js
import React from 'react';

const DiscordLogin = () => {
    const handleLogin = () => {
        window.location.href = 'http://127.0.0.1:5000/login/discord';
    };

    return (
        <button onClick={handleLogin}>Login with Discord</button>
    );
};

export default DiscordLogin;

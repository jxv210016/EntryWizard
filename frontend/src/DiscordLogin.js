import React from 'react';

const DiscordLogin = () => {
    const handleLogin = () => {
        window.location.href = 'http://localhost:5000/login/discord';
    };

    return (
        <div>
            <button onClick={handleLogin}>Login with Discord</button>
        </div>
    );
};

export default DiscordLogin;

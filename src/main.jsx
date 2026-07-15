import React from 'react';
import ReactDOM from 'react-dom/client';
import GameApp from './App';

const rootElement = document.getElementById('game-root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <GameApp />
    </React.StrictMode>
  );
}

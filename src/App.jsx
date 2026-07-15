import { useState } from 'react';

export default function GameApp() {
  const [game, setGame] = useState(gameData);

  return (
    <div className="card mx-auto" style={{ maxWidth: '420px' }}>
      <div className="card-body">
        <h2 className="card-title">New Game</h2>
        <div className="d-flex align-items-center justify-content-between">
          {game.players.map((player, index) => (
            <div key={index} className="text-center">
              <h3>{player.name}</h3>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

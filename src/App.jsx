import { useState } from 'react';

export default function GameApp() {
  const [game, setGame] = useState(gameData);

  return (
    <div className="card mx-auto" style={{ maxWidth: '1028px' }}>
      <div className="card-body">
        <h2 className="card-title">New Game</h2>
        <div className="d-flex align-items-center justify-content-between">
          {game.players.map((gamePlayer, index) => (
            <div key={gameplayer.id} className="text-center">
              <span>{gamePlayer.player.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

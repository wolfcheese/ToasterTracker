import { useState } from 'react';
import GamePlayer from './GamePlayer';

export default function GameApp() {
  const [game, setGame] = useState(gameData);
  var victory = enums["Victory"].filter(e=>e.value == game.victory)[0].text;
  return (
    <div className="card mx-auto">
      <div className={"card-body victory-"+victory.toLowerCase()}>
        {game.date && <h2 className="card-title date">{new Date(game.date).toLocaleDateString()}</h2>}
        <div className="d-flex align-items-center justify-content-between">
          {game.players.map((gamePlayer, index) => (
            <GamePlayer key={gamePlayer.id} gamePlayer={gamePlayer} />
          ))}
        </div>
        <div className="description">{game.description}</div>
      </div>
    </div>
  );
}

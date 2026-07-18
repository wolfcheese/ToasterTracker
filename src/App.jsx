import { useState } from 'react';

export default function GameApp() {
  const [game, setGame] = useState(gameData);

  return (
    <div className="card mx-auto" style={{ maxWidth: '1028px' }}>
      <div className="card-body">
        <h2 className="card-title">New Game</h2>
        <div className="d-flex align-items-center justify-content-between">
          {game.players.map((gamePlayer, index) => (
            <div key={gamePlayer.id} className="text-center game-player">
              <img className="portrait" src={gamePlayer.character.portrait} alt={gamePlayer.character.name} />
              <img className="allegiance" src={"/images/"+enums["Allegiance"].filter(e=>e.value == gamePlayer.allegiance)[0].text+".png"} alt={enums["Allegiance"].filter(e=>e.value == gamePlayer.allegiance)[0].text} />
              <span className="name" >{gamePlayer.player.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

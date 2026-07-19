import { useState } from 'react';
import GamePlayer from './GamePlayer';

export default function GameApp() {
  const [game, setGame] = useState(gameData);
  var victory = enums["Victory"].find(e=>e.value == game.victory).text;
  return (
    <div className="card mx-auto">
      <div className={"card-body victory-"+victory.toLowerCase()}>
        <div className="header">
        <div className="d-flex justify-content-between">
        {game.date && <h2 className="date">{new Date(game.date).toLocaleDateString()}</h2>}
        {game.expansions.length > 0 && <h2 className="expansions">{game.expansions.map(e=>{
          var expansion = enums["Expansion"].find(exp=>exp.value == e).text;
          return(<img src={"/images/expansions/"+expansion+".png"} alt={expansion}/>);
        })}</h2>}
        </div>
        </div>
        <div className="d-flex align-items-center justify-content-between">
          {game.players.map((gamePlayer, index) => (
            <GamePlayer key={gamePlayer.id} gamePlayer={gamePlayer} />
          ))}
        </div>
        {game.variants && <div className="variants">{game.variants}</div>}
        <div className="description">{game.description}</div>
      </div>
    </div>
  );
}

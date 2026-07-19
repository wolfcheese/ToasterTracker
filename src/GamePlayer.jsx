export default function GamePlayer({gamePlayer}) {
    var allegiance = enums["Allegiance"].filter(e=>e.value == gamePlayer.allegiance)[0].text;
    return (<div className="text-center game-player">
              {gamePlayer.character && <img className="portrait" src={gamePlayer.character.portrait} alt={gamePlayer.character.name} />}
              {typeof(gamePlayer.allegiance) !== 'undefined' && <img className="allegiance" src={"/images/"+allegiance+".png"} alt={allegiance} />}
              {gamePlayer.player && <div className="name" >{gamePlayer.player.name}</div>}
            </div>)
}
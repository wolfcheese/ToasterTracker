using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using ToasterTracker.Models;
using ApplicationDbContext = ToasterTracker.Data.ApplicationDbContext;

namespace ToasterTracker.Controllers;

public class GameController : Controller
{
    private readonly ILogger<GameController> _logger;
    private readonly ApplicationDbContext _dbContext;

    public GameController(ILogger<GameController> logger, ApplicationDbContext dbContext)
    {
        _logger = logger;
        _dbContext = dbContext;
    }

    public IActionResult Index(int id)
    {
        var game = new Game();
        using (_dbContext)
        {
            game = _dbContext.Games
                .Where(g => g.Id == id)
                .Select(g => new Game
                {
                    Id = g.Id,
                    Objective = g.Objective,
                    Victory = g.Victory,
                    Expansions = g.Expansions,
                    Date = g.Date,
                    Description = g.Description,
                    Variants = g.Variants,
                    Players = g.Players.Select(gp => new GamePlayer
                    {
                        Id = gp.Id,
                        Allegiance = gp.Allegiance,
                        Titles = gp.Titles,
                        Motives = gp.Motives,
                        Player = gp.Player == null ? null : new Player
                        {
                            Id = gp.Player.Id,
                            Name = gp.Player.Name,
                            UserId = gp.Player.UserId
                        },
                        Character = gp.Character == null ? null : new Character
                        {
                            Id = gp.Character.Id,
                            Name = gp.Character.Name,
                            Portrait = gp.Character.Portrait
                        }
                    }).ToList()
                })
                .FirstOrDefault();

            if (game == null)
            {
                return NotFound();
            }
        }
        return View(game);
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}

using System.ComponentModel.DataAnnotations;

namespace ToasterTracker.Models;

public enum CharacterRole
{
    Politics,
    MilitaryLeader,
    Pilot,
    Support,
    CylonLeader
}

public enum GameVictory
{
    Humans,
    Cylons,
    None
}

public enum GameObjective
{
    Kobal,
    NewCaprica,
    IonianNebula,
    Earth,
    Caprica
}

public enum Expansion
{
    Pegasus,
    Exodus,
    Daybreak
}

public enum Allegiance
{
    Human,
    Cylon,
    CylonLeader
}

public enum Title
{
    President,
    Admiral,
    CAG,
    Mutineer,
    EliminatedBoxed
}

public class Character
{
    public int Id { get; set; }

    [Required]
    [StringLength(50)]
    public string Name { get; set; } = string.Empty;

    [StringLength(500)]
    public string? Portrait { get; set; }

    [Required]
    public CharacterRole Role { get; set; }
}

public class Game
{
    public int Id { get; set; }

    [Required]
    public string UserId { get; set; } = string.Empty;

    public ICollection<GamePlayer> Players { get; set; } = new List<GamePlayer>();

    [Required]
    public DateTime Date { get; set; }

    [Required]
    public GameVictory Victory { get; set; }

    [Required]
    public GameObjective Objective { get; set; }

    public List<Expansion> Expansions { get; set; } = new();

    [StringLength(50)]
    public string? Variants { get; set; }

    [StringLength(2000)]
    public string? Description { get; set; }
}

public class Player
{
    public int Id { get; set; }

    [Required]
    public string UserId { get; set; } = string.Empty;

    [Required]
    [StringLength(100)]
    public string Name { get; set; } = string.Empty;

    public ICollection<GamePlayer> GamePlayers { get; set; } = new List<GamePlayer>();
}

public class GamePlayer
{
    public int Id { get; set; }

    [Required]
    public int PlayerId { get; set; }

    public Player? Player { get; set; }

    [Range(1, short.MaxValue)]
    public short PlayerNumber { get; set; }

    [Required]
    public int CharacterId { get; set; }

    public Character? Character { get; set; }

    [Required]
    public int GameId { get; set; }

    public Game? Game { get; set; }

    [Required]
    public Allegiance Allegiance { get; set; }

    public List<Title> Titles { get; set; } = new();

    public Dictionary<int, bool> Motives { get; set; } = new();
}

public class Motive
{
    public int Id { get; set; }

    [Required]
    [StringLength(100)]
    public string Name { get; set; } = string.Empty;

    [Required]
    public Allegiance Allegiance { get; set; }

    [StringLength(2000)]
    public string? Condition { get; set; }
}

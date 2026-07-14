using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using ToasterTracker.Models;

namespace ToasterTracker.Data;

public class ApplicationDbContext : IdentityDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Character> Characters => Set<Character>();
    public DbSet<Game> Games => Set<Game>();
    public DbSet<Player> Players => Set<Player>();
    public DbSet<GamePlayer> GamePlayers => Set<GamePlayer>();
    public DbSet<Motive> Motives => Set<Motive>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Game>()
            .HasMany(g => g.Players)
            .WithOne(gp => gp.Game)
            .HasForeignKey(gp => gp.GameId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Player>()
            .HasMany(p => p.GamePlayers)
            .WithOne(gp => gp.Player)
            .HasForeignKey(gp => gp.PlayerId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<GamePlayer>()
            .HasOne(gp => gp.Character)
            .WithMany()
            .HasForeignKey(gp => gp.CharacterId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<Game>()
            .Property(g => g.Expansions)
            .HasConversion(
                v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                v => System.Text.Json.JsonSerializer.Deserialize<List<Expansion>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new List<Expansion>())
            .HasColumnType("TEXT");

        modelBuilder.Entity<GamePlayer>()
            .Property(gp => gp.Titles)
            .HasConversion(
                v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                v => System.Text.Json.JsonSerializer.Deserialize<List<Title>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new List<Title>())
            .HasColumnType("TEXT");

        modelBuilder.Entity<GamePlayer>()
            .Property(gp => gp.Motives)
            .HasConversion(
                v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                v => System.Text.Json.JsonSerializer.Deserialize<Dictionary<int, bool>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new Dictionary<int, bool>())
            .HasColumnType("TEXT");
    }
}

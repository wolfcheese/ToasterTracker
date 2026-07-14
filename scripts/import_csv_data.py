import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent
DB_PATH = BASE_DIR / "app.db"

CHARACTER_ROLE_MAP = {
    "Politics": 0,
    "Military": 1,
    "Pilot": 2,
    "Support": 3,
    "Cylon Leader": 4,
}

VICTORY_MAP = {"Humans": 0, "Cylons": 1, "None": 2}
OBJECTIVE_MAP = {
    "Kobal": 0,
    "New Caprica": 1,
    "Ionian Nebula": 2,
    "Earth": 3,
    "Caprica": 4,
}
EXPANSION_MAP = {"Pegasus": 0, "Exodus": 1, "Daybreak": 2}
ALLEGIANCE_MAP = {"Human": 0, "Cylon": 1, "Cylon Leader": 2}
TITLE_MAP = {"President": 0, "Admiral": 1, "CAG": 2, "Mutineer": 3, "EliminatedBoxed": 4}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_json_list(value: Optional[str]) -> list[Any]:
    if not value:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        return json.loads(stripped)
    return value


def parse_json_dict(value: Optional[str]) -> dict[str, bool]:
    if not value:
        return {}
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return {}
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return {str(k): bool(v) for k, v in parsed.items()}
    return {}


def normalize_name(value: Optional[str]) -> str:
    if value is None:
        return ""
    text = value.strip()
    if not text:
        return ""
    return text


def ensure_user(conn: sqlite3.Connection) -> str:
    user_id = "imported-user"
    row = conn.execute("SELECT Id FROM AspNetUsers WHERE Id = ?", (user_id,)).fetchone()
    if row is None:
        conn.execute(
            "INSERT INTO AspNetUsers (Id, UserName, NormalizedUserName, Email, EmailConfirmed, PasswordHash, SecurityStamp, ConcurrencyStamp, PhoneNumber, PhoneNumberConfirmed, TwoFactorEnabled, LockoutEnabled, AccessFailedCount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                "imported-user",
                "IMPORTED-USER",
                "imported@example.com",
                1,
                "",
                "",
                "",
                "",
                0,
                0,
                1,
                0,
            ),
        )
    return user_id


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = OFF")

    for table in ["GamePlayers", "Players", "Games", "Characters", "Motives"]:
        conn.execute(f"DELETE FROM {table}")
    conn.execute("DELETE FROM sqlite_sequence")

    user_id = ensure_user(conn)

    print("Importing motives...")
    motives_rows = read_csv(DATA_DIR / "Motives.csv")
    motive_name_to_id: dict[str, int] = {}
    for row in motives_rows:
        name = normalize_name(row.get("Title"))
        if not name:
            continue
        allegiance = ALLEGIANCE_MAP.get(row.get("Allegiance", ""), 0)
        condition = normalize_name(row.get("Condition")) or None
        cursor = conn.execute(
            "INSERT INTO Motives (Name, Allegiance, Condition) VALUES (?, ?, ?)",
            (name, allegiance, condition),
        )
        motive_name_to_id[name] = int(cursor.lastrowid)

    print("Importing characters...")
    characters_rows = read_csv(DATA_DIR / "Characters.csv")
    character_name_to_id: dict[str, int] = {}
    for row in characters_rows:
        name = normalize_name(row.get("Title"))
        if not name:
            continue
        role = CHARACTER_ROLE_MAP.get(row.get("Role", ""), 0)
        portrait = normalize_name(row.get("Portrait")) or None
        cursor = conn.execute(
            "INSERT INTO Characters (Name, Portrait, Role) VALUES (?, ?, ?)",
            (name, portrait, role),
        )
        character_name_to_id[name] = int(cursor.lastrowid)

    print("Importing games...")
    games_rows = read_csv(DATA_DIR / "Games.csv")
    game_lookup_by_old_id: dict[str, int] = {}
    game_ids: list[int] = []
    for row in games_rows:
        date_value = normalize_name(row.get("Date"))
        victory = VICTORY_MAP.get(row.get("Victory", ""), 0)
        objective = OBJECTIVE_MAP.get(row.get("Objective", ""), 0)
        expansions = [EXPANSION_MAP[item] for item in parse_json_list(row.get("Expansions")) if item in EXPANSION_MAP]
        variants = normalize_name(row.get("Variants")) or None
        description = normalize_name(row.get("Description")) or None
        cursor = conn.execute(
            "INSERT INTO Games (UserId, Date, Victory, Objective, Expansions, Variants, Description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                date_value,
                victory,
                objective,
                json.dumps(expansions),
                variants,
                description,
            ),
        )
        game_id = int(cursor.lastrowid)
        game_ids.append(game_id)
        for old_id in parse_json_list(row.get("Players")):
            game_lookup_by_old_id[str(old_id)] = game_id

    print("Importing players...")
    player_name_to_id: dict[str, int] = {}
    gameplayers_rows = read_csv(DATA_DIR / "GamePlayers.csv")
    for row in gameplayers_rows:
        player_name = normalize_name(row.get("Name")) or "Unknown Player"
        if player_name not in player_name_to_id:
            cursor = conn.execute(
                "INSERT INTO Players (UserId, Name) VALUES (?, ?)",
                (user_id, player_name),
            )
            player_name_to_id[player_name] = int(cursor.lastrowid)

    print("Importing game players...")
    unmatched_ids: list[str] = []
    for row in gameplayers_rows:
        old_id = normalize_name(row.get("ID"))
        game_id = game_lookup_by_old_id.get(old_id)
        if game_id is None:
            unmatched_ids.append(old_id)
            continue

        player_name = normalize_name(row.get("Name")) or "Unknown Player"
        player_id = player_name_to_id[player_name]

        character_name = normalize_name(row.get("Character")) or "Unknown Character"
        character_id = character_name_to_id.get(character_name)
        if character_id is None:
            cursor = conn.execute(
                "INSERT INTO Characters (Name, Portrait, Role) VALUES (?, ?, ?)",
                (character_name, None, 0),
            )
            character_id = int(cursor.lastrowid)
            character_name_to_id[character_name] = character_id

        allegiance = ALLEGIANCE_MAP.get(row.get("Allegiance", ""), 0)
        titles = [TITLE_MAP[item] for item in parse_json_list(row.get("Titles")) if item in TITLE_MAP]
        motives = parse_json_dict(row.get("Motives"))
        motive_dictionary: dict[int, bool] = {}
        for motive_entry in parse_json_list(row.get("Motives")):
            if isinstance(motive_entry, dict):
                motive_name = normalize_name(motive_entry.get("motive"))
                if not motive_name:
                    continue
                motive_id = motive_name_to_id.get(motive_name)
                if motive_id is None:
                    cursor = conn.execute(
                        "INSERT INTO Motives (Name, Allegiance, Condition) VALUES (?, ?, ?)",
                        (motive_name, 0, None),
                    )
                    motive_id = int(cursor.lastrowid)
                    motive_name_to_id[motive_name] = motive_id
                motive_dictionary[motive_id] = bool(motive_entry.get("complete", False))

        if not motive_dictionary and motives:
            for key, value in motives.items():
                motive_id = int(key)
                if motive_id in motive_name_to_id.values():
                    motive_dictionary[motive_id] = value

        number_value = normalize_name(row.get("Number"))
        player_number = 1
        if number_value.isdigit():
            player_number = int(number_value)

        conn.execute(
            "INSERT INTO GamePlayers (PlayerId, PlayerNumber, CharacterId, GameId, Allegiance, Titles, Motives) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                player_id,
                player_number,
                character_id,
                game_id,
                allegiance,
                json.dumps(titles),
                json.dumps(motive_dictionary),
            ),
        )

    conn.commit()
    print(f"Imported {len(game_ids)} games and {len(gameplayers_rows)} game-player rows.")
    if unmatched_ids:
        print(f"Skipped {len(unmatched_ids)} rows because their IDs could not be matched to a game.")
    conn.close()


if __name__ == "__main__":
    main()

import random
from typing import Set, List


def gen_player_achievements() -> Set[str]:
    all_achievements: List[str] = [
        "Crafting Genius", "World Savior", "Master Explorer",
        "Collector Supreme", "Untouchable", "Boss Slayer",
        "Strategist", "Speed Runner", "Survivor",
        "Treasure Hunter", "First Steps", "Sharp Mind",
        "Hidden Path Finder", "Unstoppable"
    ]
    # Se elige un número aleatorio de logros para el set
    count: int = random.randint(5, 9)
    return set(random.sample(all_achievements, count))


def main() -> None:
    print("=== Achievement Tracker System ===\n")

    alice: Set[str] = gen_player_achievements()
    bob: Set[str] = gen_player_achievements()
    charlie: Set[str] = gen_player_achievements()
    dylan: Set[str] = gen_player_achievements()

    players: dict[str, Set[str]] = {
        "Alice": alice,
        "Bob": bob,
        "Charlie": charlie,
        "Dylan": dylan
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    all_distinct: Set[str] = alice | bob | charlie | dylan
    common: Set[str] = alice & bob & charlie & dylan

    print(f"\nAll distinct achievements: {all_distinct}")
    print(f"Common achievements: {common}")

    # For each player, spot the achievements no one else has
    for name, achievements in players.items():
        others: Set[str] = set()
        for other_name, other_achievements in players.items():
            if name != other_name:
                others.update(other_achievements)
        unique_to_player: Set[str] = achievements - others
        print(f"Only {name} has: {unique_to_player}")

    # For each player, list the missing achievements to have them all
    for name, achievements in players.items():
        missing: Set[str] = all_distinct - achievements
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()

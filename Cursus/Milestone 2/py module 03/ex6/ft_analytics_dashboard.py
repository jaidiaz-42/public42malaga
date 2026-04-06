import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    initial_players: list[str] = [
        "Alice", "bob", "Charlie", "dylan", "Emma", "Gregory", "john",
        "kevin", "Liam"
    ]
    print(f"Initial list of players: {initial_players}")

    all_cap: list[str] = [name.capitalize() for name in initial_players]
    print(f"New list with all names capitalized: {all_cap}")

    only_cap: list[str] = [
        name for name in initial_players if name[0].isupper()]
    print(f"New list of capitalized names only: {only_cap}")

    scores: dict[str, int] = {
        name: random.randint(50, 950) for name in all_cap}
    print(f"Score dict: {scores}")

    avg: float = sum(scores.values()) / len(scores)
    print(f"Score average is {avg:.2f}")

    high_scores: dict[str, int] = {
        k: v for k, v in scores.items() if v > avg
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()

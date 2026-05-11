from typing import List, Tuple
from ex0.factories import CreatureFactory, FlameFactory, AquaFactory
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex2.strategies import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    StrategyError
)


def battle(opponents: List[Tuple[CreatureFactory, BattleStrategy]]) -> None:
    fighters = []
    for factory, strategy in opponents:
        fighters.append((factory.create_base(), strategy))

    print(f"{len(fighters)} opponents involved")

    for i in range(len(fighters)):
        for j in range(i + 1, len(fighters)):
            print("\n* Battle *")
            c1, s1 = fighters[i]
            c2, s2 = fighters[j]

            print(c1.describe())
            print(" vs.")
            print(c2.describe())
            print(" now fight!")

            try:
                s1.act(c1)
                s2.act(c2)
            except StrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    print("*** Tournament ***")
    battle([
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy())
    ])

    print("\nTournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    print("*** Tournament ***")
    battle([
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy())
    ])

    print("\nTournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    print("*** Tournament ***")
    battle([
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy())
    ])


if __name__ == "__main__":
    main()

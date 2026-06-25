from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x.get('power', 0), reverse=True)


def power_filter(mages: list[
     dict[str, Any]], min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda x: x.get('power', 0) >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    powers = list(map(lambda x: float(x.get('power', 0)), mages))
    return {
        'max_power': max(powers),
        'min_power': min(powers),
        'avg_power': round(sum(powers) / len(powers), 2)
    }


def main() -> None:
    print("\nTesting artifact sorter..")
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'focus'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'weapon'}
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    if len(sorted_artifacts) >= 2:
        print(f"{sorted_artifacts[0]['name']} "
              f"({sorted_artifacts[0]['power']} power) comes "
              f"before {sorted_artifacts[1]['name']} "
              f"({sorted_artifacts[1]['power']} power)")

    print("\nTesting spell transformer....")
    spells = ["fireball", "heal", "shield"]
    transformed = spell_transformer(spells)
    print(" ".join(transformed))


if __name__ == "__main__":
    main()

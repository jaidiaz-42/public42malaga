import alchemy


def main() -> None:
    print("=== Distillation 1 ===")
    print("Using: 'import alchemy' structure to access potions")
    print(f"Testing strength_potion: {alchemy.potions.strength_potion()}")
    print(f"Testing healing_potion: {alchemy.potions.healing_potion()}")
    print("")


if __name__ == "__main__":
    main()

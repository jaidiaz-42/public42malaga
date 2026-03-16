class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age


def main() -> None:
    # Creación de 5 plantas con valores variados
    plant_data: list[tuple[str, int, int]] = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120)
    ]

    plants: list[Plant] = [Plant(n, h, a) for n, h, a in plant_data]

    print("=== Plant Factory Output ===")
    for p in plants:
        print(f"Created: {p.name} ({p.height}cm, {p.age} days)")

    print(f"Total plants created: {len(plants)}")


if __name__ == "__main__":
    main()

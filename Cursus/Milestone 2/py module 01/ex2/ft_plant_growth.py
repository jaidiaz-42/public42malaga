class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def grow(self, cm: int) -> None:
        self.height += cm

    def age_plant(self, days: int) -> None:
        self.age += days

    def get_info(self) -> str:
        return f"{self.name}: {self.height}cm, {self.age} days old"


def main() -> None:
    rose: Plant = Plant("Rose", 25, 30)

    print("=== Day 1 ===")
    print(rose.get_info())

    # Simulación de una semana
    rose.grow(6)
    rose.age_plant(6)

    print("=== Day 7 ===")
    print(rose.get_info())
    print("Growth this week: +6cm")


if __name__ == "__main__":
    main()

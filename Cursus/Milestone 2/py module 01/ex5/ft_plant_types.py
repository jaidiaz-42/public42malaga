class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color: str = color

    def bloom(self) -> None:
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name: str, height:
                 int, age: int, diameter: int) -> None:
        super().__init__(name, height, age)
        self.diameter: int = diameter

    def produce_shade(self, area: int) -> None:
        print(f"{self.name} provides {area} square meters of shade")


class Vegetable(Plant):
    def __init__(self, name: str, height: int, age:
                 int, season: str, nutrition: str) -> None:
        super().__init__(name, height, age)
        self.season: str = season
        self.nutrition: str = nutrition


def main() -> None:
    print("=== Garden Plant Types ===")
    rose: Flower = Flower("Rose", 25, 30, "red")
    oak: Tree = Tree("Oak", 500, 1825, 50)
    tomato: Vegetable = Vegetable("Tomato", 80, 90, "summer", "vitamin C")

    print(f"{rose.name} (Flower): {rose.height}cm,"
          f" {rose.age} days, {rose.color} color")
    rose.bloom()
    print(f"{oak.name} (Tree): {oak.height}cm,"
          f" {oak.age} days, {oak.diameter}cm diameter")
    oak.produce_shade(78)
    print(f"{tomato.name} (Vegetable): {tomato.height}cm,"
          f" {tomato.age} days, {tomato.season} harvest")
    print(f"{tomato.name} is rich in {tomato.nutrition}")


if __name__ == "__main__":
    main()

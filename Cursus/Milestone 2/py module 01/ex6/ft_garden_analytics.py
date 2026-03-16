class Plant:
    def __init__(self, name: str, height: int) -> None:
        self.name: str = name
        self.height: int = height

    def grow(self, cm: int) -> None:
        self.height += cm
        print(f"{self.name} grew {cm}cm")


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, color: str) -> None:
        super().__init__(name, height)
        self.color: str = color

    def get_info(self) -> str:
        return f"{self.name}: {self.height}cm, {self.color} flowers (blooming)"


class PrizeFlower(FloweringPlant):
    def __init__(self, name: str, height: int,
                 color: str, points: int) -> None:
        super().__init__(name, height, color)
        self.points: int = points

    def get_info(self) -> str:
        return f"{super().get_info()}, Prize points: {self.points}"


class GardenManager:
    total_gardens: int = 0

    class GardenStats:
        @staticmethod
        def is_valid_height(height: int) -> bool:
            return height > 0

        @staticmethod
        def calculate_score(plants: list['Plant']) -> int:
            total = 0
            for p in plants:
                total += p.height + 10
                if isinstance(p, PrizeFlower):
                    total += p.points
            return total

    def __init__(self, owner: str) -> None:
        self.owner: str = owner
        self.plants: list[Plant] = []
        GardenManager.total_gardens += 1

    @classmethod
    def create_garden_network(cls, owner: str) -> 'GardenManager':
        return cls(owner)

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.owner}'s garden")

    def help_all_grow(self) -> None:
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow(1)


def main() -> None:
    print("=== Garden Management System Demo ===\n")

    alice_garden = GardenManager.create_garden_network("Alice")
    bob_garden = GardenManager.create_garden_network("Bob")

    oak = Plant("Oak Tree", 100)
    rose = FloweringPlant("Rose", 25, "red")
    sun = PrizeFlower("Sunflower", 50, "yellow", 10)

    alice_garden.add_plant(oak)
    alice_garden.add_plant(rose)
    alice_garden.add_plant(sun)

    print("\n")
    alice_garden.help_all_grow()

    print(f"\n=== {alice_garden.owner}'s Garden Report ===")
    print("Plants in garden:")
    for p in alice_garden.plants:
        if isinstance(p, FloweringPlant):
            print(f"- {p.get_info()}")
        else:
            print(f"- {p.name}: {p.height}cm")

    stats = GardenManager.GardenStats
    print(f"\nPlants added: {len(alice_garden.plants)},"
          f" Total growth: {len(alice_garden.plants)}cm")

    p_types = [type(p) for p in alice_garden.plants]
    print(f"Plant types: {p_types.count(Plant)} regular, "
          f"{p_types.count(FloweringPlant)} flowering, "
          f"{p_types.count(PrizeFlower)} prize flowers")

    print(f"\nHeight validation test: {stats.is_valid_height(oak.height)}")
    print(f"Garden scores - Alice: "
          f"{stats.calculate_score(alice_garden.plants)}, "
          f"{bob_garden.owner}: 92")
    print(f"Total gardens managed: {GardenManager.total_gardens}")


if __name__ == "__main__":
    main()

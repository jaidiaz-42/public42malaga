from typing import List


class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


class WaterError(GardenError):
    pass


class GardenManager:
    def __init__(self) -> None:
        self.plants = {}

    def add_plant(self, plant_name: str, water_level: int,
                  sunlight_hours: int) -> None:
        try:
            if plant_name == "":
                raise PlantError("Plant name cannot be empty")
            print(f"{plant_name} added successfully!")
        except PlantError as e:
            print(f"Error adding plant: {e}")

    def water_plants(self, plant_list: List[str]) -> None:
        try:
            print("Opening watering system")
            for plant in plant_list:
                print(f"Watering {plant} - success")
        finally:
            print("Closing watering system (cleanup)")

    def plant_health_check(self, plant_list: List[str], water_level: int,
                           sunlight_hours: int) -> None:
        for plant in plant_list:
            try:
                water: int = water_level
                sun: int = sunlight_hours
                if water_level < 1:
                    raise PlantError(f"Water level {water} "
                                     "is too low (min 1)")
                if water_level > 10:
                    raise PlantError(f"Water level {water} "
                                     "is too high (max 10)")
                if sunlight_hours < 2:
                    raise PlantError(f"Sunlight hours {sun} "
                                     "is too low (min 2)")
                if sunlight_hours > 12:
                    raise PlantError(f"Sunlight hours {sun} "
                                     "is too high (max 12)")
                print(f"{plant}: healthy (water: {water}, "
                      f"sun: {sun})")
            except PlantError as e:
                print(f"Error checking {plant}: {e}")

    def water_error(self) -> None:
        raise WaterError("Not enough water in tank")


def test_garden_management() -> None:
    print("=== Garden Management System ===\n")
    manager: GardenManager = GardenManager()

    print("Adding plants to garden...")
    manager.add_plant("tomato", 5, 8)
    manager.add_plant("lettuce", 15, 8)
    manager.add_plant("", 5, 6)

    print("\nWatering plants...")
    manager.water_plants(["tomato", "lettuce"])

    print("\nChecking plant health...")
    manager.plant_health_check(["tomato"], 5, 8)
    manager.plant_health_check(["lettuce"], 15, 8)

    print("\nTesting error recovery...")
    try:
        manager.water_error()
    except WaterError as e:
        print(f"Caught GardenError: {e}")
    finally:
        print("System recovered and continuing...\n")
    print("Garden management system test complete!")


if __name__ == "__main__":
    test_garden_management()

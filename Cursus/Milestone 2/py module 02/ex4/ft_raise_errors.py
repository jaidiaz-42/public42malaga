def check_plant_health(plant_name: str, water_level: int,
                       sunlight_hours: int) -> str:
    if plant_name == "":
        raise ValueError("Plant name cannot be empty")
    if water_level < 1:
        raise ValueError(f"Water level {water_level} "
                         "is too low (min 1)")
    if water_level > 10:
        raise ValueError(f"Water level {water_level} "
                         "is too high (max 10)")
    if sunlight_hours < 2:
        raise ValueError(f"Sunlight hours {sunlight_hours} "
                         "is too low (min 2)")
    if sunlight_hours > 12:
        raise ValueError(f"Sunlight hours {sunlight_hours} "
                         "is too high (max 12)")
    return (f"Plant '{plant_name}' is healthy!\n")


def test_plant_checks() -> None:
    print("=== Garden Plant Health Checker ===\n")
    print("Testing good values...")
    try:
        print(check_plant_health("tomato", 5, 6))
    except ValueError as e:
        print(f"Error: {e}\n")
    print("Testing empty plant name...")
    try:
        print(check_plant_health("", 5, 6))
    except ValueError as e:
        print(f"Error: {e}\n")
    print("Testing bad water level...")
    try:
        print(check_plant_health("lettuce", 15, 3))
    except ValueError as e:
        print(f"Error: {e}\n")
    print("Testing bad sunlight hours...")
    try:
        print(check_plant_health("oak", 5, 0))
    except ValueError as e:
        print(f"Error: {e}\n")
    print("All error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()

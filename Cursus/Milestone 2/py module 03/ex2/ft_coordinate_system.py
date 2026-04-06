import math
from typing import Tuple


def get_player_pos() -> Tuple[float, float, float]:
    while True:
        try:
            line: str = input(
                "Enter new coordinates as "
                "floats in format 'x,y,z': ")
            parts: list[str] = line.split(",")
            if len(parts) != 3:
                print("Invalid syntax")
                continue
            x: float = float(parts[0].strip())
            y: float = float(parts[1].strip())
            z: float = float(parts[2].strip())
            return (x, y, z)
        except ValueError as e:
            param: str = line.split(",")[0] if "," in line else line
            print(f"Error on parameter '{param}': {e}")


def main() -> None:
    print("=== Game Coordinate System ===\n")

    print("Get a first set of coordinates")
    pos1: Tuple[float, float, float] = get_player_pos()
    x1, y1, z1 = pos1

    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={x1}, Y={y1}, Z={z1}")

    dist_center: float = math.sqrt(x1**2 + y1**2 + z1**2)
    print(f"Distance to center: {round(dist_center, 4)}")

    print("\nGet a second set of coordinates")
    pos2: Tuple[float, float, float] = get_player_pos()
    x2, y2, z2 = pos2

    dist_pts: float = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    print(f"Distance between the 2 sets of coordinates: {round(dist_pts, 4)}")


if __name__ == "__main__":
    main()

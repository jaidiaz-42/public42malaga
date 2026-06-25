from collections import deque
from typing import List, Tuple  # , Dict, Optional
from src.matrix import MazeMatrix, N, E, S, W, MOVE


class MazeSolver:
    def __init__(self, matrix: MazeMatrix) -> None:
        self.matrix: MazeMatrix = matrix

    def solve(self, entry: Tuple[int, int],
              exit_coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        # queue: saves pairs of (current_position, path_to_reach_it)
        queue: deque[Tuple[Tuple[int, int], List[Tuple[int, int]]]] = deque()
        queue.append((entry, [entry]))
        visited = {entry}

        while queue:
            (cx, cy), path = queue.popleft()

            # return the path if we reached the exit
            if (cx, cy) == exit_coord:
                return path

            current_value = self.matrix.grid[cy][cx]

            # evaluate possible moves based on the current cell's walls
            for direction, (dx, dy) in MOVE.items():
                if (current_value & direction) == 0:
                    nx, ny = cx + dx, cy + dy

                    if (self.matrix.is_in_bounds(nx, ny) and
                       (nx, ny) not in visited):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))

        return []  # return empty path if no solution is found

    def path_to_directions(self, path: List[Tuple[int, int]]) -> str:
        if not path or len(path) < 2:
            return ""

        directions = []
        dir_to_char = {N: "N", S: "S", E: "E", W: "W"}

        for i in range(len(path) - 1):
            cx, cy = path[i]
            nx, ny = path[i + 1]
            dx, dy = nx - cx, ny - cy

            # Find the direction corresponding to the movement (dx, dy)
            for direction, (move_dx, move_dy) in MOVE.items():
                if move_dx == dx and move_dy == dy:
                    directions.append(dir_to_char[direction])
                    break

        return "".join(directions)

    def save_to_file(self,
                     filepath: str,
                     entry: Tuple[int, int],
                     exit_coord: Tuple[int, int],
                     path: List[Tuple[int, int]]) -> None:
        dir_string = self.path_to_directions(path)

        with open(filepath, 'w') as f:
            # 1. write the maze grid in hexadecimal format
            for y in range(self.matrix.height):
                row_hex = []
                for x in range(self.matrix.width):
                    val = self.matrix.grid[y][x]
                    row_hex.append(f"{val:X}")
                f.write(" ".join(row_hex) + "\n")
            f.write("\n")

            # 2. write the entry and exit coordinates
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_coord[0]},{exit_coord[1]}\n")

            # 3. write the solution path as a string of directions
            f.write(f"{dir_string}\n")

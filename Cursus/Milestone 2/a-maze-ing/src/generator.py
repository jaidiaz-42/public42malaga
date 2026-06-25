import random
from typing import List, Tuple
from src.matrix import MazeMatrix, MOVE, OPPOSITE  # , N, E, S, W


class MazeGenerator:
    def __init__(self, matrix: MazeMatrix) -> None:
        self.matrix: MazeMatrix = matrix
        self.visited: List[List[bool]] = [
            [False for _ in range(matrix.width)] for _ in range(matrix.height)
        ]

    def generate(self, start_x: int = 0, start_y: int = 0) -> None:
        stack: List[Tuple[int, int]] = []

        if (start_x, start_y) in self.matrix.cells_42:
            start_x, start_y = self._find_free_start_cell()

        stack.append((start_x, start_y))
        self.visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            neighbors = self._get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                direction, next_x, next_y = random.choice(neighbors)

                # break the wall between current cell and chosen neighbor
                self.matrix.grid[current_y][current_x] &= ~direction
                self.matrix.grid[next_y][next_x] &= ~OPPOSITE[direction]

                # mark the neighbor as visited and add it to the stack
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                # backtrack if there are no unvisited neighbors
                stack.pop()

    def _get_unvisited_neighbors(self, x: int, y: int) -> List[
         Tuple[int, int, int]]:
        valid_neighbors: List[Tuple[int, int, int]] = []

        for direction, (dx, dy) in MOVE.items():
            nx, ny = x + dx, y + dy

            # The neighbor is valid if:
            # 1. It is within the bounds of the map.
            # 2. It has not been visited yet by the algorithm.
            # 3. It is not a cell reserved for the "42" pattern.
            if self.matrix.is_in_bounds(nx, ny):
                cells42 = self.matrix.cells_42
                if (not self.visited[ny][nx] and (nx, ny) not in cells42):
                    valid_neighbors.append((direction, nx, ny))
        return valid_neighbors

    def _find_free_start_cell(self) -> Tuple[int, int]:
        # search 1 cell not in 42 cells
        for y in range(self.matrix.height):
            for x in range(self.matrix.width):
                if (x, y) not in self.matrix.cells_42:
                    return x, y
        return (0, 0)

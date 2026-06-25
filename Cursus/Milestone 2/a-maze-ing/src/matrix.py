from typing import List, Tuple, Set

N, E, S, W = 1, 2, 4, 8

OPPOSITE: dict[int, int] = {N: S, S: N, E: W, W: E}

MOVE: dict[int, Tuple[int, int]] = {
    N: (0, -1),
    S: (0, 1),
    E: (1, 0),
    W: (-1, 0)
}


class MazeMatrix:

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

        # N + E + S + W = 1 + 2 + 4 + 8 = 15 (hexadecimal: 'F')
        self.grid: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)]

        # create mask for 42 cells
        self.cells_42: Set[Tuple[int, int]] = set()

        # try to apply the 42 pattern if the maze is large enough
        self._apply_42_mask()

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _apply_42_mask(self) -> None:
        mask_42 = [
            [1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 1, 0, 0]
        ]

        mask_h = len(mask_42)
        mask_w = len(mask_42[0])

        if self.width < mask_w + 4 or self.height < mask_h + 4:
            print("[INFO] El tamaño del laberinto es demasiado pequeño"
                  " para albergar el patrón '42'.")
            return

        # calculate the top-left corner to center the mask
        start_x = (self.width - mask_w) // 2
        start_y = (self.height - mask_h) // 2

        # apply the mask to the maze grid
        for y in range(mask_h):
            for x in range(mask_w):
                if mask_42[y][x] == 1:
                    target_x = start_x + x
                    target_y = start_y + y
                    # ubication cells
                    self.cells_42.add((target_x, target_y))
                    # mark all walls as closed (15) for these cells
                    self.grid[target_y][target_x] = 15

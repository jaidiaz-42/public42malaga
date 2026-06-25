import os
import sys
from typing import List, Tuple, Dict
from src.matrix import MazeMatrix, N, E, S, W


class MazeDisplay:

    def __init__(self, matrix: MazeMatrix,
                 entry: Tuple[int, int],
                 exit_coord: Tuple[int, int],
                 path: List[Tuple[int, int]]) -> None:
        self.matrix: MazeMatrix = matrix
        self.entry: Tuple[int, int] = entry
        self.exit_coord: Tuple[int, int] = exit_coord
        self.path: List[Tuple[int, int]] = path

        # interactive path state
        self.show_path: bool = True
        self.color_index: int = 0

        # 0: Clasic (Green), 1: Blue Cyan, 2: Magenta, 3: hite/Grey
        self.palettes: List[Dict[str, str]] = [
            {"wall": "\033[1;32m", "path": "\033[1;33m",
             "entry": "\033[1;31m",
             "exit": "\033[1;36m",
             "42": "\033[1;35m"},  # Green/Yellow
            {"wall": "\033[1;36m",
             "path": "\033[1;32m",
             "entry": "\033[1;31m",
             "exit": "\033[1;33m",
             "42": "\033[1;34m"},  # Cyan/Green
            {"wall": "\033[1;35m",
             "path": "\033[1;36m",
             "entry": "\033[1;32m",
             "exit": "\033[1;31m",
             "42": "\033[1;33m"},  # Magenta/Cyan
            {"wall": "\033[1;37m",
             "path": "\033[1;34m",
             "entry": "\033[1;32m",
             "exit": "\033[1;35m",
             "42": "\033[1;31m"}  # White/Blue
        ]
        self.reset_code: str = "\033[0m"

    def clear_screen(self) -> None:
        if os.name == 'nt':
            print("\033[2J\033[H", end="")
        else:
            sys.stdout.write("\033[H")
            sys.stdout.flush()

    def render(self) -> None:
        # Clear the console before rendering
        self.clear_screen()

        c = self.palettes[self.color_index]
        path_set = set(self.path)

        print("=== 42 A-MAZE-ING VISUALIZER ===")
        print(f"Dimensiones: {self.matrix.width}x{self.matrix.height}\n")

        # analysis of the maze grid to render it with walls and paths
        for y in range(self.matrix.height):
            top_line = ""
            for x in range(self.matrix.width):
                val = self.matrix.grid[y][x]
                top_line += c["wall"] + "+---" if (
                    val & N) else c["wall"] + "+   "
            print(top_line + "+")

            mid_line = ""  # left wall + content + right wall for each cell
            for x in range(self.matrix.width):
                val = self.matrix.grid[y][x]

                # west wall
                mid_line += c["wall"] + "|" if (val & W) else " "

                # cell content: entry, exit, path, 42 cell or empty
                if (x, y) == self.entry:
                    mid_line += c["entry"] + " S "
                elif (x, y) == self.exit_coord:
                    mid_line += c["exit"] + " E "
                elif self.show_path and (x, y) in path_set:
                    mid_line += c["path"] + " • "
                elif (x, y) in self.matrix.cells_42:
                    mid_line += c["42"] + "███"
                else:
                    mid_line += "   "

            # West wall checker for the last cell in the row
            last_val = self.matrix.grid[y][-1]
            mid_line += c["wall"] + "|" if (last_val & E) else " "
            print(mid_line)

        # Last line of walls for the bottom of the maze
        bottom_line = ""
        for x in range(self.matrix.width):
            val = self.matrix.grid[-1][x]
            bottom_line += c["wall"] + "+---" if (
                val & S) else c["wall"] + "+   "
        print(bottom_line + "+" + self.reset_code)

        # MENU
        print("\n[CONTROLES INTERACTIVOS]")
        print(" [H] Mostrar/Ocultar solución (Toggle Path)")
        print(" [C] Cambiar paleta de colores (Wall Colors)")
        print(" [R] Regenerar laberinto con nueva semilla")
        print(" [Q] Salir del programa")

    def change_color(self) -> None:
        self.color_index = (self.color_index + 1) % len(self.palettes)

    def toggle_path(self) -> None:
        self.show_path = not self.show_path

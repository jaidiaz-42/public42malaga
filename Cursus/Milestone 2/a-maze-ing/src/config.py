import os
from typing import Dict, Tuple, Any


class ConfigParser:

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.data: Dict[str, str] = {}

    def parse(self) -> Dict[str, Any]:

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Error: El archivo"
                                    f"'{self.filepath}' no existe.")

        with open(self.filepath, 'r') as file:
            for line_number, line in enumerate(file, 1):
                clean_line = line.strip()

                if not clean_line or clean_line.startswith('#'):
                    continue

                if '=' not in clean_line:
                    raise SyntaxError("Error de sintaxis en línea"
                                      f" {line_number}:"
                                      " Falta el operador '='.")

                key, value = clean_line.split('=', 1)
                self.data[key.strip()] = value.strip()

        return self._validate()

    def _validate(self) -> Dict[str, Any]:
        required_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
            ]
        for key in required_keys:
            if key not in self.data:
                raise ValueError("Error de configuración:"
                                 f"Falta la clave obligatoria '{key}'.")

        validated: Dict[str, Any] = {}

        try:
            validated["WIDTH"] = int(self.data["WIDTH"])
            validated["HEIGHT"] = int(self.data["HEIGHT"])
            if validated["WIDTH"] <= 0 or validated["HEIGHT"] <= 0:
                print(
                    "WIDTH y HEIGHT deben ser enteros mayores que cero.")
                print("Se aplicará la configuración estándar:"
                      "WIDTH=20,"
                      "HEIGHT=15")
                validated["WIDTH"] = 20
                validated["HEIGHT"] = 15

            validated["ENTRY"] = self._parse_coordinates(
                self.data["ENTRY"],
                validated["WIDTH"],
                validated["HEIGHT"],
                default_coord=(0, 0),
                coord_type="ENTRY"
            )
            validated["EXIT"] = self._parse_coordinates(
                self.data["EXIT"],
                validated["WIDTH"],
                validated["HEIGHT"],
                default_coord=(validated["WIDTH"] - 1,
                               validated["HEIGHT"] - 1),
                coord_type="EXIT"
            )

            if validated["ENTRY"] == validated["EXIT"]:
                raise ValueError("Las coordenadas de ENTRY y EXIT"
                                 " no pueden ser iguales.")

            validated["OUTPUT_FILE"] = self.data["OUTPUT_FILE"]
            validated["PERFECT"] = self.data["PERFECT"].lower() in ("true",
                                                                    "1",
                                                                    "yes")

        except ValueError as e:
            raise ValueError(f"Error en la validación de datos: {e}")

        return validated

    def _parse_coordinates(self,
                           coord_str: str,
                           width: int,
                           height: int,
                           default_coord: Tuple[int, int],
                           coord_type: str) -> Tuple[int, int]:
        try:
            parts = coord_str.split(',')
            if len(parts) != 2:
                raise ValueError()
            x, y = int(parts[0]), int(parts[1])
        except ValueError:
            print(f"[WARN] Formato inválido para {coord_type} '{coord_str}'"
                  f". Se usará la configuración estándar: {default_coord}")
            return default_coord

        if not (0 <= x < width) or not (0 <= y < height):
            print(f"[WARN] Coordenadas de {coord_type} ({x},{y})"
                  f"fuera de los límites ({width}x{height}). \n"
                  f"Aplicando configuración estándar: {default_coord}")
            return default_coord

        return (x, y)

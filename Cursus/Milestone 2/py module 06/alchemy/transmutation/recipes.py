import alchemy  # Abs
from elements import create_fire  # Rel


def lead_to_gold() -> str:
    return f"Recipe transmuting Lead to Gold: brew " \
     f"'{alchemy.elements.create_air()}' " \
     f"and '{alchemy.potions.strength_potion()}' mixed with '{create_fire()}'"

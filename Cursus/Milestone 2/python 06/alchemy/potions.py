from elements import create_fire, create_water
import alchemy.elements as inner_elements


def healing_potion() -> str:
    return f"Healing Potion brewed with '{inner_elements.create_earth()}'" \
           f"and '{inner_elements.create_air()}'"


def strength_potion() -> str:
    return (f"Strength potion brewed with "
            f"'{create_fire()}' and '{create_water()}'")

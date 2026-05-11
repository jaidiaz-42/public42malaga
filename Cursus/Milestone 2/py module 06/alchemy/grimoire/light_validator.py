from .light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    ingredients_parsed: str = ingredients.replace("and", ",")
    ingredients_list = ingredients_parsed.split(",")
    ingredients_list = [value.strip().lower() for value in
                        ingredients_list]

    if set(ingredients_list).intersection(light_spell_allowed_ingredients()):
        return "VALID"
    return "INVALID"

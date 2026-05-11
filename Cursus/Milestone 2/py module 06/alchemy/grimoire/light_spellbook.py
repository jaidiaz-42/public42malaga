def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    # o aqui o en el validator importando en la funcion validate
    from .light_validator import validate_ingredients
    validation_status: str = validate_ingredients(ingredients)
    status: str = "rejected"
    if (validation_status == "VALID"):
        status = "recorded"

    return (
            f"Spell {status}: {spell_name} "
            f"({ingredients} - {validation_status})"
        )

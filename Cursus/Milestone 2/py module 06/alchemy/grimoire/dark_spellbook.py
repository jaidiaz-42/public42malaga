from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    validation_status: str = validate_ingredients(ingredients)
    status: str = "rejected"
    if (validation_status == "VALID"):
        status = "recorded"

    return (
            f"Spell {status}: {spell_name} "
            f"({ingredients} - {validation_status})"
        )

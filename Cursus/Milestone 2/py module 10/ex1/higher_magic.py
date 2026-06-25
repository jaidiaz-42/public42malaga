from collections.abc import Callable
from typing import Any


def spell_combiner(spell1: Callable[
     [str, int], str], spell2: Callable[
        [str, int], str]) -> Callable[[str, int], tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable[
     [str, int], str], multiplier: int) -> Callable[[str, int], str]:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable[
     [str, int], Any], spell: Callable[
        [str, int], str]) -> Callable[[str, int], str]:
    def cast_if(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return cast_if


def spell_sequence(spells: list[
     Callable[[str, int], str]]) -> Callable[[str, int], list[str]]:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def main() -> None:
    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target}"

    def heal(target: str, power: int) -> str:
        return f"Heals {target}"

    def power_check(target: str, power: int) -> str:
        return str(power)

    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    res = combined("Dragon", 10)
    print(f"Combined spell result: {res[0]}, {res[1]}")

    print("\nTesting power amplifier...")
    amplified = power_amplifier(power_check, 3)
    print(f"Original: 10, Amplified: {amplified('Dummy', 10)}")


if __name__ == "__main__":
    main()

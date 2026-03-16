class SecurePlant:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.__height: int = 0
        self.__age: int = 0

    def set_height(self, height: int) -> None:
        if height < 0:
            print("Security: Negative height rejected")
        else:
            self.__height = height
            print(f"Height updated: {height}cm [OK]")

    def set_age(self, age: int) -> None:
        if age < 0:
            print("Security: Negative age rejected")
        else:
            self.__age = age
            print(f"Age updated: {age} days [OK]")

    def get_info(self) -> str:
        return (f"Current plant: {self.name}"
                f"({self.__height}cm, {self.__age} days)")


def main() -> None:
    print("=== Garden Security System ===")
    rose: SecurePlant = SecurePlant("Rose")
    print(f"Plant created: {rose.name}")

    rose.set_height(25)
    rose.set_age(30)

    print("Invalid operation attempted: height -5cm [REJECTED]")
    rose.set_height(-5)

    print(rose.get_info())


if __name__ == "__main__":
    main()

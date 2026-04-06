import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ft_inventory_system.py <item:qty> ...")
        return

    inventory = {}

    try:
        for arg in sys.argv[1:]:
            item, qty_str = arg.split(":")
            qty = int(qty_str)
            # Acumular si el item ya existe
            inventory[item] = inventory.get(item, 0) + qty

        total_items = sum(inventory.values())
        unique_types = len(inventory)

        print(f"Total items in inventory: {total_items}")
        print(f"Unique item types: {unique_types}")

        print("\n=== Current Inventory ===")
        for item, qty in inventory.items():
            percent = (qty / total_items) * 100
            unit_str = "units" if qty != 1 else "unit"
            print(f"{item}: {qty} {unit_str} ({percent:.1f}%)")

        most_abundant = max(inventory, key=inventory.get)
        least_abundant = min(inventory, key=inventory.get)

        print("\n=== Inventory Statistics ===")
        print(f"Most abundant: {most_abundant} "
              f"({inventory[most_abundant]} units)")

        last_qty = inventory[least_abundant]
        unit_last = "units" if last_qty != 1 else "unit"
        print(f"Least abundant: {least_abundant} ({last_qty} {unit_last})")

        abundant = {k: v for k, v in inventory.items() if v >= 7}
        moderate = {k: v for k, v in inventory.items() if 4 <= v <= 6}
        scarce = {k: v for k, v in inventory.items() if v < 4}

        print("\n=== Item Categories ===")
        print(f"Abundant = {abundant}")
        print(f"Moderate = {moderate}")
        print(f"Scarce = {scarce}")

    except (ValueError, IndexError):
        print("Format error. Use item:qty (e.g., apple:5)")


if __name__ == "__main__":
    main()

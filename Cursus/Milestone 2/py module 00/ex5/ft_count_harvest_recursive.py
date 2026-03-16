def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count_days(current, total):
        if current > total:
            return
        print(f"Day {current}")
        count_days(current + 1, total)

    count_days(1, days)
    print("Harvest time!")
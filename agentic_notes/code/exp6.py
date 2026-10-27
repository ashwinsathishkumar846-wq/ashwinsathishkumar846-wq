laptops = [
    {"name": "Laptop A", "price": 38000, "speed": 5, "battery": 6},
    {"name": "Laptop B", "price": 55000, "speed": 8, "battery": 9},
    {"name": "Laptop C", "price": 72000, "speed": 9, "battery": 7},
    {"name": "Laptop D", "price": 45000, "speed": 7, "battery": 5}
]


def system1(budget):
    affordable = [x for x in laptops if x["price"] <= budget]
    return min(affordable, key=lambda x: x["price"])


def score(x, budget):
    return (0.3 * ((budget - x["price"]) / budget * 10)
            + 0.4 * x["speed"] + 0.3 * x["battery"])


def system2(budget):
    affordable = [x for x in laptops if x["price"] <= budget]
    return max(affordable, key=lambda x:
        0.3 * ((budget - x["price"]) / budget * 10)
        + 0.4 * x["speed"] + 0.3 * x["battery"])


print("=== System 1 vs System 2 ===")

for budget in (40000, 60000, 80000):
    fast = system1(budget)
    deep = system2(budget)
    print("\nBudget: Rs.", budget)
    print("System 1:", fast["name"])
    print("System 2:", deep["name"], "Score:", round(score(deep, budget), 2))
    print("Same decision:", fast["name"] == deep["name"])

from ex00 import add_ingot


def add_ingots(purse: dict, amount: int) -> dict:
    copy_purse = purse.copy()

    for i in range(amount):
        copy_purse = add_ingot(copy_purse)

    return copy_purse


def split_booty(purse0: dict, purse1: dict, purse2: dict) -> tuple[dict, dict, dict]:
    all_gold_ingots: int = 0

    for purse in purse0, purse1, purse2:
        all_gold_ingots += purse["gold_ingots"] * (purse["gold_ingots"] >= 0)

    p0: dict = {}
    p1: dict = {}
    p2: dict = {}

    p0 = add_ingots(p0, all_gold_ingots // 3 + (all_gold_ingots % 3 == 2))
    p1 = add_ingots(p1, all_gold_ingots // 3 + (all_gold_ingots % 3 - 1 == 1))
    p2 = add_ingots(p2, all_gold_ingots // 3 + (all_gold_ingots % 3 == 1))
    print(all_gold_ingots)
    return (p0, p1, p2)


if __name__ == "__main__":
    p0: dict = {"gold_ingots": -3, "apples": 2}
    p1: dict = {"gold_ingots": 1, "apples": 2}
    p2: dict = {"gold_ingots": 1, "apples": 2}
    test_p: dict = {}
    test_p = add_ingots(test_p, 4)
    print(test_p)
    print(split_booty(p0, p1, p2))

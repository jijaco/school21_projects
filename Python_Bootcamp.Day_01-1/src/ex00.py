def add_ingot(purse: dict) -> dict:
    copy_purse = purse.copy()

    if (copy_purse.get("gold_ingots") != None):
        if (copy_purse.get("gold_ingots") >= 1):
            copy_purse["gold_ingots"] += 1
        else:
            copy_purse["gold_ingots"] = 1
    else:
        copy_purse["gold_ingots"] = 1

    return copy_purse


def get_ingot(purse: dict) -> dict:
    copy_purse = purse.copy()

    if copy_purse.get("gold_ingots") == None:
        print("No gold ingots")
    elif (copy_purse.get("gold_ingots") > 1):
        copy_purse["gold_ingots"] -= 1
    else:
        copy_purse.pop("gold_ingots")

    return copy_purse


def empty(purse: dict) -> dict:
    copy_purse = purse.copy()

    copy_purse.clear()

    return copy_purse


if __name__ == "__main__":
    purse: dict = {}
    copy_purse: dict = {}
    copy_purse = add_ingot(purse)

    print(purse.get("gold_ingots") == None)

    print(copy_purse.get("gold_ingots") == 1)

    copy_purse = get_ingot(copy_purse)
    print(copy_purse.get("gold_ingots") == None)

    copy_purse = get_ingot(copy_purse)
    print(copy_purse.get("gold_ingots") == None)

    purse = {"gold_ingots": -1}
    purse = get_ingot(purse)
    print(purse.get("gold_ingots") == None)

    purse = {"gold_ingots": -1}
    purse = get_ingot(purse)
    print(purse.get("gold_ingots") == None)

    purse = {"gold_ingots": -1}
    purse = add_ingot(purse)
    print(purse.get("gold_ingots") == 1)

    purse = add_ingot(purse)
    print(purse.get("gold_ingots") == 2)

    purse["apples"] = 1
    print(purse["apples"] == 1)

    copy_purse = empty(purse)
    print(purse != copy_purse)
    print(copy_purse == {})
    print(purse.get("gold_ingots") == 2)
    print(purse.get("apples") == 1)

from typing import Callable
from ex00 import *


def set_alarm(function: Callable) -> None:
    def wrapper(purse: dict) -> dict:
        purse = function(purse)
        print("SQUEAK")
        return purse
    return wrapper


add_ingot = set_alarm(add_ingot)
get_ingot = set_alarm(get_ingot)
empty = set_alarm(empty)

if __name__ == "__main__":
    test_purse: dict = {}
    test_purse = add_ingot(test_purse)
    test_purse = add_ingot(test_purse)
    test_purse = add_ingot(test_purse)
    print(test_purse.get("gold_ingots") == 3)
    test_purse = get_ingot(test_purse)
    print(test_purse.get("gold_ingots") == 2)
    test_purse = empty(test_purse)
    print(test_purse == {})

class Key:
    def __init__(self, passphrase: str = "zax2rulez") -> None:
        self.passphrase: str = passphrase

    def __str__(self) -> str:
        return "GeneralTsoKeycard"

    def __len__(self) -> int:
        return 1337

    def __getitem__(self, num: int) -> int:
        pow_ten = 1
        number_of_digits = 0
        while abs(num / pow_ten) > 1:
            pow_ten *= 10
            number_of_digits += 1
        return number_of_digits

    def __gt__(self, num: int) -> bool:
        return num <= 9000


if __name__ == "__main__":
    key = Key()
    print(len(key) == 1337)
    print(key[404] == 3)
    print(key > 9000)
    print(key.passphrase == "zax2rulez")
    print(str(key) == "GeneralTsoKeycard")

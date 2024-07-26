from collections import Counter


class Player:

    def __init__(self, behavior: int = 0):
        self._behavior = behavior
        self._prev_behavior = behavior
        self._name: str

    def __gt__(self, other) -> bool:
        return self._behavior > other._behavior

    def __eq__(self, other) -> bool:
        return self._behavior == other._behavior

    def __eq__(self, other: int) -> bool:
        return self._behavior == other

    # def __neq__(self, other) -> int:
    #     return not (self == other)

    def track_current_behavior(self):
        self._prev_behavior = self._behavior

    def my_name(self) -> str:
        return self._name

    def return_to_default(self) -> None:
        pass


class Cheater(Player):

    def __init__(self, behavior: int = 0):
        super().__init__(1)
        self._name = "Cheater"

    def adapt(self, other: Player) -> None:
        pass

    def return_to_default(self) -> None:
        self._behavior = 1
        self._prev_behavior = 1


class Cooperator(Player):

    def __init__(self, behavior: int = 0):
        super().__init__(0)
        self._name = "Cooperator"

    def adapt(self, other: Player) -> None:
        pass

    def return_to_default(self) -> None:
        self._behavior = 0
        self._prev_behavior = 0


class Copycat(Player):

    def __init__(self, behavior: int = 0):
        super().__init__(0)
        self._name = "Copycat"

    def adapt(self, other: Player) -> None:
        # super().adapt()
        self._behavior = other._prev_behavior

    def return_to_default(self) -> None:
        self._behavior = 0
        self._prev_behavior = 0


class Grudger(Player):
    def __init__(self, behavior: int = 0):
        super().__init__(0)
        self._name = "Grudger"

    def adapt(self, other: Player) -> None:
        # super().adapt()
        self._behavior = self._behavior or other._prev_behavior

    def return_to_default(self) -> None:
        self._behavior = 0
        self._prev_behavior = 0


class Detective(Player):
    def __init__(self, behavior: int = 0):
        super().__init__(0)
        self._name = "Detective"
        self.__games_played: int = 0
        self.__oponent_cheated: bool = False

    def adapt(self, other: Player) -> None:
        if other._behavior:
            self.__oponent_cheated = True

        if self.__games_played < 4:
            if self.__games_played == 0:
                self._behavior = 1
                self.__games_played = 1
            elif self.__games_played == 1:
                self._behavior = 0
                self.__games_played = 2
            elif self.__games_played == 2:
                self._behavior = 0
                self.__games_played = 3
            elif self.__games_played == 3:
                self._behavior = 1
                self.__games_played = 4

        if self.__oponent_cheated and self.__games_played >= 4:
            self._behavior = other._prev_behavior

    def return_to_default(self) -> None:
        self._behavior = 0
        self._prev_behavior = 0


class Game(object):

    def __init__(self, matches: int = 10) -> None:
        self.matches: int = matches
        self.registry: Counter = Counter()

    def __round(self, player1: Player, player2: Player) -> None:
        # player1
        if player1 > player2:
            self.registry[player1.my_name()] += 3
            self.registry[player2.my_name()] -= 1
        elif player1 == player2 == 0:
            self.registry[player1.my_name()] += 2
            self.registry[player2.my_name()] += 2
        elif player1 < player2:
            self.registry[player1.my_name()] -= 1
            self.registry[player2.my_name()] += 3

    def play(self, player1: Player, player2: Player) -> None:
        if self.registry.get(player1.my_name()) == None:
            self.registry[player1.my_name()] = 0
        if self.registry.get(player2.my_name()) == None:
            self.registry[player2.my_name()] = 0

        for i in range(self.matches):
            self.__round(player1, player2)
            player1.adapt(player2)
            player2.adapt(player1)
            player1.track_current_behavior()
            player2.track_current_behavior()

        player1.return_to_default()
        player2.return_to_default()

    def top3(self) -> None:
        for i in self.registry.most_common(3):
            print(*i)


if __name__ == "__main__":
    game: Game = Game()

    game.play(Cheater(), Cooperator())
    game.play(Cheater(), Copycat())
    game.play(Cheater(), Grudger())
    game.play(Cheater(), Detective())
    game.play(Cooperator(), Copycat())
    game.play(Cooperator(), Grudger())
    game.play(Cooperator(), Detective())
    game.play(Copycat(), Grudger())
    game.play(Copycat(), Detective())
    game.play(Grudger(), Detective())

    game.top3()

import json
import random
from collections import defaultdict


class Protagonist:
    def __init__(self, name: str, id: str, start_location):
        self.id = id  # Уникальный идентификатор игрока
        self.name: str = name  # Имя игрока
        self.hp: int = 10  # Очки здоровья
        self.strength: int = 1  # Уровень силы
        self.craft: int = 1  # Уровень мастерства
        self.inventory = defaultdict(int)  # Инвентарь игрока
        self.inventory["pocket dust"] += 1  # Начальный предмет в инвентаре
        self.level: int = 1  # Уровень игрока
        self.active_quests = []  # Активные квесты
        self.completed_quests = []  # Выполненные квесты
        self.killed_enemies = []  # Список убитых врагов
        self.current_location = start_location  # Текущая локация игрока

    def talk_to(self, npc):
        """
        Взаимодействие с NPC.
        """
        print(f"{npc.name} говорит: {npc.phrases[0]}")

    def quest_to(self, npc):
        """
        Взаимодействие с NPC.
        """
        quest = npc.offer_quest()
        if quest:
            if quest.description not in self.completed_quests:
                if quest.description not in self.active_quests:
                    print(f"{npc.name} предлагает квест: {quest.description}")
                    self.active_quests.append(quest.description)
                if quest.objective['item'] in self.inventory:
                    print(f"Спасибо за {quest.objective['item']}! Держи награду за выполненный квест")
                    print(f"Вы получили: {quest.reward['item']}. Ваш уровень мастерства повышен на {quest.reward['craft_points']} очка")
                    # Увеличиваем навык мастерства гг
                    self.craft += quest.reward['craft_points']
                    # Удаляем предмет из инвентаря
                    self.inventory.pop(quest.objective['item'])
                    # Добавляем награду в инвентарь
                    new_inventory = quest.reward['item']
                    self.inventory[new_inventory] = 1
                    self.active_quests.remove(quest.description)
                    self.completed_quests.append(quest.description)
                    if "Advanced Cyber Implant" in self.inventory and "Hacker Toolkit" in self.inventory:
                        print('Поздравляем! Вы прошли игру!')
            else:
                print('Вы уже проходили этот квест')

    def attack(self, enemy):
        """
        Атака на врага.
        """
        protagonist_roll = random.randint(1, 6) + self.strength  # Бросок кубика для игрока
        enemy_roll = random.randint(1, 6) + enemy.strength  # Бросок кубика для врага
        if protagonist_roll > enemy_roll:
            print(f"Вы победили {enemy.name}!")
            self.advance_strength()
            self.killed_enemies.append(enemy.name)

            if enemy.name == "Corporate Security":
                print(f"Вы получили новый предмет! - Corporate Server Data")
                self.inventory['Corporate Server Data'] += 1
        else:
            print(f"{enemy.name} победил вас.")
            self.take_hit()
            if self.hp <= 0:
                print(f"Вы умерли. Игра начнется заново.")


    def take_hit(self, value=1):
        """
        Получение урона.
        """
        self.hp -= value
        # if self.hp <= 0:
        #     raise Exception("Вы умерли")

    def heal(self, value=1):
        """
        Лечение игрока.
        """
        self.hp += value

    def advance_strength(self, value: int = 1):
        """
        Повышение уровня силы.
        """
        self.strength += value
        if self.strength >= 10:
            self.level += 1
            self.strength = 1

    def advance_craft(self, value: int = 1):
        """
        Повышение уровня мастерства.
        """
        self.craft += value

    def go(self, direction):
        """
        Перемещает персонажа в указанном направлении.
        """
        if direction in self.current_location.directions:
            self.current_location = self.current_location.directions[direction]
            print(f"Вы переместились в {self.current_location.name}.")
            print(self.current_location.description)
        else:
            print("Вы не можете пойти в этом направлении.")

    def whereami(self):
        """
        Возвращает описание текущего местоположения.
        """
        print(f"Вы находитесь: {self.current_location.name}")
        print(self.current_location.description)

    def possible_directions(self):
        dirs = []
        for direction in self.current_location.directions.items():
            dirs.append(direction[0])
        return dirs

    def take(self, item: str):
        """
        Добавление предмета в инвентарь.
        """
        self.inventory[item] += 1

    def give(self, npc, item: str):
        """
        Передача предмета NPC.
        """
        if self.inventory[item] > 0:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            npc.receive(item)
        else:
            print(f"У вас нет {item}")

    def actual_inventory(self):
        for item in self.inventory.items():
            print(item)

    def if_exit(self, start_location):
        self.hp: int = 10  # Очки здоровья
        self.strength: int = 1  # Уровень силы
        self.craft: int = 1  # Уровень мастерства
        self.inventory = defaultdict(int)  # Инвентарь игрока
        self.inventory["pocket dust"] += 1  # Начальный предмет в инвентаре
        self.level: int = 1  # Уровень игрока
        self.active_quests = []  # Активные квесты
        self.completed_quests = []  # Выполненные квесты
        self.killed_enemies = []  # Список убитых врагов
        self.current_location = start_location  # Текущая локация игрока


class NPC:
    def __init__(self, name: str, phrases: list, dialogue, inventory, quests: list = None):
        self.name = name  # Имя NPC
        self.phrases = phrases  # Фразы NPC
        self.dialogue = Dialogue(**dialogue)
        self.inventory = inventory  # Инвентарь NPC
        self.quests = quests if quests else []  # Квесты, предлагаемые NPC

    def receive(self, item: str):
        """
        Получение предмета от игрока.
        """
        self.inventory[item] += 1

    def offer_quest(self):
        """
        Предложение квеста игроку.
        """
        if self.quests:
            return self.quests[0]
        return None


class Enemy:
    def __init__(self, name: str, strength: int, phrases: list):
        self.name = name  # Имя врага
        self.phrases = phrases  # Фразы врага
        self.strength = strength  # Уровень силы врага

    def attack(self, protagonist):
        """
        Атака на игрока.
        """
        protagonist.take_hit()


class Location:
    def __init__(self, name: str, description: str, directions: dict):
        self.name = name  # Название локации
        self.description = description  # Описание локации
        self.directions = directions  # Направления к другим локациям

    def add_direction(self, direction, location):
        self.directions[direction] = location


def load_location(name: str):
    with open('map_data.json', 'r') as f:
        data = json.load(f)
        for loc_data in data["locations"]:
            if loc_data["name"] == name:
                return Location(loc_data["name"], loc_data["description"], loc_data["directions"])
    return None


class Dialogue:
    def __init__(self, greeting, questions, answers):
        self.greeting = greeting
        self.questions = questions  # Словарь вопросов
        self.answers = answers  # Словарь ответов

    def get_answer(self, question):
        """
        Возвращает ответ на заданный вопрос, если он существует.
        """
        return self.answers.get(question, "У меня нет ответа на этот вопрос.")


class Quest:
    def __init__(self, description: str, objective: dict, reward: dict):
        self.description = description  # Описание квеста
        self.objective = objective  # Цель квеста (напр., {"item": "magic stone"})
        self.reward = reward  # Награда за выполнение квеста (напр., {"strength": 2})

    def check_completion(self, protagonist):
        """
        Проверка, выполнен ли квест.
        """
        for key, value in self.objective.items():
            if key == "item":
                if protagonist.inventory[value] > 0:
                    return True
            elif key == "kill":
                if value in protagonist.killed_enemies:
                    return True
        return False

    def give_reward(self, protagonist):
        """
        Награждение игрока за выполнение квеста.
        """
        for key, value in self.reward.items():
            if key == "strength":
                protagonist.advance_strength(value)
            elif key == "craft":
                protagonist.advance_craft(value)
            elif key == "item":
                protagonist.take(value)

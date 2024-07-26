from load_map import load_map
from load_data import load_protagonist, load_npcs, load_enemies

# Загрузка карты
locations, start_location = load_map()

# Инициализация главного героя
protagonist = load_protagonist(start_location)

# Инициализация NPC и врагов
npcs = load_npcs()
enemies = load_enemies()


# Функция для отображения диалога с NPC
def talk_to_npc(npc):
    print(f"Вы подошли к {npc.name}.")
    print(npc.dialogue.greeting)
    while True:
        print("\nЧто вы хотите спросить?")
        for i, question in enumerate(npc.dialogue.questions):
            print(f"{i + 1}. {npc.dialogue.questions[question]}")
        help_list = list(npc.dialogue.questions)
        print("0. Вернуться")
        choice = input("Введите номер вопроса: ")

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(npc.dialogue.questions):
            question = help_list[int(choice) - 1]
            print(npc.dialogue.get_answer(question))
            if question == 'quest':
                print('1. Принять квест')
                print('2. Отклонить квест')
                quest_choice = input("Введите номер ответа: ")
                if quest_choice == "2":
                    break
                else:
                    protagonist.quest_to(npc)
                    break
            elif question == 'addition':
                if npc.inventory:
                    print('1. Взять предмет')
                    print('2. НЕ брать предмет')
                    inventory_choice = input("Введите номер ответа: ")
                    if inventory_choice == '2':
                        break
                    else:
                        if npc.inventory["item"] not in protagonist.inventory:
                            protagonist.take(npc.inventory["item"])
                            print(f"Предмет {npc.inventory['item']} добавлен в инвентарь")
                        else:
                            print(f"У вас уже есть {npc.inventory['item']} в инвентаре")
        else:
            print("Неверный ввод. Попробуйте еще раз.")


# Интерактивный интерфейс
def main():
    print("Добро пожаловать в игру!")
    while True:
        print("\nВыберите действие:")
        print("0. Посмотреть профиль")
        print("1. Посмотреть текущее местоположение")
        print("2. Поговорить с NPC")
        print("3. Атаковать врага")
        print("4. Переместиться")
        print("5. Выйти из игры")
        choice = input("Введите номер действия: ")

        if choice == "0":
            print(f"Имя игрока: {protagonist.name}")
            print(f"Здоровье: {protagonist.hp}")
            print(f"Сила: {protagonist.strength}")
            print(f"Мастерство: {protagonist.craft}")
            print(f"Уровень: {protagonist.level}")
            print(f"Активные квесты: {protagonist.active_quests}")
            print(f"Выполненные квесты: {protagonist.completed_quests}")
            print(f"Инвентарь: ")
            protagonist.actual_inventory()
            print(f"Текущая локация: {protagonist.current_location.name}")
        elif choice == "1":
            protagonist.whereami()
        elif choice == "2":
            for i, npc in enumerate(npcs):
                print(f"{i + 1}. {npc.name}")
            npc_choice = int(input("Выберите NPC для разговора: ")) - 1
            if 0 <= npc_choice < len(npcs):
                talk_to_npc(npcs[npc_choice])
            else:
                print("Неверный выбор. Попробуйте еще раз.")
        elif choice == "3":
            for i, enemy in enumerate(enemies):
                print(f"{i + 1}. {enemy.name}")
            enemy_choice = int(input("Выберите врага для атаки: ")) - 1
            if 0 <= enemy_choice < len(enemies):
                protagonist.attack(enemies[enemy_choice])
            else:
                print("Неверный выбор. Попробуйте еще раз.")
        elif choice == "4":
            direction = input(f"Введите направление {protagonist.possible_directions()}: ")
            protagonist.go(direction)
        elif choice == "5":
            print("Выход из игры.")
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")


if __name__ == "__main__":
    main()

import json
from models import Protagonist, NPC, Enemy, Quest


# Функции для загрузки данных из JSON файла
def load_protagonist(start_location):
    with open('game_data.json', 'r') as f:
        data = json.load(f)
        prot_data = data["protagonist"]
        protagonist = Protagonist(prot_data["name"], prot_data["id"], start_location)
        protagonist.hp = prot_data["hp"]
        protagonist.strength = prot_data["strength"]
        protagonist.craft = prot_data["craft"]
        for item, count in prot_data["inventory"].items():
            protagonist.inventory[item] = count
        return protagonist


def load_npcs():
    with open('game_data.json', 'r') as f:
        data = json.load(f)
        npcs = []
        for npc_data in data["npcs"]:
            # Загрузка квестов
            quests = [Quest(q["description"], q["objective"], q["reward"]) for q in npc_data.get("quests", [])]

            # Загрузка диалога
            dialogue_data = npc_data.get("dialogue", {})
            dialogue = {
                "greeting": dialogue_data.get("greeting", ""),
                "questions": dialogue_data.get("questions", {}),
                "answers": dialogue_data.get("answers", {})
            }

            # Создание NPC
            npcs.append(NPC(
                name=npc_data["name"],
                phrases=npc_data.get("phrases", []),
                dialogue=dialogue,
                inventory=npc_data.get("inventory", {}),
                quests=quests
            ))
        return npcs


def load_enemies():
    with open('game_data.json', 'r') as f:
        data = json.load(f)
        enemies = []
        for enemy_data in data["enemies"]:
            enemies.append(Enemy(enemy_data["name"], enemy_data["strength"], enemy_data["phrases"]))
        return enemies

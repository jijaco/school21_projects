import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InputTextMessageContent, InlineQueryResultArticle, InputFile
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from load_map import load_map
from load_data import load_protagonist, load_npcs, load_enemies

API_TOKEN = 'your_token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Load game data
locations, start_location = load_map()
protagonist = load_protagonist(start_location)
npcs = load_npcs()
enemies = load_enemies()

# Keyboard buttons
main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_kb.add(KeyboardButton("Профиль"), KeyboardButton("Местоположение"))
main_menu_kb.add(KeyboardButton("Разговор с NPC"), KeyboardButton("Атака врага"))
main_menu_kb.add(KeyboardButton("Переместиться"), KeyboardButton("Выйти"))

# Вспомогательная функция для отправки сообщений
last_user_id = None

photo_dict = {
        'Neon Gate': 'img/neon_gate_1.jpg',
        'Cyber Street': 'img/cyber_street_2.jpg',
        'Tech Market': 'img/tech_market_3.jpg',
        'Hackers Den': 'img/hackers_den.jpg',
        'Corporate Tower': 'img/corporate_tower.jpg',
        'Back Alley': 'img/back_alley.jpg',
        'Underground Club': 'img/underground_club.jpg',
        'Sky Lounge': 'img/sky_lounge.jpg',
        'Roof Top Garden': 'img/roof_top_garden.jpg'
    }


async def send_message_to_user(text):
    if last_user_id:
        await bot.send_message(last_user_id, text)


# Класс для перенаправления stdout в телеграм-бот
class TelegramLogger:
    def __init__(self):
        self.original_stdout = sys.stdout

    def write(self, message):
        if message.strip():
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(send_message_to_user(message))
            else:
                loop.run_until_complete(send_message_to_user(message))

    def flush(self):
        pass


# Перенаправление stdout на TelegramLogger
sys.stdout = TelegramLogger()


# Start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    await message.reply("Добро пожаловать в игру!", reply_markup=main_menu_kb)


# Profile command handler
@dp.message_handler(lambda message: message.text == "Профиль")
async def show_profile(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    profile_text = (
        f"Имя игрока: {protagonist.name}\n"
        f"Здоровье: {protagonist.hp}\n"
        f"Сила💪🏻: {protagonist.strength}\n"
        f"Мастерство: {protagonist.craft}\n"
        f"Уровень: {protagonist.level}\n"
        f"Активные квесты: {', '.join(protagonist.active_quests)}\n"
        f"Выполненные квесты: {', '.join(protagonist.completed_quests)}\n"
        f"Инвентарь: {', '.join(protagonist.inventory.keys())}\n"
        f"Текущая локация: {protagonist.current_location.name}"
    )
    await message.reply(profile_text)


# Location command handler
@dp.message_handler(lambda message: message.text == "Местоположение")
async def show_location(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    await bot.send_photo(chat_id=message.chat.id, photo=InputFile(f"{photo_dict.get(protagonist.current_location.name)}"))
    location_text = (
        f"Вы находитесь: {protagonist.current_location.name}\n"
        f"{protagonist.current_location.description}"
    )
    await message.reply(location_text)


# Talk to NPC command handler
@dp.message_handler(lambda message: message.text == "Разговор с NPC")
async def talk_to_npc_handler(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    npc_kb = InlineKeyboardMarkup()
    for i, npc in enumerate(npcs):
        npc_kb.add(InlineKeyboardButton(npc.name, callback_data=f"npc_{i}"))
    await message.reply("Выберите NPC для разговора:", reply_markup=npc_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('npc_'))
async def process_npc_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('_')[1])
    npc = npcs[index]
    dialogue_text = f"Вы подошли к {npc.name}.\n{npc.dialogue.greeting}"
    dialogue_kb = InlineKeyboardMarkup()
    for i, question in enumerate(npc.dialogue.questions):
        dialogue_kb.add(InlineKeyboardButton(npc.dialogue.questions[question], callback_data=f"dialogue_{index}_{i}"))
    await bot.send_message(callback_query.from_user.id, dialogue_text, reply_markup=dialogue_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('dialogue_'))
async def process_dialogue_callback(callback_query: types.CallbackQuery):
    dialogue_kb = InlineKeyboardMarkup()
    data = callback_query.data.split('_')
    index = int(data[1])
    question_index = int(data[2])
    npc = npcs[index]
    question = list(npc.dialogue.questions.keys())[question_index]
    answer = npc.dialogue.get_answer(question)
    await bot.send_message(callback_query.from_user.id, answer)

    # Implementing quest acceptance/rejection
    if question == 'quest':
        quest = npc.offer_quest()
        if quest.objective['item'] not in protagonist.inventory:
            quest_kb = InlineKeyboardMarkup()
            quest_kb.add(InlineKeyboardButton("Принять квест", callback_data=f"accept_quest_{index}"))
            quest_kb.add(InlineKeyboardButton("Отклонить квест", callback_data=f"decline_quest_{index}"))
            await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=quest_kb)
        elif quest.objective['item'] in protagonist.inventory:
            quest_kb = InlineKeyboardMarkup()
            quest_kb.add(InlineKeyboardButton("Завершить квест", callback_data=f"finish_quest_{index}"))
            quest_kb.add(InlineKeyboardButton("Не завершать квест", callback_data=f"exit_quest_{index}"))
            await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=quest_kb)

    # Implementing item acceptance/rejection
    elif question == 'addition' and npc.inventory:
        inventory_kb = InlineKeyboardMarkup()
        inventory_kb.add(InlineKeyboardButton("Взять предмет", callback_data=f"take_item_{index}"))
        inventory_kb.add(InlineKeyboardButton("НЕ брать предмет", callback_data=f"decline_item_{index}"))
        await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=inventory_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('accept_quest_') or c.data.startswith('decline_quest_')
                                     or c.data.startswith('exit_quest_') or c.data.startswith('finish_quest_'))
async def process_quest_choice(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    index = int(data[2])
    npc = npcs[index]
    if data[0] == 'accept':
        protagonist.quest_to(npc)
        await bot.send_message(callback_query.from_user.id, f"Квест от {npc.name} принят!")
    elif data[0] == 'decline':
        await bot.send_message(callback_query.from_user.id, f"Квест от {npc.name} отклонен.")
    elif data[0] == 'exit':
        await bot.send_message(callback_query.from_user.id, f"Квест отложен")
    elif data[0] == 'finish':
        protagonist.quest_to(npc)
        await bot.send_message(callback_query.from_user.id, f"Квест от {npc.name} завершен!")


@dp.callback_query_handler(lambda c: c.data.startswith('take_item_') or c.data.startswith('decline_item_'))
async def process_item_choice(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    index = int(data[2])
    npc = npcs[index]
    if data[0] == 'take':
        item = npc.inventory["item"]
        if item not in protagonist.inventory:
            protagonist.take(item)
            await bot.send_message(callback_query.from_user.id, f"Предмет {item} добавлен в инвентарь")
        else:
            await bot.send_message(callback_query.from_user.id, f"У вас уже есть {item} в инвентаре")
    else:
        await bot.send_message(callback_query.from_user.id, "Вы отказались взять предмет.")


# Attack enemy command handler
@dp.message_handler(lambda message: message.text == "Атака врага")
async def attack_enemy_handler(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    enemy_kb = InlineKeyboardMarkup()
    for i, enemy in enumerate(enemies):
        enemy_kb.add(InlineKeyboardButton(enemy.name, callback_data=f"enemy_{i}"))
    await message.reply("Выберите врага для атаки:", reply_markup=enemy_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('enemy_'))
async def process_enemy_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('_')[1])
    enemy = enemies[index]
    protagonist.attack(enemy)
    if protagonist.hp <= 0:
        protagonist.if_exit(start_location)
    else:
        await bot.send_message(callback_query.from_user.id, f"Здоровье: {protagonist.hp}")


# Move command handler
@dp.message_handler(lambda message: message.text == "Переместиться")
async def move_handler(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    directions_kb = InlineKeyboardMarkup()
    for direction in protagonist.possible_directions():
        directions_kb.add(InlineKeyboardButton(direction, callback_data=f"move_{direction}"))
    await message.reply("Выберите направление:", reply_markup=directions_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('move_'))
async def process_move_callback(callback_query: types.CallbackQuery):
    direction = callback_query.data.split('_')[1]
    success = protagonist.go(direction)
    await bot.send_photo(chat_id=callback_query.message.chat.id,
                         photo=InputFile(f"{photo_dict.get(protagonist.current_location.name)}"))


# Exit command handler
@dp.message_handler(lambda message: message.text == "Выйти")
async def exit_game(message: types.Message):
    global last_user_id
    last_user_id = message.from_user.id
    protagonist.if_exit(start_location)
    await message.reply("Выход из игры. До новых встреч!")
    print("Выход из игры")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

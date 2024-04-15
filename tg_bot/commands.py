from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file
from datetime import datetime, timedelta
from utils.data import add_thousands_separator
from tg_bot.events import get_bebra_coins
from utils.parsing import Data
from tg_bot.key import shop_btn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

main_btn = [
        [types.KeyboardButton(text="📈 Ферма"), types.KeyboardButton(text="👤 Профиль")],
        [types.KeyboardButton(text="🔁 Обменник"), types.KeyboardButton(text="🛒 Магазин")],
        [types.KeyboardButton(text="🆘 Помощь")]
    ]

async def start_command(message: types.Message):
    data.check_user(message.from_user.id)
    

    text = """
👋 Добро пожаловать в бота <b>Bebra Miner</b>! 

🤖 Майни особые BebraCoin'ы и покупай новое оборудование для майнинга!


<i>⚠️ Все покупки, совершенные в боте являются виртуальными.
Бот не имеет ничего общего с обычными майнерами и майнингом. Бот является игровым, а не коммерческим.</i>

"""
    if message.chat.type == "private":
        await message.answer(text + "\n\n👇 Для продолжения нажми на одну из кнопок ", reply_markup=types.ReplyKeyboardMarkup(keyboard=main_btn.append(), resize_keyboard=True))
    else:
        await message.reply(text + "\n\n👇 Для продолжения нажми на одну из команд или введи ее вручную")





async def profile_command(message: types.Message):
    key = InlineKeyboardBuilder()

    key.button(text="⚙️ Настройки", callback_data="settings")
    key.button(text='🎟 Промокоды', callback_data='promocodes')




    data.check_user(message.from_user.id)
    Rbalance = read_file('data/users.json')[str(message.from_user.id)]['Rbalance']
    Bbalance = read_file('data/users.json')[str(message.from_user.id)]['Bbalance']
    miners = read_file('data/users.json')[str(message.from_user.id)]['miners']
    count = 0
    money_per_15_min = 0

    for miner in miners:
        money_per_15_min += miners[miner]['pow'] * miners[miner]['count']
        count += miners[miner]['count']
    text = f"""
➖➖➖➖➖➖➖➖➖➖➖
ℹ️ Информация о вас

🔑 Логин: @{message.from_user.username}
🆔 ID: {message.from_user.id}

🔰 Префикс: {read_file('data/users.json')[str(message.from_user.id)]['user_prefix']}
💸 Баланс b-cash: {add_thousands_separator(round(Rbalance, 8))}
🪙 Баланас BebraCoin'ов: {add_thousands_separator(round(Bbalance, 8))}
💪 Мощность фермы: {round(money_per_15_min, 8)} BC/15 мин. (Кол-во машин: {count})
➖➖➖➖➖➖➖➖➖➖➖
"""
    if message.chat.type == "private":
        await message.answer(text, reply_markup=types.ReplyKeyboardMarkup(keyboard=main_btn, resize_keyboard=True))
    else:
        await message.reply(text)



    
# async def i_dont_know(message: types.Message, bot: Bot):
#     await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAMNZg7vy4TrMLA2Q5UfHuDtK5cIN4UAAjAAA9UIjTlQ-8E00w8ezjQE') 

async def delete_panel(message: types.Message):
    await message.answer("Панель удалена.", reply_markup=types.ReplyKeyboardRemove())


async def farm_command(message: types.Message, appscheduler: AsyncIOScheduler, bot: Bot):
    data.check_user(message.from_user.id)
    miners = read_file('data/users.json')[str(message.from_user.id)]['miners']
    count = 0
    money_per_15_min = 0

    for miner in miners:
        money_per_15_min += miners[miner]['pow'] * miners[miner]['count']
        count += miners[miner]['count']
    await message.reply(f"У вас {count} майнер(-ов).\n\nДоход: {round(money_per_15_min, 6)} BCoins/15 минут.")

    appscheduler.add_job(get_bebra_coins, trigger='interval', minutes=15, kwargs={'plus': round(money_per_15_min, 6), 'chat_id': message.from_user.id})


async def shop_command(message: types.Message):
    data.check_user(message.from_user.id)
    current = datetime.now()
    current_date = ("0" + str(current.day) if current.day < 10 else str(current.day)) + "." + ("0" + str(current.month) if current.month < 10 else str(current.month)) + "." + str(current.year)[2:]

    await message.reply(f"Магазин на {current_date}\nОбновление магазина происходит каждый день в 21:00 по МСК. ", reply_markup=shop_btn())



async def trade_command(message: types.Message):
    data.check_user(message.from_user.id)
    key = InlineKeyboardBuilder()
    key.button(text='Обменять', callback_data='p2p')
    await message.reply(f"Здесь можно обменять свои BebraCoin'ы на b-cash.\n\nКурс на данный момент:\n1 BebraCoin = {add_thousands_separator(Data().rate)} b-cash.", reply_markup=key.as_markup())


async def help_command(message: types.Message):
    await message.reply("Появились вопросы/Нужна помощь?\n\nНапиши @ArtizSQ\nКанал: @bebra_miner_news")
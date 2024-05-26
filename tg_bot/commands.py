from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file
from datetime import datetime, timedelta
from utils.data import add_thousands_separator, get_ability
from tg_bot.events import get_bebra_coins
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.parsing import Data
from tg_bot.key import shop_btn, main_btn, ivent_shop

from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Promo(StatesGroup):
    text = State()

async def start_command(message: types.Message):
    data.check_user(message.from_user.id)
    

    text = """
👋 Добро пожаловать в бота <b>Bebra Miner</b>! 

🤖 Майни особые BebraCoin'ы и покупай новое оборудование для майнинга!


<i>⚠️ Все покупки, совершенные в боте являются виртуальными.
Бот не имеет ничего общего с обычными майнерами и майнингом. Бот является игровым, а не коммерческим.</i>

"""
    if message.chat.type == "private":
        await message.reply(text + "\n\n👇 Для продолжения нажми на одну из кнопок ", reply_markup=main_btn())
    else:
        await message.reply(text + "\n\n👇 Для продолжения нажми на одну из команд или введи ее вручную")


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
    rouded_money = round(money_per_15_min, 5)
    time = 15
    if read_file('data/users.json')[str(message.from_user.id)]['user_prefix'] in read_file('data/items/prefixes.json'):
        ability = get_ability(message.from_user.id, read_file('data/users.json')[str(message.from_user.id)]['user_prefix'])
        if ability.startswith('add'):
            rouded_money += rouded_money * float(ability.split('_')[1]) / 100
            
        elif ability.startswith('speed'):
            time -= int(ability.split('_')[1])
    appscheduler.add_job(get_bebra_coins, trigger='interval', minutes=time, kwargs={'plus': rouded_money, 'chat_id': message.from_user.id})
    await message.reply(f"📝 У вас {count} майнер(-ов).\n\n💸 Доход: {rouded_money} BCoins/{time} минут.")

    


async def shop_command(message: types.Message):
    data.check_user(message.from_user.id)
    current = datetime.now()
    current_date = ("0" + str(current.day) if current.day < 10 else str(current.day)) + "." + ("0" + str(current.month) if current.month < 10 else str(current.month)) + "." + str(current.year)[2:]

    await message.reply(f"🛒 Магазин на {current_date}\nОбновление магазина происходит каждый день в 21:00 по МСК. ", reply_markup=shop_btn())



async def trade_command(message: types.Message, bot: Bot):
    data.check_user(message.from_user.id)
    key = InlineKeyboardBuilder()
    rate_data = read_file('data/rate_info.json')
    key.button(text='Обменять', callback_data='p2p')
    image = types.FSInputFile(path='data/graph.png')

    await bot.send_photo(chat_id=message.from_user.id, photo=image) 
    await message.reply(f"Здесь можно обменять свои BebraCoin'ы на b-cash.\n\nКурс на данный момент:\n1 BebraCoin = {add_thousands_separator(Data().rate)} b-cash.", reply_markup=key.as_markup())


async def ivent_command(message: types.Message):
    await message.reply("Ивентовый магазин со своими уникальными товарами\n\nОбновление магазина происходит каждые 12 часов\n", reply_markup=ivent_shop())


async def promocode_command(message: types.Message, state: FSMContext):
    key = InlineKeyboardBuilder()
    key.button(text="Отмена", callback_data="cancel")
    await message.reply(f"Введите промокод:", reply_markup=key.as_markup())
    await state.set_state(Promo.text)


    
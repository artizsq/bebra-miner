from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from utils.data import read_file, save_file
from utils.data import add_thousands_separator
from utils.parsing import Data
import random

def shop_btn():
    data = read_file('data/current_shop.json')
    kb = InlineKeyboardBuilder()
    item1 = data[0]
    item2 = data[1]
    item3 = data[2]
    item4 = data[3]
    kb.button(text=item1 + " | " + add_thousands_separator(read_file('data/shop_items.json')[item1]['price']) + " b-cash", callback_data=f"_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(read_file('data/shop_items.json')[item2]['price']) + " b-cash", callback_data=f"_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(read_file('data/shop_items.json')[item3]['price']) + " b-cash", callback_data=f"_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(read_file('data/shop_items.json')[item4]['price']) + " b-cash", callback_data=f"_{item4}")
    kb.adjust(1)
    return kb.as_markup()


def ivent_shop():
    data = Data()
    current_shop = read_file(f'data/{data.event_name}/shop.json')
    shop_data = read_file(f'data/{data.event_name}/event_miners.json')

    kb = InlineKeyboardBuilder()
    item1 = current_shop[0]
    item2 = current_shop[1]
    item3 = current_shop[2]
    item4 = current_shop[3]
    item5 = current_shop[4]
    kb.button(text=item1 + " | " + add_thousands_separator(shop_data[item1]['price']) + " b-cash", callback_data=f"ev_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(shop_data[item2]['price']) + " b-cash", callback_data=f"ev_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(shop_data[item3]['price']) + " b-cash", callback_data=f"ev_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(shop_data[item4]['price']) + " b-cash", callback_data=f"ev_{item4}")
    kb.button(text=item5 + " | " + add_thousands_separator(shop_data[item5]['price']) + " b-cash", callback_data=f"ev_{item5}")
    kb.adjust(1)
    return kb.as_markup()

    


def main_btn():
    data = Data()
    btn = [
            [types.KeyboardButton(text="📈 Ферма"), types.KeyboardButton(text="👤 Профиль")],
            [types.KeyboardButton(text="🔁 Обменник"), types.KeyboardButton(text="🛒 Магазин")],
            [types.KeyboardButton(text="🆘 Помощь")]
        ]
    if data.isEvent == True:
        btn.append([types.KeyboardButton(text="⌛️ Ивент")])
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return kb
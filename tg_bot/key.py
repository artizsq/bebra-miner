from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram import types
from utils.data import read_file, save_file
from utils.data import add_thousands_separator
from utils.parsing import Data
import random


def shop_btn():
    key =  InlineKeyboardBuilder()
    miners = InlineKeyboardButton(text="Майнеры", callback_data="shop_miners")
    prefix = InlineKeyboardButton(text="Префиксы", callback_data="shop_prefix")
    key.add(miners, prefix)
    return key.as_markup()

def shop_miners():
    data = read_file('data/shop/miners.json')
    kb = InlineKeyboardBuilder()
    item1 = data[0]
    item2 = data[1]
    item3 = data[2]
    item4 = data[3]
    item5 = data[4]
    item6  = data[5]
    kb.button(text=item1 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item1]['price']) + " b-cash", callback_data=f"_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item2]['price']) + " b-cash", callback_data=f"_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item3]['price']) + " b-cash", callback_data=f"_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item4]['price']) + " b-cash", callback_data=f"_{item4}")
    kb.button(text=item5 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item5]['price']) + " b-cash", callback_data=f"_{item5}")
    kb.button(text=item6 + " | " + add_thousands_separator(read_file('data/items/miners.json')[item6]['price']) + " b-cash", callback_data=f"_{item6}")
    kb.adjust(1)
    return kb.as_markup()

def shop_prefixes():
    data = read_file('data/shop/prefixes.json')
    kb = InlineKeyboardBuilder()
    item1 = data[0]
    item2 = data[1]
    item3 = data[2]
    item4 = data[3]
    kb.button(text=item1 + " | " + add_thousands_separator(read_file('data/items/prefixes.json')[item1]['price']) + " b-cash", callback_data=f"p_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(read_file('data/items/prefixes.json')[item2]['price']) + " b-cash", callback_data=f"p_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(read_file('data/items/prefixes.json')[item3]['price']) + " b-cash", callback_data=f"p_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(read_file('data/items/prefixes.json')[item4]['price']) + " b-cash", callback_data=f"p_{item4}")
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
    kb.button(text=item1 + " | " + add_thousands_separator(shop_data[item1]['price']) + " b-cash", callback_data=f"event_shop_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(shop_data[item2]['price']) + " b-cash", callback_data=f"event_shop_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(shop_data[item3]['price']) + " b-cash", callback_data=f"event_shop_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(shop_data[item4]['price']) + " b-cash", callback_data=f"event_shop_{item4}")
    kb.button(text=item5 + " | " + add_thousands_separator(shop_data[item5]['price']) + " b-cash", callback_data=f"event_shop_{item5}")
    kb.adjust(1)
    return kb.as_markup()

    


def main_btn():
    data = Data()
    btn = [
            [types.KeyboardButton(text="📈 Ферма"), types.KeyboardButton(text="👤 Профиль")],
            [types.KeyboardButton(text="🔁 Обменник"), types.KeyboardButton(text="🛒 Магазин")]
        ]
    if data.isEvent == True:
        btn.append([types.KeyboardButton(text="⌛️ Ивент")])
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return kb




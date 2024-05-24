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

def shop_miners(ability, user_id):
    data = read_file('data/shop/miners.json')
    miner_data = read_file('data/items/miners.json')
    kb = InlineKeyboardBuilder()
    item1 = data[0]
    item2 = data[1]
    item3 = data[2]
    item4 = data[3]
    item5 = data[4]
    item6  = data[5]

    price1 = miner_data[item1]['price'] 
    price2 = miner_data[item2]['price'] 
    price3 = miner_data[item3]['price'] 
    price4 = miner_data[item4]['price'] 
    price5 = miner_data[item5]['price'] 
    price6 = miner_data[item6]['price']

    
    user_data = read_file('data/users.json')
    if user_data[str(user_id)]['user_prefix'] in read_file('data/items/prefixes.json'):
        if ability.startswith('shop'):
            price1 -= miner_data[item1]['price'] * int(ability.split('_')[1]) / 100
            price2 -= miner_data[item2]['price'] * int(ability.split('_')[1]) / 100
            price3 -= miner_data[item3]['price'] * int(ability.split('_')[1]) / 100
            price4 -= miner_data[item4]['price'] * int(ability.split('_')[1]) / 100
            price5 -= miner_data[item5]['price'] * int(ability.split('_')[1]) / 100
            price6 -= miner_data[item6]['price'] * int(ability.split('_')[1]) / 100


    kb.button(text=item1 + " | " + add_thousands_separator(round(price1, 2)) + " b-cash", callback_data=f"_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(round(price2, 2)) + " b-cash", callback_data=f"_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(round(price3, 2)) + " b-cash", callback_data=f"_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(round(price4, 2)) + " b-cash", callback_data=f"_{item4}")
    kb.button(text=item5 + " | " + add_thousands_separator(round(price5, 2)) + " b-cash", callback_data=f"_{item5}")
    kb.button(text=item6 + " | " + add_thousands_separator(round(price6, 2)) + " b-cash", callback_data=f"_{item6}")
    kb.adjust(1)
    return kb.as_markup()

def shop_prefixes(ability, user_id):
    data = read_file('data/shop/prefixes.json')
    prefix_data = read_file('data/items/prefixes.json')
    kb = InlineKeyboardBuilder()
    item1 = data[0]
    item2 = data[1]
    item3 = data[2]
    item4 = data[3]

    price1 = prefix_data[item1]['price'] 
    price2 = prefix_data[item2]['price'] 
    price3 = prefix_data[item3]['price'] 
    price4 = prefix_data[item4]['price'] 


    
    user_data = read_file('data/users.json')
    if user_data[str(user_id)]['user_prefix'] in read_file('data/items/prefixes.json'):
        if ability.startswith('shop'):
            price1 -= prefix_data[item1]['price'] * int(ability.split('_')[1]) / 100
            price2 -= prefix_data[item2]['price'] * int(ability.split('_')[1]) / 100
            price3 -= prefix_data[item3]['price'] * int(ability.split('_')[1]) / 100
            price4 -= prefix_data[item4]['price'] * int(ability.split('_')[1]) / 100

    kb.button(text=item1 + " | " + add_thousands_separator(round(price1, 2)) + " b-cash", callback_data=f"p_{item1}")
    kb.button(text=item2 + " | " + add_thousands_separator(round(price2, 2)) + " b-cash", callback_data=f"p_{item2}")
    kb.button(text=item3 + " | " + add_thousands_separator(round(price3, 2)) + " b-cash", callback_data=f"p_{item3}")
    kb.button(text=item4 + " | " + add_thousands_separator(round(price4, 2)) + " b-cash", callback_data=f"p_{item4}")
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




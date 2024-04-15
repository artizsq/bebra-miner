from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import read_file, save_file
from utils.data import add_thousands_separator
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
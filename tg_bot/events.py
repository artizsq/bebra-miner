from aiogram import Bot, types
import random
from utils.data import read_file, save_file
from utils.parsing import Data
from utils.data import add_bebra_coins
data = Data()

async def get_bebra_coins(plus, chat_id: int):
    add_bebra_coins(chat_id, plus)


async def update_current_shop(bot: Bot):
    shop_data = read_file('data/shop_items.json')
    current_shop = read_file('data/current_shop.json')
    
    current_shop.clear()  # Очищаем текущий магазин
    
    # Выбираем уникальные 4 предмета
    random_items = random.sample(list(shop_data), k=4)
    print(random_items)

    current_shop = random_items
    
    save_file('data/current_shop.json', current_shop)

    for admin in data.admin_ids:
        await bot.send_message(admin, "Магазин обновлен!")

async def update_rate(bot: Bot):
    data = Data()
    plus_minus = random.randint(0, 1)
    rate = data.rate
    if plus_minus == 0:
        rate += random.randint(0, 20000)
        data.update('Bot', 'rate', rate)
    else:
        rate -= random.randint(0, 20000)
        data.update('Bot', 'rate', rate)

    for admin in data.admin_ids:
        await bot.send_message(admin, "Курс обновлен!\nТекущий курс: " + str(rate))

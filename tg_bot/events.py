from aiogram import Bot, types
import random
import matplotlib.pyplot as plt
from utils.data import read_file, save_file
from utils.parsing import Data
from utils.data import add_bebra_coins



async def get_bebra_coins(plus, chat_id: int):
    add_bebra_coins(chat_id, plus)


async def update_current_shop(bot: Bot):
    data = Data()
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
        await bot.send_message(admin, "Курс обновлен!\n\nТекущий курс: " + str(rate))

    rate_data = read_file('data/rate_info.json')
    rate_data.append(rate)
    save_file('data/rate_info.json', rate_data)
    plt.title("График изменения курса")
    plt.grid(True)
    plt.plot(rate_data, color='black', label="Курс")
    plt.ylabel('Значение курса')
    plt.legend()

    # Показать график
    plt.savefig('data/graph.png')

    


# Построить график



def update_event(bot: Bot):
    data = Data()
    shop_data = read_file(f'data/{data.event_name}/event_miners.json')
    current_shop = read_file(f'data/{data.event_name}/shop.json')
    
    current_shop.clear()  # Очищаем текущий магазин
    
    # Выбираем уникальные 4 предмета
    random_items = random.sample(list(shop_data), k=5)
    print(random_items)

    current_shop = random_items
    
    save_file(f'data/{data.event_name}/shop.json', current_shop)
    
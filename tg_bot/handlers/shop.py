from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file, add_miners, save_file
from utils.data import add_thousands_separator, retranslate_prefix, get_ability, convert_number
import json
from tg_bot.key import shop_btn, shop_miners, shop_prefixes
from utils.parsing import Data




class ShopMiner:

    async def buy_event_miner(callback_query: types.CallbackQuery):
        data = Data()
        miner = callback_query.data.split('_')[2]
        count = int(callback_query.data.split('_')[1])
        user_data = read_file('data/users.json')
        miner_data = read_file(f'data/{Data().event_name}/event_miners.json')
        if user_data[str(callback_query.from_user.id)]['Rbalance'] < miner_data[miner]['price']:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(miner_data[miner]['price'] - user_data[str(callback_query.from_user.id)]['Rbalance'], 8))) + " b-cash", show_alert=True)
        else:
            user_data[str(callback_query.from_user.id)]['Rbalance'] -= miner_data[miner]['price']
            if miner not in user_data[str(callback_query.from_user.id)]['miners']:
                user_data[str(callback_query.from_user.id)]['miners'][miner] = {
                    'pow': miner_data[miner]['pow'],
                    'count': count
                }
                save_file('data/users.json', user_data)
            else:
                user_data[str(callback_query.from_user.id)]['miners'][miner]['count'] += count
            save_file('data/users.json', user_data)

            await callback_query.answer("✅ Вы купили " + miner + " за " + str(add_thousands_separator(miner_data[miner]['price'])) + " b-cash!\nКоличество: " + str(count) + "\nК вашему текущему фарму прибавилось +" + str(miner_data[miner]['pow'] * 8), show_alert=True)


    async def buy_miner(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        miner = callback_query.data.split('_')[2]
        count = int(callback_query.data.split('_')[1])
        miner_data = read_file('data/items/miners.json')
        Rbalance = read_file('data/users.json')[str(user_id)]['Rbalance']
        user_data = read_file('data/users.json')
        price = miner_data[miner]['price']
        if user_data[str(callback_query.from_user.id)]['user_prefix'] in read_file('data/items/prefixes.json'):
            ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
            if ability.startswith('shop'):
                price -= miner_data[miner]['price'] * int(ability.split('_')[1]) / 100
        if Rbalance < price:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(price * count - Rbalance, 8))) + " b-cash")
        else:
            user_data = read_file('data/users.json')
            user_data[str(user_id)]['Rbalance'] -= price * count
            if miner not in user_data[str(user_id)]['miners']:
                user_data[str(user_id)]['miners'][miner] = {
                    'pow': read_file('data/items/miners.json')[miner]['pow'],
                    'count': count
                }
            else:
                user_data[str(user_id)]['miners'][miner]['count'] += count
            save_file('data/users.json', user_data)
            power = read_file('data/items/miners.json')[miner]['pow'] * count
            await callback_query.answer("✅ Вы купили " + miner + " за " + str(add_thousands_separator(price * count)) + " b-cash!\n🔢 Количество: " + str(count) + "\n🔋 К вашему текущему фарму прибавилось " + str(round(power, 6)), show_alert=True)


    async def check_miner_info(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')
        miner_data = read_file('data/items/miners.json')
        miner = callback_query.data.split('_')[1]
        key.button(text="1", callback_data=f"b_1_{miner}")
        key.button(text="5", callback_data=f"b_5_{miner}")
        key.button(text="10", callback_data=f"b_10_{miner}")
        price = miner_data[miner]['price']
        if user_data[str(callback_query.from_user.id)]['user_prefix'] in read_file('data/items/prefixes.json'):
            ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
            if ability.startswith('shop'):
                price -= miner_data[miner]['price'] * int(ability.split('_')[1]) / 100

        power = miner_data[miner]['pow']
        await callback_query.message.edit_text(f"❇️ Вы выбрали майнер: {miner}\n💵 Цена: {add_thousands_separator(price)} b-cash\n🔋 Мощность: {power} BC/15 мин.\n\nВыберите количество, которое хотите купить: ", reply_markup=key.as_markup())

    async def check_miner_info_event(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')[str(callback_query.from_user.id)]
        miner_data = read_file(f'data/{Data().event_name}/event_miners.json')
        miner = callback_query.data.split('_')[2]
        key.button(text="1", callback_data=f"ev_1_{miner}")
        key.button(text="5", callback_data=f"ev_5_{miner}")
        key.button(text="10", callback_data=f"ev_10_{miner}")
        await callback_query.message.edit_text(f"❇️ Вы выбрали майнер: {miner}\n💵 Цена: {add_thousands_separator(round(miner_data[miner]['price'], 2))} b-cash\n🔋 Мощность: {int(miner_data[miner]['pow'])} BC/15 мин.", reply_markup=key.as_markup())



    async def  all_shop_miners(callback_query: types.CallbackQuery):
        user_data = read_file('data/users.json')
        ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
        user_id = callback_query.from_user.id
        await callback_query.message.edit_text("🛒 Магазин майнеров", reply_markup=shop_miners(ability, user_id))


class ShopPrefix():
    async def all_shop_prefixes(callback_query: types.CallbackQuery):
        user_data = read_file('data/users.json')
        ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
        user_id = callback_query.from_user.id
        await callback_query.message.edit_text("🛒 Магазин префиксов", reply_markup=shop_prefixes(ability, user_id))

    async def check_prefix_info(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')
        prefix = callback_query.data.split('_')[1]
        prefix_data = read_file('data/items/prefixes.json')
        key.button(text='Купить', callback_data=f"pre_{prefix}")
        price = prefix_data[prefix]['price']
        if user_data[str(callback_query.from_user.id)]['user_prefix'] in read_file('data/items/prefixes.json'):
            ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
            if ability.startswith('shop'):
                price -= prefix_data[prefix]['price'] * int(ability.split('_')[1]) / 100
        await callback_query.message.edit_text(f"❇️ Вы выбрали перфикс: {prefix}\n💵 Цена: {add_thousands_separator(price)} b-cash\n⭐️ Способность: <i>{retranslate_prefix(prefix)}</i>", reply_markup=key.as_markup())

    async def buy_prefix(callback_query: types.CallbackQuery):
        data = Data()
        prefix = callback_query.data.split('_')[1]
        user_data = read_file('data/users.json')
        prefix_data = read_file('data/items/prefixes.json')
        price = prefix_data[prefix]['price']
        if user_data[str(callback_query.from_user.id)]['user_prefix'] in read_file('data/items/prefixes.json'):
            ability = get_ability(callback_query.from_user.id, user_data[str(callback_query.from_user.id)]['user_prefix'])
            if ability.startswith('shop'):
                price -= prefix_data[prefix]['price'] * int(ability.split('_')[1]) / 100
        if user_data[str(callback_query.from_user.id)]['Rbalance'] < prefix_data[prefix]['price']:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(price - user_data[str(callback_query.from_user.id)]['Rbalance'], 8))) + " b-cash", show_alert=True)
        
        elif prefix in user_data[str(callback_query.from_user.id)]['prefix']:
            await callback_query.answer("✅ Вы уже купили этот префикс!", show_alert=True)
        else:
            user_data[str(callback_query.from_user.id)]['Rbalance'] -= prefix_data[prefix]['price'] + price
            user_data[str(callback_query.from_user.id)]['prefix'].append(prefix)
            print(prefix)
            save_file('data/users.json', user_data)
            await callback_query.answer("✅ Вы купили префикс " + prefix + " за " + str(add_thousands_separator(price)) + " b-cash!", show_alert=True)


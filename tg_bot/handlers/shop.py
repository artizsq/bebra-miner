from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file, add_miners, save_file
from utils.data import add_thousands_separator
import json
from tg_bot.key import shop_btn, shop_miners, shop_prefixes
from utils.parsing import Data




class ShopMiner:

    async def buy_event_miner(callback_query: types.CallbackQuery):
        data = Data()
        miner = callback_query.data.split('_')[1]
        user_data = read_file('data/users.json')
        miner_data = read_file(f'data/{Data().event_name}/event_miners.json')
        if user_data[str(callback_query.from_user.id)]['Rbalance'] < miner_data[miner]['price']:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(miner_data[miner]['price'] - user_data[str(callback_query.from_user.id)]['Rbalance'], 8))) + " b-cash")
        else:
            user_data[str(callback_query.from_user.id)]['Rbalance'] -= miner_data[miner]['price']
            if miner not in user_data[str(callback_query.from_user.id)]['miners']:
                user_data[str(callback_query.from_user.id)]['miners'][miner] = {
                    'pow': miner_data[miner]['pow'],
                    'count': 1
                }
                save_file('data/users.json', data)
            else:
                user_data[str(callback_query.from_user.id)]['miners'][miner]['count'] += 1
            save_file('data/users.json', user_data)

            await callback_query.answer("✅ Вы купили " + miner + " за " + str(add_thousands_separator(miner_data[miner]['price'])) + " b-cash!\n➕ К вашему текущему фарму прибавилось +" + str(miner_data[miner]['pow']), show_alert=True)


    async def buy_miner(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        miner = callback_query.data.split('_')[1]
        price = read_file('data/items/miners.json')[miner]['price']
        Rbalance = read_file('data/users.json')[str(user_id)]['Rbalance']

        if Rbalance < price:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(price - Rbalance, 8))) + " b-cash")
        else:
            user_data = read_file('data/users.json')
            user_data[str(user_id)]['Rbalance'] -= price
            if miner not in user_data[str(user_id)]['miners']:
                user_data[str(user_id)]['miners'][miner] = {
                    'pow': read_file('data/items/miners.json')[miner]['pow'],
                    'count': 1
                }
            else:
                user_data[str(user_id)]['miners'][miner]['count'] += 1
            save_file('data/users.json', user_data)

            await callback_query.answer("✅ Вы купили " + miner + " за " + str(add_thousands_separator(price)) + " b-cash!\n➕ К вашему текущему фарму прибавилось +" + str(read_file('data/items/miners.json')[miner]['pow']), show_alert=True)


    async def check_miner_info(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')[str(callback_query.from_user.id)]
        miner_data = read_file('data/items/miners.json')
        miner = callback_query.data.split('_')[1]
        key.button(text='Купить', callback_data=f"b_{miner}")
        await callback_query.message.edit_text(f"❇️ Вы выбрали майнер: {miner}\n💵 Цена: {add_thousands_separator(miner_data[miner]['price'])} b-cash\n🔋 Мощность: {miner_data[miner]['pow']} BC/15 мин.", reply_markup=key.as_markup())

    async def check_miner_info_event(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')[str(callback_query.from_user.id)]
        miner_data = read_file(f'data/{Data().event_name}/event_miners.json')
        miner = callback_query.data.split('_')[2]
        key.button(text='Купить', callback_data=f"ev_{miner}")
        await callback_query.message.edit_text(f"❇️ Вы выбрали майнер: {miner}\n💵 Цена: {add_thousands_separator(miner_data[miner]['price'])} b-cash\n🔋 Мощность: {miner_data[miner]['pow']} BC/15 мин.", reply_markup=key.as_markup())


    async def  all_shop_miners(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("🛒 Магазин майнеров", reply_markup=shop_miners())


class ShopPrefix():
    async def all_shop_prefixes(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("🛒 Магазин префиксов", reply_markup=shop_prefixes())

    async def check_prefix_info(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')[str(callback_query.from_user.id)]
        miner = callback_query.data.split('_')[1]
        prefix_data = read_file('data/items/prefixes.json')
        key.button(text='Купить', callback_data=f"pre_{miner}")
        await callback_query.message.edit_text(f"❇️ Вы выбрали перфикс: {miner}\n💵 Цена: {add_thousands_separator(prefix_data[miner]['price'])} b-cash\n⭐️ Способность: <i>Недоступно</i>", reply_markup=key.as_markup())

    async def buy_prefix(callback_query: types.CallbackQuery):
        data = Data()
        prefix = callback_query.data.split('_')[1]
        user_data = read_file('data/users.json')
        prefix_data = read_file('data/items/prefixes.json')
        if user_data[str(callback_query.from_user.id)]['Rbalance'] < prefix_data[prefix]['price']:
            await callback_query.answer("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(round(prefix_data[prefix]['price'] - user_data[str(callback_query.from_user.id)]['Rbalance'], 8))) + " b-cash")
        
        elif prefix in user_data[str(callback_query.from_user.id)]['prefix']:
            await callback_query.answer("✅ Вы уже купили этот префикс!", show_alert=True)
        else:
            user_data[str(callback_query.from_user.id)]['Rbalance'] -= prefix_data[prefix]['price']
            user_data[str(callback_query.from_user.id)]['prefix'].append(prefix)
            print(prefix)
            save_file('data/users.json', user_data)
            await callback_query.answer("✅ Вы купили префикс " + prefix + " за " + str(add_thousands_separator(prefix_data[prefix]['price'])) + " b-cash!", show_alert=True)


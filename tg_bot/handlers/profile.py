from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file, save_file, converter
from utils.data import add_thousands_separator, retranslate_prefix

from utils.parsing import Data



class Profile:
    async def profile_command_inline(callback_query: types.CallbackQuery):
        converter(callback_query.from_user.id)
        key = InlineKeyboardBuilder()

        key.button(text='🔋 Мои машины', callback_data='all_miners')
        key.button(text='⭐️ Мои префиксы', callback_data='all_prefixes')

        data.check_user(callback_query.from_user.id)
        Rbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Rbalance']
        Bbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Bbalance']
        miners = read_file('data/users.json')[str(callback_query.from_user.id)]['miners']
        prefix = read_file('data/users.json')[str(callback_query.from_user.id)]['user_prefix']
        count = 0
        money_per_15_min = 0

        for miner in miners:
            money_per_15_min += miners[miner]['pow'] * miners[miner]['count']
            count += miners[miner]['count']
        text = f"""
    ➖➖➖➖➖➖➖➖➖➖➖
ℹ️ Информация о вас

🔑 Логин: @{callback_query.from_user.username}
🆔 ID: {callback_query.from_user.id}

🔰 Префикс: <b>{read_file('data/users.json')[str(callback_query.from_user.id)]['user_prefix']}</b>
⭐️ Способность: <i>{retranslate_prefix(prefix)}</i>

💸 Баланс b-cash: {add_thousands_separator(round(Rbalance, 5))}
🪙 Баланас BebraCoin'ов: {add_thousands_separator(round(Bbalance, 8))}
💪 Мощность фермы: {round(money_per_15_min, 5)} BC/15 мин. ({count} майнеров)
➖➖➖➖➖➖➖➖➖➖➖
    """
        await callback_query.message.edit_text(text, reply_markup=key.as_markup())



    async def profile_command(message: types.Message):
        converter(message.from_user.id)
        key = InlineKeyboardBuilder()

        key.button(text='🔋 Мои машины', callback_data='all_miners')
        key.button(text='⭐️ Мои префиксы', callback_data='all_prefixes')

        data.check_user(message.from_user.id)
        Rbalance = read_file('data/users.json')[str(message.from_user.id)]['Rbalance']
        Bbalance = read_file('data/users.json')[str(message.from_user.id)]['Bbalance']
        miners = read_file('data/users.json')[str(message.from_user.id)]['miners']
        count = 0
        prefix = read_file('data/users.json')[str(message.from_user.id)]['user_prefix']
        money_per_15_min = 0

        for miner in miners:
            money_per_15_min += miners[miner]['pow'] * miners[miner]['count']
            count += miners[miner]['count']
        text = f"""
➖➖➖➖➖➖➖➖➖➖➖
ℹ️ Информация о вас

🔑 Логин: @{message.from_user.username}
🆔 ID: {message.from_user.id}

🔰 Префикс: <b>{read_file('data/users.json')[str(message.from_user.id)]['user_prefix']}</b>
⭐️ Способность: <i>{retranslate_prefix(prefix)}</i>

💸 Баланс b-cash: {add_thousands_separator(round(Rbalance, 5))}
🪙 Баланас BebraCoin'ов: {add_thousands_separator(round(Bbalance, 5))}
💪 Мощность фермы: {round(money_per_15_min, 5)} BC/15 мин. ({count} майнеров)
➖➖➖➖➖➖➖➖➖➖➖
"""
        await message.reply(text, reply_markup=key.as_markup())



    async def change_prefix(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()
        key.button(text="Назад", callback_data="back_pr")

        prefix = callback_query.data.split('_')[1]
        data = read_file("data/users.json")
        data[str(callback_query.from_user.id)]["user_prefix"] = prefix
        save_file("data/users.json", data)
        ability = retranslate_prefix(prefix)

        await callback_query.message.edit_text(f"✅ Теперь ваш префикс: <b>{prefix}</b>\n⭐️ Способность: <i>{ability}</i>", parse_mode='HTML', reply_markup=key.as_markup())


    async def miner_info(callback_query: types.CallbackQuery):
        converter(callback_query.from_user.id)
        try:
            
            udata = read_file('data/users.json')
            miner = callback_query.data.split('_')[1]
            miners = udata[str(callback_query.from_user.id)]['miners']
            event_miners = read_file(f'data/{udata[str(callback_query.from_user.id)]["miners"][miner]["event"]}/event_miners.json')
            
            if miner in event_miners:
                mdata = event_miners[miner]
                event = mdata['event'] + ' (' + mdata['emoji'] + ')'
            else:
                mdata = read_file('data/items/miners.json')[miner]
                event = "Не найден"


            count = miners[miner]['count']
            key = InlineKeyboardBuilder()
            key.button(text="Назад", callback_data="back_m")
            await callback_query.message.edit_text(f"""
ℹ️<b>Информация о майнере {miner}</b>

▶️ Название: {miner}
🔋 Мощность (1 штука): {mdata['pow']} BC/15 мин
⌛️ Ивент: {event}

💵 Цена: {mdata['price']} b-cash
💪 Мощность (всех): {round(mdata['pow']*count, 5)} BC/15 мин
📝 Кол-во майнеров: {count}
    """, parse_mode='HTML', reply_markup=key.as_markup())

        except Exception as e:
            await callback_query.message.edit_text("⚠️ Ошибка при получении списка машин. Пожалуйста, сообщите администратору.", parse_mode='HTML')
            print(e)

            
    

    async def all_user_prefixes(callback_query: types.CallbackQuery):
        data = read_file('data/users.json')
        prefixes = data[str(callback_query.from_user.id)]['prefix']
        key = InlineKeyboardBuilder()
        for prefix in prefixes:
            key.button(text=prefix, callback_data=f"PR_{prefix}")
        key.button(text="Назад", callback_data="back_profile")
        key.adjust(1)

        await callback_query.message.edit_text("📝 Список всех ваших префиксов",parse_mode='HTML', reply_markup=key.as_markup())


    async def all_user_miners(callback_query: types.CallbackQuery):
        converter(callback_query.from_user.id)
        try:
            data = read_file('data/users.json')
            miners = data[str(callback_query.from_user.id)]['miners']
            key = InlineKeyboardBuilder()
            for miner in miners:
                event_miners = read_file(f'data/{data[str(callback_query.from_user.id)]["miners"][miner]["event"]}/event_miners.json')
                if miner in event_miners:
                    emoji = event_miners[miner]['emoji']
                else:
                    emoji = ''
                key.button(text=f'{emoji} {miner} | {miners[miner]["count"]}', callback_data=f"MI_{miner}")
            key.button(text="Назад", callback_data="back_profile")
            key.adjust(1)
            await callback_query.message.edit_text("🌟 Список всех ваших машин", parse_mode='HTML', reply_markup=key.as_markup())
        except Exception as e:

            await callback_query.message.edit_text("⚠️ Ошибка при получении списка машин. Пожалуйста, сообщите администратору.", parse_mode='HTML')
        
    

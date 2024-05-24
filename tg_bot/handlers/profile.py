from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file, save_file
from utils.data import add_thousands_separator, retranslate_prefix

from utils.parsing import Data



class Profile:
    async def profile_command_inline(callback_query: types.CallbackQuery):
        key = InlineKeyboardBuilder()

        key.button(text='🔋 Мои машины', callback_data='all_miners')
        key.button(text='⭐️ Мои префиксы', callback_data='all_prefixes')

        data.check_user(callback_query.from_user.id)
        Rbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Rbalance']
        Bbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Bbalance']
        miners = read_file('data/users.json')[str(callback_query.from_user.id)]['miners']
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
💸 Баланс b-cash: {add_thousands_separator(round(Rbalance, 8))}
🪙 Баланас BebraCoin'ов: {add_thousands_separator(round(Bbalance, 8))}
💪 Мощность фермы: {round(money_per_15_min, 8)} BC/15 мин. (Кол-во машин: {count})
➖➖➖➖➖➖➖➖➖➖➖
    """
        await callback_query.message.edit_text(text, reply_markup=key.as_markup())



    async def profile_command(message: types.Message):
        key = InlineKeyboardBuilder()

        key.button(text='🔋 Мои машины', callback_data='all_miners')
        key.button(text='⭐️ Мои префиксы', callback_data='all_prefixes')

        data.check_user(message.from_user.id)
        Rbalance = read_file('data/users.json')[str(message.from_user.id)]['Rbalance']
        Bbalance = read_file('data/users.json')[str(message.from_user.id)]['Bbalance']
        miners = read_file('data/users.json')[str(message.from_user.id)]['miners']
        count = 0
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
💸 Баланс b-cash: {add_thousands_separator(round(Rbalance, 8))}
🪙 Баланас BebraCoin'ов: {add_thousands_separator(round(Bbalance, 8))}
💪 Мощность фермы: {round(money_per_15_min, 8)} BC/15 мин. (Кол-во машин: {count})
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
        key = InlineKeyboardBuilder()
        key.button(text="Назад", callback_data="back_m")
        miner = callback_query.data.split('_')[1]
        data = read_file("data/items/miners.json")
        udata = read_file("data/users.json")
        try:
            mdata = data[miner]
        except KeyError:
            data = read_file(f"data/{Data().event_name}/event_miners.json")
            mdata = data[miner]
        count = udata[str(callback_query.from_user.id)]["miners"][miner]["count"]
        await callback_query.message.edit_text(f"""
ℹ️<b>Информация о майнере {miner}</b>

▶️ Название: {miner}
🔋 Мощность (1 штука): {mdata['pow']} BC/15 мин
{f'⌛️ Ивент: {Data().event_name} ({mdata["emoji"]})' if miner in read_file(f'data/{Data().event_name}/event_miners.json') else ""}

💵 Цена: {mdata['price']} b-cash
💪 Мощность (всех): {mdata['pow']*count} BC/15 мин
📝 Кол-во майнеров: {count}
                                            """, parse_mode='HTML', reply_markup=key.as_markup())
    

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

        data = read_file('data/users.json')
        miners = data[str(callback_query.from_user.id)]['miners']
        key = InlineKeyboardBuilder()
        user_data = read_file('data/users.json')
        for miner in miners:
            if miner in read_file(f"data/{Data().event_name}/event_miners.json"):
                emoji = read_file(f"data/{Data().event_name}/event_miners.json")[miner]['emoji']
                key.button(text=f'{emoji} {miner} | {user_data[str(callback_query.from_user.id)]["miners"][miner]["count"]}', callback_data=f"MI_{miner}")
            else:
                key.button(text=f'{miner} | {user_data[str(callback_query.from_user.id)]["miners"][miner]["count"]}', callback_data=f"MI_{miner}")
        key.button(text="Назад", callback_data="back_profile")
        key.adjust(1)
        

        await callback_query.message.edit_text("📝 Список всех ваших машин\n\n<i>[эмодзи ивента] Название машины | Количество машин</i>",parse_mode='HTML', reply_markup=key.as_markup())

    

from aiogram import types, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import read_file, add_miners, save_file, add_thousands_separator
from aiogram.fsm.context import FSMContext
from utils.parsing import Data
from aiogram.fsm.state import State, StatesGroup

class Trade(StatesGroup):
    coins = State()







async def check_miner_info(callback_query: types.CallbackQuery):
    key = InlineKeyboardBuilder()

    key.button(text='Купить', callback_data=f"b{callback_query.data}")
    user_data = read_file('data/users.json')[str(callback_query.from_user.id)]
    miner_data = read_file('data/shop_items.json')
    miner = callback_query.data.split('_')[1]
    await callback_query.message.edit_text(f"Вы выбрали майнер: {miner}\nЦена: {add_thousands_separator(miner_data[miner]['price'])} b-cash\nМощность: {miner_data[miner]['pow']} BC/15 мин.", reply_markup=key.as_markup())
    

    

async def buy_miner(callback_query: types.CallbackQuery):
    user_data = read_file('data/users.json')
    miner_data = read_file('data/shop_items.json')
    miner = callback_query.data.split('b_')[1]

    if user_data[str(callback_query.from_user.id)]['Rbalance'] < miner_data[miner]['price']:
        await callback_query.answer("Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(miner_data[miner]['price'] - user_data[str(callback_query.from_user.id)]['Rbalance'])) + " руб")
    else:
        user_data[str(callback_query.from_user.id)]['Rbalance'] -= miner_data[miner]['price']
        save_file('data/users.json', user_data)
        add_miners(callback_query.from_user.id, miner)
        await callback_query.answer("Вы купили " + miner + " за " + str(add_thousands_separator(miner_data[miner]['price'])) + " b-cash!\nК вашему текущему фарму прибавилось +" + str(miner_data[miner]['pow']))

async def trade_button(callback_query: types.CallbackQuery, state: FSMContext):
    key = InlineKeyboardBuilder()
    Bbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Bbalance']
    key.button(text='Отмена', callback_data='cancel')
    await callback_query.message.edit_text(f"Введите кол-во которое хотите обменять\n\nУ вас на балансе: {round(Bbalance, 8)} BebraCoin'ов", reply_markup=key.as_markup())
    await state.set_state(Trade.coins)


async def trade_coins(message: types.Message, state: FSMContext):
    data = read_file('data/users.json')
    key = InlineKeyboardBuilder()

    key.button(text='Отмена', callback_data='cancel')
    
    if message.text.replace(".", "", 1).isdigit():  # Проверяем, что введенное значение является числом
        Bbalance = data[str(message.from_user.id)]['Bbalance']
        Rbalance = data[str(message.from_user.id)]['Rbalance']
        try:
            amount = float(message.text)
            if amount > Bbalance:
                await message.reply("Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(amount - Bbalance)) + " BebraCoin'ов")
            else:
                data[str(message.from_user.id)]['Rbalance'] += Data().rate * amount
                data[str(message.from_user.id)]['Bbalance'] -= amount
                save_file('data/users.json', data)
                await message.reply(f"Вы обменяли {amount} BebraCoin'ов на {add_thousands_separator(Data().rate * amount)} b-cash")
                await state.clear()
        except ValueError:
            if int(amount) > Bbalance:
                await message.reply("Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(int(amount) - Bbalance)) + " BebraCoin'ов")
            else:
                data[str(message.from_user.id)]['Rbalance'] += round(Data().rate * int(amount), 8)
                data[str(message.from_user.id)]['Bbalance'] -= int(amount)
                save_file('data/users.json', data)
                await message.reply(f"Вы обменяли {amount} BebraCoin'ов на {add_thousands_separator(round(Data().rate * int(amount), 8))} b-cash")
                await state.clear()
    else:
        await message.reply("Пожалуйста, введите корректное число.", reply_markup=key.as_markup())
            

async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()


async def all_user_miners(callback_query: types.CallbackQuery):
    key = InlineKeyboardBuilder()
    data = read_file('data/users.json')
    miners = data[str(callback_query.from_user.id)]['miners']
    for miner in miners:
        key.button(text=f"{miner} | {miners[miner]['count']}", callback_data='MI_' + miner)
    key.adjust(1)

    await callback_query.message.edit_text("📝 Список всех ваших машин\n\n<i>Название машины | Количество машин</i>",parse_mode='HTML', reply_markup=key.as_markup())


async def all_user_prefixes(callback_query: types.CallbackQuery):
    key = InlineKeyboardBuilder()
    data = read_file('data/users.json')
    prefixes = data[str(callback_query.from_user.id)]['prefix']
    for prefix in prefixes:
        key.button(text=f"{prefix}", callback_data='PR_' + prefix)
    key.adjust(1)

    await callback_query.message.edit_text("📝 Список всех ваших префиксов",parse_mode='HTML', reply_markup=key.as_markup())


async def change_prefix(callback_query: types.CallbackQuery):
    data = read_file('data/users.json')
    prefix = callback_query.data.split('_')[1]
    data[str(callback_query.from_user.id)]['user_prefix'] = prefix
    save_file('data/users.json', data)
    await callback_query.message.edit_text(f"✅ Теперь ваш префикс: {prefix}")


async def miner_info(callback_query: types.CallbackQuery):
    key = InlineKeyboardBuilder()

    key.button(text="Назад", callback_data="back_m")

    mdata = read_file("data/shop_items.json")
    udata = read_file("data/users.json")
    miner = callback_query.data.split('_')[1]
    await callback_query.message.edit_text(f"""
<b>Информация о майнере {miner}</b>

--------------------------------
Название: {miner}
Мощность (1 штука): {mdata[miner]['pow']} BC/15 мин 

Цена: {mdata[miner]['price']} b-cash
Мощность (всех): {mdata[miner]['pow'] * udata[str(callback_query.from_user.id)]['miners'][miner]['count']} BC/15 мин
Кол-во майнеров: {udata[str(callback_query.from_user.id)]["miners"][miner]['count']}
                                       """, parse_mode='HTML', reply_markup=key.as_markup())
    


async def go_back(callback_query: types.CallbackQuery):
    choose = callback_query.data.split('_')[1]
    if choose == 'm':
        await all_user_miners(callback_query)
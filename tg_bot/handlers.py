from aiogram import types, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import read_file, add_miners, save_file
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
    await callback_query.message.edit_text(f"Вы выбрали майнер: {miner}\nЦена: {miner_data[miner]['price']} b-cash\nМощность: {miner_data[miner]['pow']} BC/15 мин.", reply_markup=key.as_markup())
    

    

async def buy_miner(callback_query: types.CallbackQuery):
    user_data = read_file('data/users.json')
    miner_data = read_file('data/shop_items.json')
    miner = callback_query.data.split('b_')[1]

    if user_data[str(callback_query.from_user.id)]['Rbalance'] < miner_data[miner]['price']:
        await callback_query.answer("Недостаточно средств на балансе!\nВам не хватает " + str(miner_data[miner]['price'] - user_data[str(callback_query.from_user.id)]['Rbalance']) + " руб")
    else:
        user_data[str(callback_query.from_user.id)]['Rbalance'] -= miner_data[miner]['price']
        save_file('data/users.json', user_data)
        add_miners(callback_query.from_user.id, miner)
        await callback_query.answer("Вы купили " + miner + " за " + str(miner_data[miner]['price']) + " b-cash!\nК вашему текущему фарму прибавилось +" + str(miner_data[miner]['pow']))

async def trade_button(callback_query: types.CallbackQuery, state: FSMContext):
    key = InlineKeyboardBuilder()
    Bbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Bbalance']
    key.button(text='Отмена', callback_data='cancel')
    await callback_query.message.edit_text(f"Введите кол-во которое хотите обменять\n\nУ вас на балансе: {round(Bbalance, 8)} BebraCoin'ов", reply_markup=key.as_markup())
    await state.set_state(Trade.coins)


async def trade_coins(message: types.Message, state: FSMContext):
    data = read_file('data/users.json')
    
    if message.text.replace(".", "", 1).isdigit():  # Проверяем, что введенное значение является числом
        Bbalance = data[str(message.from_user.id)]['Bbalance']
        Rbalance = data[str(message.from_user.id)]['Rbalance']
        try:
            amount = float(message.text)
            if amount > Bbalance:
                await message.reply("Недостаточно средств на балансе!\nВам не хватает " + str(amount - Bbalance) + " BebraCoin'ов")
            else:
                data[str(message.from_user.id)]['Rbalance'] += Data().rate * amount
                data[str(message.from_user.id)]['Bbalance'] -= amount
                save_file('data/users.json', data)
                await message.reply(f"Вы обменяли {amount} BebraCoin'ов на {Data().rate * amount} b-cash")
                await state.clear()
        except ValueError:
            if int(amount) > Bbalance:
                await message.reply("Недостаточно средств на балансе!\nВам не хватает " + str(int(amount) - Bbalance) + " BebraCoin'ов")
            else:
                data[str(message.from_user.id)]['Rbalance'] += round(Data().rate * int(amount), 8)
                data[str(message.from_user.id)]['Bbalance'] -= int(amount)
                save_file('data/users.json', data)
                await message.reply(f"Вы обменяли {amount} BebraCoin'ов на {round(Data().rate * int(amount), 8)} b-cash")
                await state.clear()
    else:
        await message.reply("Пожалуйста, введите корректное число.")
            

async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
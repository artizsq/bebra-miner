from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import data
from utils.data import read_file
from datetime import datetime, timedelta
from utils.data import add_thousands_separator
from tg_bot.events import get_bebra_coins

from aiogram import types, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import read_file, add_miners, save_file, add_thousands_separator
from aiogram.fsm.context import FSMContext
from utils.parsing import Data
import json
from aiogram.fsm.state import State, StatesGroup

class Trade(StatesGroup):
    coins = State()


class Trader:
    async def trade_button(callback_query: types.CallbackQuery, state: FSMContext):
        key = InlineKeyboardBuilder()
        key.button(text="Отменить", callback_data="cancel")
        Bbalance = read_file('data/users.json')[str(callback_query.from_user.id)]['Bbalance']
        await callback_query.message.edit_text(f"👉 Введите кол-во которое хотите обменять\n\n🪙 У вас на балансе: {round(Bbalance, 8)} BebraCoin'ов", reply_markup=key.as_markup())
        await state.set_state(Trade.coins)

    async def trade_coins(message: types.Message, state: FSMContext):
        data = read_file('data/users.json')

        key = InlineKeyboardBuilder()
        key.button(text='Отмена', callback_data='cancel')

        try:
            amount = float(message.text)
            if not isinstance(amount, float) or amount <= 0:
                await message.reply("❌ Число должно быть положительным и содержать десятичную точку.", reply_markup=key.as_markup())
            elif amount > data[str(message.from_user.id)]['Bbalance']:
                await message.reply("🚫 Недостаточно средств на балансе!\nВам не хватает " + str(add_thousands_separator(amount - data[str(message.from_user.id)]['Bbalance'])) + " BebraCoin'ов")
            else:
                data[str(message.from_user.id)]['Rbalance'] += Data().rate * amount
                data[str(message.from_user.id)]['Bbalance'] -= amount
                save_file('data/users.json', data)
                await message.reply(f"✅ Вы обменяли {amount} BebraCoin'ов на {add_thousands_separator(Data().rate * amount)} b-cash")
                await state.clear()
        except ValueError:
            await message.reply("🔄 Пожалуйста, введите корректное число.", reply_markup=key.as_markup())

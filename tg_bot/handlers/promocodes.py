
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import read_file, save_file, add_thousands_separator
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton

async def promocode_redeem(message: types.Message, state: FSMContext):
    await state.clear()
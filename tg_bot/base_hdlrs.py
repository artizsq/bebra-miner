from aiogram import types
from aiogram.fsm.context import FSMContext


async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()











        



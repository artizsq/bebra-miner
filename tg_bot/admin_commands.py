from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import parsing
from tg_bot.events import update_current_shop
from utils.data import read_file

async def delete_panel(message: types.Message):
    await message.answer("Панель удалена.", reply_markup=types.ReplyKeyboardRemove())


async def admin_panel(message: types.Message, bot: Bot):
    key = InlineKeyboardBuilder()
    key.button(text="Увеличить баланс", callback_data="add_balance")
    key.button(text="Уменьшить баланс", callback_data="sub_balance")
    key.button(text="Рассылка", callback_data="send")
    key.button(text="Забанить пользователя", callback_data="ban")
    key.button(text="Разбанить пользователя", callback_data="unban")
    key.button(text="Выгрузить БД", callback_data="upload")
    key.button(text="Обновить магазин", callback_data="update_shop")
    key.button(text="Обновить курс", callback_data="rate")
    key.adjust(2, 1, 2, 2)

    await message.reply("Админ панель: ", reply_markup=key.as_markup())
    for admin in parsing.Data().admin_ids:
        await bot.send_message(admin, f"Админ {message.from_user.id} зашел в панель администратора.")


async def update_shop_admin(callback_qeury: types.Message, bot: Bot):
    await update_current_shop(bot)
    await callback_qeury.answer("Магазин обновлен.")


async def send_BD(callback_qeury: types.Message, bot: Bot):
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/users.json'))
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/current_shop.json'))
    await callback_qeury.answer("БД выгружена.")


# async def send_notification(callback_qeury: types.Message, bot: Bot):
#     for user in read_file('data/users.json'):

#     await bot.send_message(callback_qeury.from_user.id, "Сообщение отправлено.")
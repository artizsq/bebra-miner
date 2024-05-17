from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.parsing import Data 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tg_bot.events import update_current_shop, update_rate
from utils.data import read_file, save_file

class Admin(StatesGroup):
    user_id = State()
    message = State()
    action = State()
    balance = State()
    ban = State()



async def delete_panel(message: types.Message):
    await message.answer("Панель удалена.", reply_markup=types.ReplyKeyboardRemove())


async def admin_panel(message: types.Message, bot: Bot):
    data = Data()
    for admin in data.admin_ids:
        await bot.send_message(admin, f"Админ {message.from_user.id} зашел в панель администратора.")
    
    key = InlineKeyboardBuilder()
    key.button(text="Увеличить баланс", callback_data="add_balance")
    key.button(text="Уменьшить баланс", callback_data="sub_balance")
    key.button(text="Рассылка", callback_data="send")
    key.button(text="Забанить пользователя", callback_data="ban")
    key.button(text="Разбанить пользователя", callback_data="unban")
    key.button(text="Выгрузить БД", callback_data="upload")
    key.button(text="Загрузить БД", callback_data="set")
    key.button(text="Обновить магазин", callback_data="update_shop")
    key.button(text="Обновить курс", callback_data="rate")
    key.adjust(2, 1, 2, 2)

    await message.reply("Админ панель: ", reply_markup=key.as_markup())
    


async def update_shop_admin(callback_qeury: types.CallbackQuery, bot: Bot):
    await update_current_shop(bot)
    


async def send_BD(callback_qeury: types.Message, bot: Bot):
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/users.json'))
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/shop/miners.json'))
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/shop/prefixes.json'))
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/config.ini'))
    await bot.send_document(callback_qeury.from_user.id, types.FSInputFile(path='data/rate_info.json')) 
    await callback_qeury.answer("БД выгружена.")


# async def send_notification(callback_qeury: types.Message, bot: Bot):
#     for user in read_file('data/users.json'):

#     await bot.send_message(callback_qeury.from_user.id, "Сообщение отправлено.")

async def update_rate_button(callback_qeury: types.CallbackQuery, bot: Bot):
    data = Data()
    await update_rate(bot)
    


async def add_balance(callback_qeury: types.CallbackQuery, bot: Bot, state: FSMContext):
    key = InlineKeyboardBuilder()
    key.button(text="Отмена", callback_data="cancel")
    await state.set_state(Admin.user_id)
    await state.set_data({'action': 'add'})
    await callback_qeury.message.edit_text("Введите ID пользователя: ", reply_markup=key.as_markup())


async def sub_balance(callback_qeury: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Admin.user_id)
    key = InlineKeyboardBuilder()
    key.button(text="Отмена", callback_data="cancel")
    await state.set_data({'action': 'sub'})
    await callback_qeury.message.edit_text("Введите ID пользователя: ", reply_markup=key.as_markup())


async def ban_user(callback_qeury: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Admin.ban)
    key = InlineKeyboardBuilder()
    key.button(text="Отмена", callback_data="cancel")
    await state.set_data({'action': 'ban'})
    await callback_qeury.message.edit_text("Введите ID пользователя: ", reply_markup=key.as_markup())

async def actions_with_balance(message: types.Message, state: FSMContext):
    key = InlineKeyboardBuilder()
    data = await state.get_data()
    
    key.button(text="Отмена", callback_data="cancel")
    if data['action'] == "add":
        await message.reply("Введите баланс который надо прибавить: ", reply_markup=key.as_markup())
        
    elif data['action'] == "sub":
        await message.reply("Введите баланс который надо отнять: ", reply_markup=key.as_markup())
    await state.set_data({'user_id': message.text, 'action': data['action']})
    await state.set_state(Admin.balance)


async def add_or_sub_balance(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_data = read_file('data/users.json')
    print(data)
    action = data['action']
    print(action)

    if action == "add":
        user_data[data['user_id']]['Rbalance'] += int(message.text)
        print(user_data[str(message.from_user.id)]['Rbalance'] + int(message.text))
    elif action == "sub":
        user_data[data['user_id']]['Rbalance'] -= int(message.text)
        print(data['user_id']['Rbalance'] - int(message.text))
    save_file('data/users.json', user_data)
    
    await message.reply("Баланс обновлен.")
    await state.clear()

async def ban_user_action(message: types.Message, state: FSMContext):
    user_data = read_file('data/users.json')
    user_data[str(message.from_user.id)]['ban'] = True
    save_file('data/users.json', user_data)
    await message.reply("Пользователь забанен.")
    await state.clear()
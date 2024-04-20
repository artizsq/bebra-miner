from aiogram.filters import BaseFilter
from aiogram import types
from utils.parsing import Data



class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message):
        data = Data()
        if str(message.from_user.id) in data.admin_ids:
            return True
        return False
    

class CheckUser(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        if callback.from_user.id == callback.message.reply_to_message.from_user.id:
            return True
        await callback.answer("❌ Не стоит нажимать на чужие кнопки!", show_alert=True)
        return False
    

class CheckIvent(BaseFilter):

    async def __call__(self, message: types.Message):
        data = Data()
        if data.isEvent == True:
            print(type(data.isEvent))
            print(data.isEvent)
            return True
        print(type(data.isEvent))
        print(data.isEvent)
        await message.answer("❌ В данный момент Ивент не активен")
        return False
    

class IventShopChecker(BaseFilter):
    async def __call__(self, message: types.CallbackQuery):
        data = Data()
        if data.isEvent == True:
            return True
        await message.answer("❌ В данный момент Ивент не активен")
        return False
        
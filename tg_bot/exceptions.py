from typing import Any
from aiogram.filters import BaseFilter
from aiogram import types
from utils.parsing import Data
from utils.data import read_file, save_file, add_thousands_separator
from aiogram.fsm.context import FSMContext



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
        miner = message.data.split("_")[2]
        if data.isEvent == True and miner in read_file(f'data/{data.event_name}/shop.json'):
            return True
        await message.answer("❌ В данный момент Ивент не активен")
        return False
    
class CheckCurrentShopMiner(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        data = Data()
        shop = read_file('data/shop/miners.json')
        miner = callback.data.split("_")[1]
        if miner not in shop:
            await callback.answer("❌ Такого майнера нет в магазине!\nОбновите магазин!", show_alert=True)
            return False
        return True
    

class CheckMinerCount(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        shop = read_file('data/shop/miners.json')
        miner = callback.data.split("_")[2]
        if miner not in shop:
            await callback.answer("❌ Такого майнера нет в магазине!\nОбновите магазин!", show_alert=True)
            return False
        return True
    
class CheckEventMinerCount(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        data = Data()
        shop = read_file(f'data/{data.event_name}/shop.json')
        miner = callback.data.split("_")[2]
        if miner not in shop:
            await callback.answer("❌ Такого майнера нет в магазине!\nОбновите магазин!", show_alert=True)
            return False
        return True
    
class CheckCurrentShopPrefix(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery):
        data = Data()
        shop = read_file('data/shop/prefixes.json')
        miner = callback.data.split('_')[1]
        if miner not in shop:
            await callback.answer("❌ Такого префикса нет в магазине!\nОбновите магазин!", show_alert=True)
            return False
        return True
    


    

class CheckPromocode(BaseFilter):
    async def __call__(self, message: types.Message, state: FSMContext):
        promocode = message.text
        data = read_file('data/users.json')
        
        promo_data = read_file('data/promo.json')
        if promocode in promo_data:
            if promo_data[promocode]['type'] == 'b-cash':
                if promo_data[promocode]['count'] > 0 and str(message.from_user.id) not in promo_data[promocode]['activations']:
                    promo_data[promocode]['count'] -= 1
                    data[str(message.from_user.id)]['Rbalance'] += promo_data[promocode]['reward']
                    promo_data[promocode]['activations'].append(str(message.from_user.id))
                    save_file('data/promo.json', promo_data)
                    save_file('data/users.json', data)
                    await message.answer(f"<b>✅ Промокод успешно применен!\n<i>+{add_thousands_separator(promo_data[promocode]['reward'])} {promo_data[promocode]['type']}</i></b>", parse_mode='HTML')
                    return True
                await message.answer("❌ Промокод недействителен!")
                await state.clear()
                return False
            
            elif promo_data[promocode]['type'] == 'miner':

                if promo_data[promocode]['count'] > 0 and str(message.from_user.id) not in promo_data[promocode]['activations']:
                    promo_data[promocode]['count'] -= 1
                    data[str(message.from_user.id)]['miners'][promo_data[promocode]['name']] = {
                        'pow': promo_data[promocode]['pow'],
                        'count': 1,
                        'event': ''
                    }
                    promo_data[promocode]['activations'].append(str(message.from_user.id))
                    save_file('data/promo.json', promo_data)
                    save_file('data/users.json', data)
                    await message.answer(f"<b>✅ Промокод успешно применен!\n<i>Новый майнер уже доступен у вас в инветаре!</i></b>", parse_mode='HTML')
                    await state.clear()
                    return True
                await message.answer("❌ Промокод недействителен!")
                await state.clear()
                return False
        else:
            await message.answer("❌ Такого промокода не найдено!")
            await state.clear()
            return False

        
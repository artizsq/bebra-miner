from aiogram import Bot, Dispatcher, F, filters, types
import asyncio
from utils.parsing import Data
from tg_bot.exceptions import IsAdmin, CheckUser
from tg_bot.commands import (start_command, 
                             profile_command, 
                             delete_panel, 
                             farm_command,
                             shop_command,
                             trade_command,
                             help_command)

from tg_bot.handlers import (check_miner_info, 
                             buy_miner, 
                             trade_button, 
                             cancel_button, 
                             trade_coins, 
                             Trade)

from tg_bot.admin_commands import (admin_panel,
                                    update_shop_admin,
                                    send_BD)
import logging
from tg_bot.middlewares import SchedulerMiddleware
from tg_bot.events import update_current_shop, update_rate
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(level=logging.INFO)




async def main():
    data = Data()
    bot = Bot(token=data.TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(update_current_shop, trigger='cron', hour=21, minute=0, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(update_rate, trigger='interval', hours=1, start_date=datetime.now(), kwargs={'bot': bot})

    
    # dp.message.register(i_dont_know, filters.Command('help'))
    # Обработчик команды /start
    dp.message.register(start_command, filters.Command("start"))

    # Обработчик команды /profile и кнопки "👤 Профиль"
    dp.message.register(profile_command, filters.Command("profile"))
    dp.message.register(profile_command, F.text == "👤 Профиль")

    # Обработчик команды /farm и кнопки "📈 Ферма"
    dp.message.register(farm_command, F.text == "📈 Ферма")
    dp.message.register(farm_command, filters.Command("farm"))

    # Обработчик команды /shop и кнопки "🛒 Магазин"
    dp.message.register(shop_command, F.text == "🛒 Магазин")
    dp.message.register(shop_command, filters.Command("shop"))

    # Обработчик команды /trade и кнопки "🔁 Обменник"
    dp.message.register(trade_command, F.text == "🔁 Обменник")
    dp.message.register(trade_command, filters.Command("trade"))

    # Обработчик команды /help и кнопки "🆘 Помощь"
    dp.message.register(help_command, F.text == "🆘 Помощь")
    dp.message.register(help_command, filters.Command("help"))

    # Обработчик команды /event
    # dp.message.register(help_command, filters.Command("event"))


    dp.message.register(trade_coins, Trade.coins)





    # Обработчик нажатия на кнопку магазина (выбран предмет покупки)
    dp.callback_query.register(check_miner_info, F.data.startswith('_'), CheckUser())

    # Обработчик нажатия на кнопку "Купить"
    dp.callback_query.register(buy_miner, F.data.startswith('b'), CheckUser())

    # Обработчик нажатия на кнопку "Обменять"
    dp.callback_query.register(trade_button, F.data == "p2p", CheckUser())

    dp.callback_query.register(cancel_button, F.data == "cancel", CheckUser())



    # ---------------------------------- #
    dp.message.register(delete_panel, filters.Command("delete_panel"), IsAdmin())
    dp.message.register(admin_panel, filters.Command("panel"), IsAdmin())

    dp.callback_query.register(send_BD, F.data == "upload", IsAdmin())
    dp.callback_query.register(update_shop_admin, F.data == "update_shop", IsAdmin())

    

    
    


    # Мидлвары (промежуточные обработчики)
    dp.update.middleware(SchedulerMiddleware(scheduler))






    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
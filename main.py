from aiogram import Bot, Dispatcher, F, filters, types
import asyncio
from utils.parsing import Data
from tg_bot.exceptions import IsAdmin, CheckUser, CheckIvent, IventShopChecker
from tg_bot.commands import (start_command, 
                             profile_command, 
                             delete_panel, 
                             farm_command,
                             shop_command,
                             trade_command,
                             help_command,
                             ivent_command)

from tg_bot.handlers import (check_miner_info, 
                             buy_miner, 
                             trade_button, 
                             cancel_button, 
                             trade_coins, 
                             Trade,
                             all_user_miners,
                             all_user_prefixes,
                             change_prefix,
                             miner_info,
                             go_back, buy_event_miner)

from tg_bot.admin_commands import (admin_panel,
                                    update_shop_admin,
                                    send_BD, Admin, 
                                    add_or_sub_balance, add_balance, 
                                    sub_balance, ban_user, ban_user_action, 
                                    actions_with_balance, update_rate_button)
import logging
from tg_bot.middlewares import SchedulerMiddleware
from tg_bot.events import update_current_shop, update_rate, update_event
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(level=logging.INFO)




async def main():
    data = Data()
    bot = Bot(token=data.TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(update_current_shop, trigger='cron', hour=21, minute=0, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(update_rate, trigger='interval', minutes=15, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(update_event, trigger='interval', hours=12, start_date=datetime.now(), kwargs={'bot': bot})

    
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
    dp.message.register(ivent_command, F.text == "⌛️ Ивент", CheckIvent())
    dp.message.register(ivent_command, filters.Command("event"), CheckIvent())


    dp.message.register(trade_coins, Trade.coins)





    # Обработчик нажатия на кнопку магазина (выбран предмет покупки)
    dp.callback_query.register(check_miner_info, F.data.startswith('_'), CheckUser())

    # Обработчик нажатия на кнопку "Купить майнер" при ивенте
    dp.callback_query.register(buy_event_miner, F.data.startswith('ev_'), CheckUser(), IventShopChecker())

    # Обработчик нажатия на кнопку "Купить"
    dp.callback_query.register(buy_miner, F.data.startswith('b_'), CheckUser())

    # Обработчик нажатия на кнопку "Обменять"
    dp.callback_query.register(trade_button, F.data == "p2p", CheckUser())

    # Кнопка отмены
    dp.callback_query.register(cancel_button, F.data == "cancel", CheckUser())

    # Обработчик нажатия на кнопку "мои майнеры"
    dp.callback_query.register(all_user_miners, F.data == "all_miners", CheckUser())

    # Обработчик нажатия на кнопку "мои префиксы"
    dp.callback_query.register(all_user_prefixes, F.data == "all_prefixes", CheckUser())

    # Обработчик нажатия на кнопку "изменить префикс"
    dp.callback_query.register(change_prefix, F.data.startswith('PR_'), CheckUser())

    # Обработчик нажатия на кнопку "информация о майнере"
    dp.callback_query.register(miner_info, F.data.startswith('MI_'), CheckUser())

    # Кнопка Назад
    dp.callback_query.register(go_back, F.data.startswith('back_'), CheckUser())


    # ---------------------------------- #
    dp.message.register(delete_panel, filters.Command("delete_panel"), IsAdmin())
    dp.message.register(admin_panel, filters.Command("panel"), IsAdmin())

    dp.callback_query.register(send_BD, F.data == "upload", IsAdmin())
    dp.callback_query.register(add_balance, F.data == "add_balance", IsAdmin())
    dp.callback_query.register(sub_balance, F.data == "sub_balance", IsAdmin())
    dp.callback_query.register(ban_user, F.data == "ban", IsAdmin())
    dp.message.register(actions_with_balance, Admin.user_id, IsAdmin())
    dp.message.register(add_or_sub_balance, Admin.balance, IsAdmin())
    dp.message.register(ban_user_action, Admin.user_id, IsAdmin())
    dp.callback_query.register(update_shop_admin, F.data == "update_shop", IsAdmin())
    dp.callback_query.register(update_rate_button, F.data == "rate", IsAdmin())


    

    
    


    # Мидлвары (промежуточные обработчики)
    dp.update.middleware(SchedulerMiddleware(scheduler))






    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
from aiogram import Bot, Dispatcher, F, filters, types
import asyncio
from utils.parsing import Data
from tg_bot.exceptions import IsAdmin, CheckUser, CheckIvent, IventShopChecker, CheckCurrentShopMiner, CheckCurrentShopPrefix
from tg_bot.commands import (start_command, 
                             delete_panel, 
                             farm_command,
                             shop_command,
                             trade_command,
                             help_command,
                             ivent_command)

from tg_bot.base_hdlrs import cancel_button
from tg_bot.handlers.trader import Trade, Trader

from tg_bot.admin.admin_commands import (admin_panel,
                                    update_shop_admin,
                                    send_BD, Admin, 
                                    add_or_sub_balance, add_balance, 
                                    sub_balance, ban_user, ban_user_action, 
                                    actions_with_balance, update_rate_button)


from tg_bot.handlers.profile import Profile
from tg_bot.handlers.shop import ShopMiner, ShopPrefix
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
    scheduler.add_job(update_rate, trigger='interval', minutes=30, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(update_event, trigger='cron', hour=12, minute=0, start_date=datetime.now(), kwargs={'bot': bot})


    
    # Обработчик команды /start
    dp.message.register(start_command, filters.Command("start"))

    # Обработчик команды /profile и кнопки "👤 Профиль"
    dp.message.register(Profile.profile_command, filters.Command("profile"))
    dp.message.register(Profile.profile_command, F.text == "👤 Профиль")

    # Обработчик команды /farm и кнопки "📈 Ферма"
    dp.message.register(farm_command, F.text == "📈 Ферма")
    dp.message.register(farm_command, filters.Command("farm"))

    # Обработчик команды /shop и кнопки "🛒 Магазин"
    dp.message.register(shop_command, F.text == "🛒 Магазин")
    dp.message.register(shop_command, filters.Command("shop"))

    # Обработчик команды /trade и кнопки "🔁 Обменник"
    dp.message.register(trade_command, F.text == "🔁 Обменник")
    dp.message.register(trade_command, filters.Command("trade"))

    # Обработчик команды /event
    dp.message.register(ivent_command, F.text == "⌛️ Ивент", CheckIvent())
    dp.message.register(ivent_command, filters.Command("event"), CheckIvent())


    dp.message.register(Trader.trade_coins, Trade.coins)





    # Обработчик нажатия на кнопку магазина (выбран предмет покупки)
    dp.callback_query.register(ShopMiner.check_miner_info, F.data.startswith('_'), CheckUser(), CheckCurrentShopMiner())

    # Обработчик нажатия на кнопку магазина (инвентовый)
    dp.callback_query.register(ShopMiner.check_miner_info_event, F.data.startswith('event_'), CheckUser(), IventShopChecker())

    # Обработчик нажатия на кнопку "Купить майнер" при ивенте
    dp.callback_query.register(ShopMiner.buy_event_miner, F.data.startswith('ev_'), CheckUser(), IventShopChecker())

    # Обработчик нажатия на кнопку "Купить"
    dp.callback_query.register(ShopMiner.buy_miner, F.data.startswith('b_'), CheckUser())

    dp.callback_query.register(ShopMiner.all_shop_miners, F.data.startswith('shop_miners'), CheckUser())

    # Обработчик нажатия на кнопку "Обменять"
    dp.callback_query.register(Trader.trade_button, F.data == "p2p", CheckUser())

    # Кнопка отмены
    dp.callback_query.register(cancel_button, F.data == "cancel", CheckUser())

    # Обработчик нажатия на кнопку "мои майнеры"
    dp.callback_query.register(Profile.all_user_miners, (F.data == "all_miners") | (F.data == 'back_m'), CheckUser())

    # Обработчик нажатия на кнопку "мои префиксы"
    dp.callback_query.register(Profile.all_user_prefixes, (F.data == "all_prefixes") | (F.data == 'back_pr'), CheckUser())

    # Обработчик нажатия на кнопку "изменить префикс"
    dp.callback_query.register(Profile.change_prefix, F.data.startswith('PR_'), CheckUser())

    # Обработчик нажатия на кнопку "информация о майнере"
    dp.callback_query.register(Profile.miner_info, F.data.startswith('MI_'), CheckUser())

    # Обработчик нажатия назад
    dp.callback_query.register(Profile.profile_command_inline, F.data == 'back_profile', CheckUser())

    # Обработчик нажатия на кнопку "магазин префиксов"
    dp.callback_query.register(ShopPrefix.all_shop_prefixes, F.data == "shop_prefix", CheckUser())

    # Обработчик нажатия на кнопку "префиксы"
    dp.callback_query.register(ShopPrefix.check_prefix_info, F.data.startswith('p_'), CheckUser(), CheckCurrentShopPrefix())

    # Обработчик нажатия на кнопку "купить префикс"
    dp.callback_query.register(ShopPrefix.buy_prefix, F.data.startswith('pre_'), CheckUser(), CheckCurrentShopPrefix())

    # Обработка магазина с префиксами

    # Кнопка Назад



    # dp.callback_query.register(plus_button, F.data.startswith("pl"), CheckUser())


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
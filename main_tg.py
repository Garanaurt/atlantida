import asyncio
from aiogram import Bot, Dispatcher
from tg_bot import handlers
from db_interface import DbSpamer
import os


#Токен бота
TOKEN = '6275915048:AAFjJo5swSwJBTMdCpy1oHG-crySYilSd5M'



if not os.path.exists('database.db'):
    with DbSpamer() as db:
        db.db_check_and_create_tables()



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)

    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
    ]

    await asyncio.gather(*tasks)



if __name__ == "__main__":
    asyncio.run(main())
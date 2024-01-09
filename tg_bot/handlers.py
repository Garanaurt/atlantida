from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from db_interface import DbSpamer
import re
import uuid
from datetime import datetime, timedelta



router = Router()



class AddUserState(StatesGroup):
    USER = State()


def kb_get_main_menu():
    keys = [
        [types.InlineKeyboardButton(text='Добавить нового юзера', callback_data='add_user')],
        [types.InlineKeyboardButton(text='Активные юзеры', callback_data="active_users")],
    ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_add_user():
    keys = [
        [types.InlineKeyboardButton(text='Подписка на 3 дня', callback_data='add_user_3')],
        [types.InlineKeyboardButton(text='Подписка на 30 дней', callback_data="add_user_30")],
        [types.InlineKeyboardButton(text='Отмена', callback_data="cancel_adding")],
    ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_go_to_main():
    keys = [
        [types.InlineKeyboardButton(text='На главную', callback_data="cancel_adding")],
    ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



async def delete_chat_mess(bot: Bot, chat):
    with DbSpamer() as db:
        messages = db.db_get_messages_in_chat_admin(chat)
    for msg in messages:
        chat_mess = int(msg[1])
        try:
            await bot.delete_message(chat_id=msg[0], message_id=chat_mess)
        except Exception:
            continue     
    with DbSpamer() as db:       
        db.db_delete_message_in_chat_admin(chat)



async def save_message(message: types.Message):
    chat_id = message.chat.id
    message_id = message.message_id
    with DbSpamer() as db:
        db.db_add_message_in_messages_admin(chat_id, message_id)




@router.callback_query(lambda c: c.data == "cancel_adding")
async def cancel_adding(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    username = call.from_user.username
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    text = f'Привет, {username}\n'
    me = await bot.send_message(chat_id, text, reply_markup=kb_get_main_menu())
    await save_message(me)
    
#Старт
@router.message(Command('start'))
async def cmd_start(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    if chat_id > 0:
        await cmd_star(message, bot)


@router.callback_query(F.data == "star")
async def cmd_star(call: types.CallbackQuery, bot: Bot):
    username = call.from_user.username
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    text = f'Привет, {username}\n'
    me = await bot.send_message(chat_id, text, reply_markup=kb_get_main_menu())
    await save_message(me)


@router.callback_query(lambda c: c.data == "add_user")
async def add_product(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(AddUserState.USER)
    me = await call.message.answer(f"На какое время подписка, нажми кнопку или пришли количество дней", reply_markup=kb_add_user(), parse_mode='HTML')
    await save_message(me)


@router.message(AddUserState.USER, F.text)
async def processing_add_user_msg(message: types.Message, state: FSMContext):
    input_text = message.text
    try:
        days = int(input_text)
    except ValueError:
        me = await message.answer(f"Пришли количество дней цифрой", reply_markup=kb_add_user(), parse_mode='HTML')
        await save_message(me)
        return

    activation_code = uuid.uuid4()
    current_date = datetime.now()
    end_date = (current_date + timedelta(days=days)).date()
    print(activation_code, end_date, sep='\n')
    with DbSpamer() as db:
        db.add_user(activation_code, end_date)
    await state.clear()
    msg = "Новый юзер добавлен в базу\n"
    msg += f"Добавлен - {current_date.date()}\n"
    msg += f"Подписка закончится - {end_date}\n"
    msg += f"<b>Код активации</b> - <code>{activation_code}</code>"
    await message.answer(msg, reply_markup=kb_go_to_main(), parse_mode='HTML')


@router.callback_query(lambda c: re.match(r'^add_user_\d+$', c.data))
async def processing_add_user_btn(call: types.CallbackQuery):
    days = int(call.data.split('_')[2])
    activation_code = uuid.uuid4()
    current_date = datetime.now()
    end_date = (current_date + timedelta(days=days)).date()
    print(activation_code, end_date, sep='\n')
    with DbSpamer() as db:
        db.add_user(activation_code, end_date)
    msg = "Новый юзер добавлен в базу\n"
    msg += f"Добавлен - {current_date.date()}\n"
    msg += f"Подписка закончится - {end_date}\n"
    msg += f"<b>Код активации</b> - <code>{activation_code}</code>"
    await call.message.answer(msg, reply_markup=kb_go_to_main(), parse_mode='HTML')


@router.callback_query(lambda c: c.data == "active_users")
async def active_users(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    msg = ''
    with DbSpamer() as db:
        all_users = db.get_all_users()
    if not all_users:
        msg = 'Пусто'
    for user in all_users:
        string = f"id-{user[0]}\ncode-<code>{user[1]}</code>\nadd-{user[2]}\nend-{user[3]}\nhwid-{user[4]}\n\n"
        msg += string
    me = await call.message.answer(msg, reply_markup=kb_go_to_main(), parse_mode='HTML')
    await save_message(me)

    

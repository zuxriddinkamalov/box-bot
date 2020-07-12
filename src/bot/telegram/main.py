# debug import
import logging
# import requests


# aiogram import
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile, InputMedia
from aiogram.types import ReplyKeyboardRemove

# bot import
import client as ClientModule
from messages import Messages
import keyboards
import states

# system import
import os
import aioredis

# init settings
logging.basicConfig(
    format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG
    )

Client = ClientModule.Client()

token_info = Client.get_telegram_token()
bot = Bot(token=token_info['token'], parse_mode=types.ParseMode.HTML)
print(f'\n\nBot started. [{token_info["title"]}] {token_info["token"]}\n\n')
storage = RedisStorage2(db=1)
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())


# /start command handler
@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)

    if not Client.user_exists(user):

        modelUser = Client.user_create(message.from_user)
    else:

        modelUser = Client.get_user(user)

    await state.set_data({})

    if not modelUser.language_set:

        await states.User.ChooseLanguage.set()
        await bot.send_chat_action(user, action='typing')

        text = Messages(user)['start_message'].replace('{}', message.from_user.first_name)
        markup = None
        await bot.send_message(user, text, reply_markup=markup)

        text = Messages(user)['ask_for_language']
        markup = keyboards.LanguageKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    else:

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)


# /state command handler
@dp.message_handler(commands=['state'], state='*')
async def get_MyState(message: types.Message):

    user = message.from_user.id

    state = await dp.current_state(user=message.from_user.id).get_state()

    await bot.send_message(user, state)


@dp.message_handler(state=states.User.ChooseLanguage)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text

    try:

        language = ClientModule.core_models.Language.objects.get(text=recieved_text).title

        Client.set_language(user, language)

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    except Exception as e:
        print(e)

    return


@dp.message_handler(state=states.User.MainMenu)
async def user_ammount_handler(message: types.Message, state: FSMContext):
    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 1).get(
            title=recieved_text
            ).button_code
    except Exception as e:
        return

    if button_code == 'catalog':
        # "Catalog button handler"

        text = Messages(user)['category']
        await states.User.Category.set()

        markup = keyboards.CategoryKeyboard(user, 1)
        await bot.send_message(user, text, reply_markup=markup)


@dp.callback_query_handler(state=states.User.Category)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if "back" in data:

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if "prev" in data:

        page = int(data.replace('prev ', ''))

        markup = keyboards.CategoryKeyboard(user, page)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "next" in data:

        page = int(data.replace('next ', ''))

        markup = keyboards.CategoryKeyboard(user, page)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)


async def shutdown(dispatcher: Dispatcher):

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

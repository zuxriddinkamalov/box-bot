# debug import
import logging
# import requests

import asyncio

from aiogram.types.message import ContentTypes
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
from messages import Messages, GenerateCart, GenerateOrder
import keyboards
import states

# system import
import os
from datetime import datetime
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
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        await bot.send_message(user, text, reply_markup=markup)


# /state command handler
@dp.message_handler(commands=['state'], state='*')
async def get_MyState(message: types.Message, state: FSMContext):

    user = message.from_user.id

    current = await dp.current_state(user=message.from_user.id).get_state()
    
    async with state.proxy() as data:

        await bot.send_message(user, f'{current}\n{data}')


@dp.message_handler(state=states.User.ChooseLanguage)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text

    try:

        language = ClientModule.core_models.Language.objects.get(text=recieved_text).title

        Client.set_language(user, language)

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
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

        cart_title = None

    except Exception as e:

        button_code = None
        cart_title = Client.get_buttons(language, 1).get(
            button_code='cart'
            ).title.split(' [')[0]

    if button_code == 'catalog':
        # "Catalog button handler"

        text = Messages(user)['category']
        await states.User.Category.set()

        markup = keyboards.CategoryKeyboard(user, 1)
        await bot.send_message(user, text, reply_markup=markup)

    is_cart_str = recieved_text.split(' ')[0]
    if is_cart_str == cart_title:
        # "Cart button handler"

        data = GenerateCart(user)
        text = data[0]

        if data[1]:

            await states.User.Cart.set()

            markup = keyboards.CartKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

        else:

            markup = None
            await bot.send_message(user, text, reply_markup=markup)

            await states.User.MainMenu.set()

            text = Messages(user)['main_menu']
            markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
            await bot.send_message(user, text, reply_markup=markup)
            
    if button_code == 'news':
        
        await states.User.NewsShow.set()
        
        news = Client.get_all_news(user)
        if news.count() != 0:

            currentAnnouncement = news.first()
            text = currentAnnouncement.text
            photo = Client.get_photo(currentAnnouncement)
            
            Client.tick_view(currentAnnouncement)

            markup = keyboards.PaginationKeyboard(user, 1, len(news))
            msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)
            if not photo[1]:
                Client.update_photo(photo[2], msg.photo[-1].file_id)

        else:

            text = Messages(user)['noNews']
            markup = None
            await bot.send_message(user, text, reply_markup=markup)

            await states.User.MainMenu.set()

            text = Messages(user)['main_menu']
            markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
            
            await bot.send_message(user, text, reply_markup=markup)

            
@dp.callback_query_handler(state=states.User.NewsShow)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = callback_query.from_user.id
    data = callback_query.data
    
    if "empty" in data:
        await bot.answer_callback_query(callback_query.id)

        return

    if "next" in data:

        await bot.answer_callback_query(callback_query.id)
        next = int(data.replace("next ", ""))

        news = Client.get_all_news(user)
        currentAnnouncement = news[next-1]
        text = currentAnnouncement.text
        photo = Client.get_photo(currentAnnouncement)

        Client.tick_view(currentAnnouncement)

        markup = keyboards.PaginationKeyboard(user, next, len(news))
        await bot.delete_message(user, callback_query.message.message_id)
        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)
        # await bot.edit_message_media(InputMediaPhoto())
        if not photo[1]:
            Client.update_photo(photo[2], msg.photo[-1].file_id)

    if "prev" in data:

        await bot.answer_callback_query(callback_query.id)
        prev = int(data.replace("prev ", ""))

        news = Client.get_all_news(user)
        currentAnnouncement = news[prev-1]
        text = currentAnnouncement.text
        photo = Client.get_photo(currentAnnouncement)

        Client.tick_view(currentAnnouncement)

        markup = keyboards.PaginationKeyboard(user, prev, len(news))
        await bot.delete_message(user, callback_query.message.message_id)
        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)
        # await bot.edit_message_media(InputMediaPhoto())
        if not photo[1]:
            Client.update_photo(photo[2], msg.photo[-1].file_id)

    if "back" in data:

        await bot.answer_callback_query(callback_query.id)

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        
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
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        await bot.send_message(user, text, reply_markup=markup)

    if "prev" in data:

        page = int(data.replace('prev ', ''))

        markup = keyboards.CategoryKeyboard(user, page)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "next" in data:

        page = int(data.replace('next ', ''))

        markup = keyboards.CategoryKeyboard(user, page)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "category" in data:
        # "Product choose handler"

        await bot.delete_message(user, callback_query.message.message_id)

        category = int(data.replace('category ', ''))

        await states.User.Product.set()

        current_category = Client.get_category(category)
        text = current_category.description
        photo = Client.get_photo(current_category)
        # markup = None
        markup = keyboards.ProductKeyboard(user, 1, category)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id
            data['category'] = category

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)

        # text = Messages(user)['product']
        # markup = keyboards.ProductKeyboard(user, 1)

        # await bot.send_message(user, text, reply_markup=markup)


@dp.callback_query_handler(state=states.User.Product)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if "back" in data:

        await bot.delete_message(user, callback_query.message.message_id)

        text = Messages(user)['category']
        await states.User.Category.set()

        markup = keyboards.CategoryKeyboard(user, 1)
        await bot.send_message(user, text, reply_markup=markup)

    if "prev" in data:

        async with state.proxy() as data:

            category = data['category']

        page = int(data.replace('prev ', ''))

        markup = keyboards.ProductKeyboard(user, page, category)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "next" in data:

        async with state.proxy() as data:

            category = data['category']

        page = int(data.replace('next ', ''))

        markup = keyboards.ProductKeyboard(user, page, category)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "product" in data:
        # "Product choose handler"

        await bot.delete_message(user, callback_query.message.message_id)

        product = int(data.replace('product ', ''))

        await states.User.ProductMenu.set()

        current_product = Client.get_product(product)
        text = current_product.description
        photo = Client.get_photo(current_product)
        # markup = None
        markup = keyboards.ProductDetailsKeyboard(user)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id
            data['product'] = product

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)  


@dp.callback_query_handler(state=states.User.ProductMenu)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if "back" in data:

        async with state.proxy() as data:

            category = data['category']

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.Product.set()

        current_category = Client.get_category(category)
        text = current_category.description
        photo = Client.get_photo(current_category)
        # markup = None
        markup = keyboards.ProductKeyboard(user, 1, category)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)

        # text = Messages(user)['product']
        # markup = keyboards.ProductKeyboard(user, 1)

        # await bot.send_message(user, text, reply_markup=markup)

    if "add" in data:

        await states.User.Quantity.set()

        async with state.proxy() as data:

            data['quantity'] = 1

        text = Messages(user)['quantity']
        markup = keyboards.QuantityKeyboard(user, 1)
        await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.Quantity)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "back" in data:

        async with state.proxy() as data:

            product = data['product']

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.ProductMenu.set()

        current_product = Client.get_product(product)
        text = current_product.description
        photo = Client.get_photo(current_product)
        # markup = None
        markup = keyboards.ProductDetailsKeyboard(user)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)

    if "minus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
        quantity -= 1

        if quantity == 0:
            await bot.answer_callback_query(callback_query.id)
            return


        async with state.proxy() as data:
            data['quantity'] = quantity

        await states.User.Quantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.QuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "plus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
            quantity += 1
            data['quantity'] = quantity

        await states.User.Quantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.QuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "accept" in data:

        # "Catalog button handler"
        async with state.proxy() as data:

            quantity = int(data['quantity'])
            product = int(data['product'])

        Client.add_to_cart(user, product, quantity)

        await bot.delete_message(user, callback_query.message.message_id)

        text = Messages(user)['cart_added']
        await bot.answer_callback_query(callback_query.id, text)

        text = Messages(user)['category']
        await states.User.Category.set()

        markup = keyboards.CategoryKeyboard(user, 1)
        await bot.send_message(user, text, reply_markup=markup)

    await bot.answer_callback_query(callback_query.id)

    return


@dp.message_handler(state=states.User.Cart)
async def user_ammount_handler(message: types.Message, state: FSMContext):
    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 5).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        await states.User.MainMenu.set()

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        await bot.send_message(user, text, reply_markup=markup)

    if 'edit' in button_code:

        await states.User.Edit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if 'clear' in button_code:

        await states.User.MainMenu.set()

        Client.cancel_cart(user)

        counter = 5

        text = Messages(user)['cart_cleared']
        start_time = datetime.now()
        markup = keyboards.CancelButton(user, counter)
        msg = await bot.send_message(user, text, reply_markup=markup)

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        await bot.send_message(user, text, reply_markup=markup)

        while True:

            if counter != 0:
                await asyncio.sleep(1)

                counter -= 1

                markup = keyboards.CancelButton(user, counter)
                try:
                    await bot.edit_message_reply_markup(user, msg.message_id, reply_markup=markup)
                except Exception as e:
                    break

            else:

                markup = None
                await bot.edit_message_reply_markup(user, msg.message_id, reply_markup=markup)
                Client.clear_cart(user)
                break

    if 'order' in button_code:

        if Client.is_verified(user):

            if Client.has_real_name(user):

                text = Messages(user)['delivery']
                await states.User.Delivery.set()

                markup = keyboards.DeliveryKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)

            else:

                await states.User.RealName.set()

                text = Messages(user)['real_name_get']

                markup = None
                await bot.send_message(user, text, reply_markup=markup)
        else:

            await states.User.Phone.set()

            text = Messages(user)['add_phone']
            markup = keyboards.ContactKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)


@dp.message_handler(state=states.User.RealName)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id
    recieved_text = message.text

    Client.set_real_name(user, recieved_text)

    text = Messages(user)['delivery']
    await states.User.Delivery.set()

    markup = keyboards.DeliveryKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)

    return


@dp.message_handler(state=states.User.Phone, content_types=types.ContentType.CONTACT)
async def user_contact_handler(message: types.Message, state: FSMContext):
    user = message.from_user.id
    phone = message.contact.phone_number

    Client.set_phone(user, phone)

    if Client.has_real_name(user):

        text = Messages(user)['delivery']
        await states.User.Delivery.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    else:

        text = Messages(user)['phone_set']

        markup = None
        await bot.send_message(user, text, reply_markup=markup)
        
        await states.User.RealName.set()

        text = Messages(user)['real_name_get']

        markup = None
        await bot.send_message(user, text, reply_markup=markup)

    return


@dp.message_handler(state=states.User.Phone)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 8).get(
            title=recieved_text
            ).button_code

    except Exception as e:

        pass

    if "back" in button_code:

        data = GenerateCart(user)
        text = data[0]

        await states.User.Cart.set()

        markup = keyboards.CartKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return

    if str(recieved_text).isdigit():
        if len(recieved_text) == 9:
            recieved_text = f"998{recieved_text}"

        if len(recieved_text) == 12:

            Client.set_phone(user, phone)

            if Client.has_real_name(user):

                text = Messages(user)['delivery']
                await states.User.Delivery.set()

                markup = keyboards.DeliveryKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)

            else:

                text = Messages(user)['phone_set']

                markup = None
                await bot.send_message(user, text, reply_markup=markup)
                
                await states.User.RealName.set()

                text = Messages(user)['real_name_get']

                markup = None
                await bot.send_message(user, text, reply_markup=markup)

        else:

            text = Messages(user)['phone_length']
            markup = None
            await bot.send_message(user, text, reply_markup=markup)
    else:

        text = Messages(user)['phone_only_digits']
        markup = None
        await bot.send_message(user, text, reply_markup=markup)

    return


@dp.callback_query_handler(state=states.User.Edit)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "back" in data:

        await bot.delete_message(user, callback_query.message.message_id)

        data = GenerateCart(user)
        text = data[0]

        await states.User.Cart.set()

        markup = keyboards.CartKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if 'position' in data:

        await bot.delete_message(user, callback_query.message.message_id)

        position = int(data.replace('position ', ''))
        position = ClientModule.core_models.Position.objects.get(pk=position)

        await states.User.EditQuantity.set()

        async with state.proxy() as data:
            data['quantity'] = position.count
            data['position'] = position.id

        current_product = position.product
        photo = Client.get_photo(current_product)
        # markup = None
        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, position.count)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)

        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.MainMenu)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "cancel" in data:

        await bot.delete_message(user, callback_query.message.message_id)
        await bot.delete_message(user, callback_query.message.message_id + 1)

        Client.revoke_cart(user)

        text = Messages(user)['cart_restored']

        markup = None
        await bot.send_message(user, text, reply_markup=markup)

        text = Messages(user)['main_menu']
        markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
        await bot.send_message(user, text, reply_markup=markup)
        
    if "accept_order_channel" in data:
        manager_chat_id = user
        order_num = int(data.replace('accept_order_channel ', ''))

        order = Client.get_order(order_num)
        if order.selected_branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

            order.manager = Client.get_user(manager_chat_id)
            order.status = ClientModule.core_models.OrderStatus.objects.get(pk=2)
            order.save()
            
            user = order.user.chat_id

            text = Messages(user)['in_porgress_cooking']
            markup = None
            await bot.send_message(user, text, reply_markup=markup)
            
            if order.delivery:
                markup = keyboards.DeliveryStatusKeyboard(order.id)
            else:
                markup = keyboards.SelfStatusKeyboard(order.id)
                
            await bot.edit_message_reply_markup(order.selected_branch.channel,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=markup)
        else:
            
            await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
        return
    
    if 'to_delivery' in data:
        manager_chat_id = user
        order_num = int(data.replace('to_delivery ', ''))

        order = Client.get_order(order_num)
        if order.selected_branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

            order.status = ClientModule.core_models.OrderStatus.objects.get(pk=3)
            order.save()
            
            user = order.user.chat_id

            text = Messages(user)['in_porgress_to_delivery']
            markup = None
            await bot.send_message(user, text, reply_markup=markup)
            await bot.answer_callback_query(callback_query.id, text='Заказ передан на доставку')
            
            markup = keyboards.EndStatusKeyboard(order.id)
            await bot.edit_message_reply_markup(order.selected_branch.channel,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=markup)
        else:
            
            await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
        return    
    
    if 'to_self' in data:
        manager_chat_id = user
        order_num = int(data.replace('to_self ', ''))

        order = Client.get_order(order_num)
        if order.selected_branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

            order.status = ClientModule.core_models.OrderStatus.objects.get(pk=3)
            order.save()
            
            user = order.user.chat_id

            text = Messages(user)['in_porgress_to_self']
            markup = None
            await bot.send_message(user, text, reply_markup=markup)
            await bot.answer_callback_query(callback_query.id, text='Заказ передан на самовывоз')
            
            
            markup = keyboards.EndStatusKeyboard(order.id)
            await bot.edit_message_reply_markup(order.selected_branch.channel,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=markup)
        else:
            
            await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
        return 
    
    if 'to_end' in data:
        manager_chat_id = user
        order_num = int(data.replace('to_end ', ''))

        order = Client.get_order(order_num)
        if order.selected_branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

            order.status = ClientModule.core_models.OrderStatus.objects.get(pk=4)
            order.active = False
            order.save()
            
            user = order.user.chat_id

            await bot.answer_callback_query(callback_query.id, text='Заказ завершен')

            
            markup = None
            await bot.edit_message_reply_markup(order.selected_branch.channel,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=markup)
        else:
            
            await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
        return 


@dp.callback_query_handler(state=states.User.EditQuantity)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "back" in data:

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.Edit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if "minus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
        quantity -= 1

        if quantity == 0:
            
            # "Catalog button handler"
            async with state.proxy() as data:

                position = int(data['position'])

            position = ClientModule.core_models.Position.objects.get(pk=position)
            position.delete()

            text = Messages(user)['product_removed']

            await bot.answer_callback_query(callback_query.id, text)

            await bot.delete_message(user, callback_query.message.message_id)

            if not Client.get_cart_count(user):

                Client.cancel_cart(user)
                Client.clear_cart(user)

                await states.User.MainMenu.set()

                text = Messages(user)['main_menu']
                markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
                await bot.send_message(user, text, reply_markup=markup)
                
                return

            else:

                await states.User.Edit.set()

                text = Messages(user)['edit_menu']
                markup = keyboards.CartEditKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
                return

        async with state.proxy() as data:
            data['quantity'] = quantity

        await states.User.EditQuantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "plus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
            quantity += 1
            data['quantity'] = quantity

        await states.User.EditQuantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "accept" in data:

        # "Catalog button handler"
        async with state.proxy() as data:

            quantity = int(data['quantity'])
            position = int(data['position'])

        position = ClientModule.core_models.Position.objects.get(pk=position)
        position.count = quantity
        position.save()

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.Edit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if "remove" in data:

        # "Catalog button handler"
        async with state.proxy() as data:

            position = int(data['position'])

        position = ClientModule.core_models.Position.objects.get(pk=position)
        position.delete()

        text = Messages(user)['product_removed']

        await bot.answer_callback_query(callback_query.id, text)

        await bot.delete_message(user, callback_query.message.message_id)

        if not Client.get_cart_count(user):
            
            Client.cancel_cart(user)
            Client.clear_cart(user)

            await states.User.MainMenu.set()

            text = Messages(user)['main_menu']
            markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
            await bot.send_message(user, text, reply_markup=markup)

        else:

            await states.User.Edit.set()

            text = Messages(user)['edit_menu']
            markup = keyboards.CartEditKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

    await bot.answer_callback_query(callback_query.id)

    return


@dp.message_handler(state=states.User.Delivery)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 9).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        data = GenerateCart(user)
        text = data[0]

        await states.User.Cart.set()

        markup = keyboards.CartKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if button_code == 'self_delivery':

        async with state.proxy() as data:

            data['delivery'] = False
            
        br = Client.get_branches()
        if br.count() != 1:
            
            text = Messages(user)['set_branch']
        
            await states.User.SetBranch.set()

            markup = keyboards.BranchSelectKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

        else:
            
            text = Messages(user)['time_set_self']

            await states.User.Time.set()

            markup = keyboards.TimeKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
        
        return      

    if button_code == 'delivery':

        async with state.proxy() as data:

            data['delivery'] = True

        text = Messages(user)['location']

        await states.User.Location.set()

        markup = keyboards.LocationKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)


@dp.callback_query_handler(state=states.User.SetBranch)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)
    
    print(data)

    if "back" in data:

        text = Messages(user)['delivery']
        await states.User.Delivery.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return

    branch_number = int(data)
    async with state.proxy() as data:

        data['branch'] = branch_number

    text = Messages(user)['time_set_self']

    await states.User.Time.set()

    markup = keyboards.TimeKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)


@dp.callback_query_handler(state=states.User.Time)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)

    if "back" in data:
        
        async with state.proxy() as data:

            delivery = data['delivery']
            
        if not delivery:

            text = Messages(user)['delivery']
            await states.User.Delivery.set()

            markup = keyboards.DeliveryKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
        else:
            
            text = Messages(user)['location']

            await states.User.Location.set()

            markup = keyboards.LocationKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

        return

    if 'close_time' in data:

        async with state.proxy() as data:

            data['time'] = False

        ps = Client.get_paysystems()

        if ps.count() != 0:

            await states.User.PaymentType.set()

            text = Messages(user)['payment_type']

            markup = keyboards.PaymentTypeKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

        else:

            await states.User.OrderAccept.set()

            async with state.proxy() as data:

                text = GenerateOrder(user, data)

            markup = keyboards.OrderAcceptKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

    if 'set_time' in data:

        text = Messages(user)['set_time']

        await states.User.TimeSet.set()

        markup = keyboards.BackKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.message_handler(state=states.User.Location)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 10).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        text = Messages(user)['delivery']
        await states.User.Delivery.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return


@dp.message_handler(state=states.User.TimeSet)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id
    recieved_text = message.text
    button_code = ''
    language = Client.get_user_language(user)
    
    try:
        button_code = Client.get_buttons(language, 15).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        print(e)

    if "back" in button_code:
        
        async with state.proxy() as data:

            delivery = data['delivery']
            
        if not delivery:
            
            text = Messages(user)['time_set_self']

            await states.User.Time.set()

            markup = keyboards.TimeKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
            
        else:
            
            await states.User.Time.set()

            text = Messages(user)["time_set_delivery"]
            markup = keyboards.TimeKeyboard(user)

            await bot.send_message(user, text, reply_markup=markup)
            
        return

    async with state.proxy() as data:

        data['time'] = recieved_text

    text = Messages(user)['time_set_success']

    markup = None
    await bot.send_message(user, text, reply_markup=markup)

    ps = Client.get_paysystems()

    if ps.count() != 0:

        await states.User.PaymentType.set()

        text = Messages(user)['payment_type']

        markup = keyboards.PaymentTypeKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    else:

        await states.User.OrderAccept.set()

        async with state.proxy() as data:

            text = GenerateOrder(user, data)

        markup = keyboards.OrderAcceptKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    return


@dp.message_handler(state=states.User.Location, content_types=types.ContentType.LOCATION)
async def location_edit_handler(message: types.Message, state: FSMContext):   

    user = message.from_user.id

    async with state.proxy() as data:

        data['location_x'] = message.location.latitude
        data['location_y'] = message.location.longitude

    await states.User.Time.set()

    text = Messages(user)["time_set_delivery"]
    markup = keyboards.TimeKeyboard(user)

    await bot.send_message(user, text, reply_markup=markup)


@dp.message_handler(state=states.User.PaymentType)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 12).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        async with state.proxy() as data:

            time = data['time']
            delivery = data['delivery']
            
        if time:
            
            text = Messages(user)['set_time']

            await states.User.TimeSet.set()

            markup = keyboards.BackKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
        
        else:
            
            if not delivery:

                text = Messages(user)['time_set_self']

                await states.User.Time.set()

                markup = keyboards.TimeKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
            else:
                
                await states.User.Time.set()

                text = Messages(user)["time_set_delivery"]
                markup = keyboards.TimeKeyboard(user)

                await bot.send_message(user, text, reply_markup=markup)
        return

    if 'card' in button_code:
        
        async with state.proxy() as data:

            data['card'] = True
            
        text = Messages(user)['paysystem_choose']

        await states.User.PaySystemChoose.set()

        markup = keyboards.PaySystemKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if 'cash' in button_code:

        async with state.proxy() as data:

            data['card'] = False
            data['paysystem'] = None
            text = GenerateOrder(user, data)
            
        await states.User.OrderAccept.set()

        markup = keyboards.OrderAcceptKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.callback_query_handler(state=states.User.PaySystemChoose)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)

    if "back" in data:

        await states.User.PaymentType.set()

        text = Messages(user)['payment_type']

        markup = keyboards.PaymentTypeKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return
    
    paysystem = data
    async with state.proxy() as data:

        data['paysystem'] = paysystem
        
    await states.User.OrderAccept.set()

    async with state.proxy() as data:

        text = GenerateOrder(user, data)

    markup = keyboards.OrderAcceptKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)


@dp.message_handler(state=states.User.OrderAccept)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)
    
    try:
        button_code = Client.get_buttons(language, 13).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        async with state.proxy() as data:

            time = data['time']
            delivery = data['delivery']
            card = data['card']
            
        ps = Client.get_paysystems()

        if ps.count() != 0:
            
            if card:
            
                text = Messages(user)['paysystem_choose']

                await states.User.PaySystemChoose.set()

                markup = keyboards.PaySystemKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
                return

            else:
                
                await states.User.PaymentType.set()

                text = Messages(user)['payment_type']

                markup = keyboards.PaymentTypeKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
                return
            
        if time:
            
            text = Messages(user)['set_time']

            await states.User.TimeSet.set()

            markup = keyboards.BackKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
            
            return
        
        else:
            
            if not delivery:

                text = Messages(user)['time_set_self']

                await states.User.Time.set()

                markup = keyboards.TimeKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
                return
                
            else:
                
                await states.User.Time.set()

                text = Messages(user)["time_set_delivery"]
                markup = keyboards.TimeKeyboard(user)

                await bot.send_message(user, text, reply_markup=markup)
                
                return

    if 'accept' in button_code:
        
        
        async with state.proxy() as data:

            card = data['card']
        
        if not card:
            
            
            async with state.proxy() as data:
                
                text = GenerateOrder(user, data, True)
                order = Client.create_order(user, data)
                markup = keyboards.OrderAcceptOrRejectKeyboard(order.id)
                
                if order.delivery:
                    await bot.send_message(order.selected_branch.channel, text, reply_markup=None)
                    await bot.send_location(order.selected_branch.channel, latitude=order.latitude, longitude=order.longitude, reply_markup=markup)
                else:
                    await bot.send_message(order.selected_branch.channel, text, reply_markup=markup)
                    

            text = Messages(user)['order_accepted']
            
            markup = None
            await bot.send_message(user, text, reply_markup=markup)

            await states.User.MainMenu.set()

            text = Messages(user)['main_menu']
            markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
            await bot.send_message(user, text, reply_markup=markup)
            
        else:
            
            async with state.proxy() as data:
                
                text = GenerateOrder(user, data, True)
                order = Client.create_order(user, data)
                markup = keyboards.OrderAcceptOrRejectKeyboard(order.id)
                
                if order.delivery:
                    await bot.send_message(order.selected_branch.channel, text, reply_markup=None)
                    await bot.send_location(order.selected_branch.channel, latitude=order.latitude, longitude=order.longitude, reply_markup=markup)
                else:
                    await bot.send_message(order.selected_branch.channel, text, reply_markup=markup)
            
            text = Messages(user)['order_accepted']
            
            cart = Client.get_cart(user)
            async with state.proxy() as data:

                paysystem = data['paysystem']
            
            paysystem = Client.get_paysystem_token(int(paysystem))
            
            prices = []
            for position in cart.positions.all():
                text = f'{position.product.title} x {position.count}'
                prices.append(
                    types.LabeledPrice(label=text, amount=position.product.price * paysystem.eq)
                    )
                
            await states.User.PreCheckout.set()
            
            msg = await bot.send_invoice(
                user,
                title=Messages(user)['checkout_title'].upper(),
                description=Messages(user)['checkout_description'],
                provider_token=paysystem.token,
                currency=paysystem.currency,
                # photo_url='https://telegra.ph/file/4953b697a61d1c6bfba30.jpg',
                photo_height=512,  # !=0/None or picture won't be shown
                photo_width=512,
                photo_size=512,
                is_flexible=False,  # True If you need to set up Shipping Fee
                prices=prices,
                start_parameter='cinema-system-payment',
                payload='HAPPY FRIDAYS COUPON',
                reply_markup=keyboards.PayKeyboard(user, False)
                )
            
            
            async with state.proxy() as data:

                data['check_message'] = msg.message_id

        return
    
    if 'edit' in button_code:
        
        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return
    

@dp.pre_checkout_query_handler(lambda query: True, state=states.User.PreCheckout)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id, 
        ok=True,
        error_message="При проведении платежа, произошла ошибка. Если проблема повторится, пожалуйста, обратитесь в тех-поддержку"
        )
    
    await states.User.SuccessfulPayment.set()
    
    


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=states.User.SuccessfulPayment)
async def got_payment(message: types.Message, state: FSMContext):
    
    user = int(message.chat.id)
    
    async with state.proxy() as data:
                
        text = GenerateOrder(user, data, True)
        order = Client.create_order(user, data)
        markup = keyboards.OrderAcceptOrRejectKeyboard(order.id)
        
        if order.delivery:
            await bot.send_message(order.selected_branch.channel, text, reply_markup=None)
            await bot.send_location(order.selected_branch.channel, latitude=order.latitude, longitude=order.longitude, reply_markup=markup)
        else:
            await bot.send_message(order.selected_branch.channel, text, reply_markup=markup)
                    
    text = Messages(user)['order_accepted']
    
    async with state.proxy() as data:

        Client.create_order(user, data)

    markup = None
    await bot.send_message(user, text, reply_markup=markup)

    await states.User.MainMenu.set()

    text = Messages(user)['main_menu']
    markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
    await bot.send_message(user, text, reply_markup=markup)
    

@dp.callback_query_handler(state=states.User.PreCheckout)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)
    

    if "back" in data:

        await states.User.OrderAccept.set()

        async with state.proxy() as data:

            text = GenerateOrder(user, data)

        markup = keyboards.OrderAcceptKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return
    
    
@dp.callback_query_handler(state=states.User.OrderEdit)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)
    

    if "back" in data:

        await states.User.OrderAccept.set()

        async with state.proxy() as data:

            text = GenerateOrder(user, data)

        markup = keyboards.OrderAcceptKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return
    
    if 'time' in data:
        
        async with state.proxy() as data:

            delivery = data['delivery']
            
        if not delivery:
            
            text = Messages(user)['time_set_self']

            await states.User.TimeEdit.set()

            markup = keyboards.TimeKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
            
        else:
            
            await states.User.TimeEdit.set()

            text = Messages(user)["time_set_delivery"]
            markup = keyboards.TimeKeyboard(user)

            await bot.send_message(user, text, reply_markup=markup)
            
        return
    
    if "delivery" in data:
        
        text = Messages(user)['delivery']
        await states.User.DeliveryEdit.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
    if 'payment' in data:
        
        await states.User.PaymentTypeEdit.set()

        text = Messages(user)['payment_type']

        markup = keyboards.PaymentTypeKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return
    
    if 'product' in data:
        
        await states.User.OrderCartEdit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.callback_query_handler(state=states.User.OrderCartEdit)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "back" in data:
        
        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return

    if 'position' in data:

        await bot.delete_message(user, callback_query.message.message_id)

        position = int(data.replace('position ', ''))
        position = ClientModule.core_models.Position.objects.get(pk=position)

        await states.User.OrderEditQuantity.set()

        async with state.proxy() as data:
            data['quantity'] = position.count
            data['position'] = position.id

        current_product = position.product
        photo = Client.get_photo(current_product)
        # markup = None
        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, position.count)

        msg = await bot.send_photo(user, photo[0], caption=text, reply_markup=markup)

        async with state.proxy() as data:

            data['photo_message'] = msg.message_id

        if not photo[1]:

            Client.update_photo(photo[2], msg.photo[-1].file_id)

        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.OrderEditQuantity)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    if "back" in data:
        
        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.OrderCartEdit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if "minus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
        quantity -= 1

        if quantity == 0:
            
            # "Catalog button handler"
            async with state.proxy() as data:

                position = int(data['position'])

            position = ClientModule.core_models.Position.objects.get(pk=position)
            position.delete()

            text = Messages(user)['product_removed']

            await bot.answer_callback_query(callback_query.id, text)

            await bot.delete_message(user, callback_query.message.message_id)

            if not Client.get_cart_count(user):

                Client.cancel_cart(user)
                Client.clear_cart(user)

                await states.User.MainMenu.set()

                text = Messages(user)['main_menu']
                markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
                await bot.send_message(user, text, reply_markup=markup)
                
                return

            else:

                await states.User.OrderCartEdit.set()

                text = Messages(user)['edit_menu']
                markup = keyboards.CartEditKeyboard(user)
                await bot.send_message(user, text, reply_markup=markup)
                
                return

        async with state.proxy() as data:
            data['quantity'] = quantity

        await states.User.OrderEditQuantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "plus" in data:

        async with state.proxy() as data:

            quantity = int(data['quantity'])
            quantity += 1
            data['quantity'] = quantity

        await states.User.OrderEditQuantity.set()

        text = Messages(user)['quantity']
        markup = keyboards.EditQuantityKeyboard(user, quantity)
        await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)
        # await bot.edit_message_caption(user, callback_query.message.message_id, caption=text, reply_markup=markup)
        # await bot.edit_message_reply_markup(user, callback_query.message.message_id, reply_markup=markup)

    if "accept" in data:

        # "Catalog button handler"
        async with state.proxy() as data:

            quantity = int(data['quantity'])
            position = int(data['position'])

        position = ClientModule.core_models.Position.objects.get(pk=position)
        position.count = quantity
        position.save()

        await bot.delete_message(user, callback_query.message.message_id)

        await states.User.OrderCartEdit.set()

        text = Messages(user)['edit_menu']
        markup = keyboards.CartEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if "remove" in data:

        # "Catalog button handler"
        async with state.proxy() as data:

            position = int(data['position'])

        position = ClientModule.core_models.Position.objects.get(pk=position)
        position.delete()

        text = Messages(user)['product_removed']

        await bot.answer_callback_query(callback_query.id, text)

        await bot.delete_message(user, callback_query.message.message_id)

        if not Client.get_cart_count(user):
            
            Client.cancel_cart(user)
            Client.clear_cart(user)

            await states.User.MainMenu.set()

            text = Messages(user)['main_menu']
            markup = keyboards.MainMenuKeyboard(user, Client.get_cart_count(user))
            await bot.send_message(user, text, reply_markup=markup)

        else:

            await states.User.OrderCartEdit.set()

            text = Messages(user)['edit_menu']
            markup = keyboards.CartEditKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)

    await bot.answer_callback_query(callback_query.id)

    return
    
    
@dp.message_handler(state=states.User.PaymentTypeEdit)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 12).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return

    if 'card' in button_code:
        
        async with state.proxy() as data:

            data['card'] = True
            
        text = Messages(user)['paysystem_choose']

        await states.User.PaySystemChooseEdit.set()

        markup = keyboards.PaySystemKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if 'cash' in button_code:
        

        async with state.proxy() as data:

            data['card'] = False
            data['paysystem'] = None
            text = GenerateOrder(user, data)
            
        text = Messages(user)['info_updated']
        markup = None
        await bot.send_message(user, text, reply_markup=markup)

        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
    
    
@dp.callback_query_handler(state=states.User.PaySystemChooseEdit)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)
    

    if "back" in data:

        await states.User.PaymentTypeEdit.set()

        text = Messages(user)['payment_type']

        markup = keyboards.PaymentTypeKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return
    
    paysystem = data
    async with state.proxy() as data:

        data['paysystem'] = paysystem
        
    text = Messages(user)['info_updated']
    markup = None
    await bot.send_message(user, text, reply_markup=markup)

    await states.User.OrderEdit.set()

    text = Messages(user)['order_edit']
    markup = keyboards.OrderEditKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
    
    
@dp.callback_query_handler(state=states.User.TimeEdit)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)

    if "back" in data:
        
        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return

    if 'close_time' in data:

        async with state.proxy() as data:

            data['time'] = False
            
        text = Messages(user)['info_updated']
        markup = None
        await bot.send_message(user, text, reply_markup=markup)

        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

    if 'set_time' in data:

        text = Messages(user)['set_time']

        await states.User.TimeSetEdit.set()

        markup = keyboards.BackKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.message_handler(state=states.User.TimeSetEdit)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id
    recieved_text = message.text
    button_code = ''
    language = Client.get_user_language(user)
    
    try:
        button_code = Client.get_buttons(language, 15).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        print(e)

    if "back" in button_code:
        
        async with state.proxy() as data:

            delivery = data['delivery']
            
        if not delivery:
            
            text = Messages(user)['time_set_self']

            await states.User.TimeEdit.set()

            markup = keyboards.TimeKeyboard(user)
            await bot.send_message(user, text, reply_markup=markup)
            
        else:
            
            await states.User.TimeEdit.set()

            text = Messages(user)["time_set_delivery"]
            markup = keyboards.TimeKeyboard(user)

            await bot.send_message(user, text, reply_markup=markup)
            
        return


    async with state.proxy() as data:

        data['time'] = recieved_text

    text = Messages(user)['info_updated']
    markup = None
    await bot.send_message(user, text, reply_markup=markup)

    await states.User.OrderEdit.set()

    text = Messages(user)['order_edit']
    markup = keyboards.OrderEditKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
    
    return


@dp.message_handler(state=states.User.DeliveryEdit)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = int(message.from_user.id)
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 9).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        await states.User.OrderEdit.set()

        text = Messages(user)['order_edit']
        markup = keyboards.OrderEditKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return

    if button_code == 'self_delivery':

        async with state.proxy() as data:

            data['delivery'] = False
            
        text = Messages(user)['set_branch']
        
        await states.User.EditBranch.set()

        markup = keyboards.BranchSelectKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return

    if button_code == 'delivery':

        async with state.proxy() as data:

            data['delivery'] = True

        text = Messages(user)['location']

        await states.User.LocationEdit.set()

        markup = keyboards.LocationKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.callback_query_handler(state=states.User.EditBranch)
async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
    user = int(callback_query.from_user.id)
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user, callback_query.message.message_id)

    if "back" in data:

        text = Messages(user)['delivery']
        await states.User.DeliveryEdit.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)

        return

    branch_number = int(data)
    async with state.proxy() as data:

        data['branch'] = branch_number

    await states.User.OrderEdit.set()

    text = Messages(user)['order_edit']
    markup = keyboards.OrderEditKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
        
        
@dp.message_handler(state=states.User.LocationEdit)
async def user_ammount_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id
    recieved_text = message.text
    language = Client.get_user_language(user)

    try:
        button_code = Client.get_buttons(language, 10).get(
            title=recieved_text
            ).button_code

    except Exception as e:
        return

    if "back" in button_code:

        text = Messages(user)['delivery']
        await states.User.DeliveryEdit.set()

        markup = keyboards.DeliveryKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        
        return
    

@dp.message_handler(state=states.User.LocationEdit, content_types=types.ContentType.LOCATION)
async def location_edit_handler(message: types.Message, state: FSMContext):   

    user = message.from_user.id

    async with state.proxy() as data:

        data['location_x'] = message.location.latitude
        data['location_y'] = message.location.longitude

    text = Messages(user)['info_updated']
    markup = None
    await bot.send_message(user, text, reply_markup=markup)

    await states.User.OrderEdit.set()

    text = Messages(user)['order_edit']
    markup = keyboards.OrderEditKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
    
    return

# @dp.callback_query_handler(state=states.User.MainMenu)
# async def callback_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext):   
#     user = int(callback_query.from_user.id)
#     data = callback_query.data
#     print(data)
#     if "accept_order_channel" in data:
#         manager_chat_id = user
#         order_num = int(data.replace('accept_order_channel ', ''))

#         order = get_order(order_num)
#         if order.branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

#             order.manager = Client.get_user(manager_chat_id)
#             order.status = Client.core_models.OrderStatus.objects.get(pk=2)
#             order.save()
            
#             user = order.user.chat_id

#             text = Messages(user)['in_porgress_cooking']
#             markup = None
#             await bot.send_message(user, text, reply_markup=markup)
            
#             if order.delivery:
#                 markup = keyboards.DeliveryStatusKeyboard(order.id)
#             else:
#                 markup = keyboards.SelfStatusKeyboard(order.id)
                
#             await bot.edit_message_reply_markup(order.branch.channel,
#                                                 message_id=callback_query.message.message_id,
#                                                 reply_markup=markup)
#         else:
            
#             await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
#         return
    
#     if 'to_delivery' in data:
#         manager_chat_id = user
#         order_num = int(data.replace('to_delivery ', ''))

#         order = get_order(order_num)
#         if order.branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

#             order.status = Client.core_models.OrderStatus.objects.get(pk=3)
#             order.save()
            
#             user = order.user.chat_id

#             text = Messages(user)['in_porgress_to_delivery']
#             markup = None
#             await bot.send_message(user, text, reply_markup=markup)
#             await bot.answer_callback_query(callback_query.id, text='Заказ передан на доставку')
            
#             markup = keyboards.EndStatusKeyboard(order.id)
#             await bot.edit_message_reply_markup(order.branch.channel,
#                                                 message_id=callback_query.message.message_id,
#                                                 reply_markup=markup)
#         else:
            
#             await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
#         return    
    
#     if 'to_self' in data:
#         manager_chat_id = user
#         order_num = int(data.replace('to_self ', ''))

#         order = get_order(order_num)
#         if order.branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

#             order.status = Client.core_models.OrderStatus.objects.get(pk=3)
#             order.save()
            
#             user = order.user.chat_id

#             text = Messages(user)['in_porgress_to_self']
#             markup = None
#             await bot.send_message(user, text, reply_markup=markup)
#             await bot.answer_callback_query(callback_query.id, text='Заказ передан на самовывоз')
            
            
#             markup = keyboards.EndStatusKeyboard(order.id)
#             await bot.edit_message_reply_markup(order.branch.channel,
#                                                 message_id=callback_query.message.message_id,
#                                                 reply_markup=markup)
#         else:
            
#             await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
#         return 
    
#     if 'to_end' in data:
#         manager_chat_id = user
#         order_num = int(data.replace('to_end ', ''))

#         order = get_order(order_num)
#         if order.branch.managers.all().filter(chat_id=manager_chat_id).count() != 0:

#             order.status = Client.core_models.OrderStatus.objects.get(pk=4)
#             order.active = False
#             order.save()
            
#             user = order.user.chat_id

#             await bot.answer_callback_query(callback_query.id, text='Заказ завершен')
            
#             markup = None
#             await bot.edit_message_reply_markup(order.branch.channel,
#                                                 message_id=callback_query.message.message_id,
#                                                 reply_markup=markup)
#         else:
            
#             await bot.answer_callback_query(callback_query.id, text='У вас нет доступа к изменению статуса')
#         return 


async def shutdown(dispatcher: Dispatcher):

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

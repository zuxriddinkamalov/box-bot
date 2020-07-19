from client import Client as client
import client as Client_module

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup


Client = client()


def BuildMenu(buttons,
              n_cols,
              header_buttons=None,
              footer_buttons=None):

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        header_buttons.reverse()
        for btn in header_buttons:

            menu.insert(0, [btn])

    if footer_buttons:

        for btn in footer_buttons:

            menu.append([btn])
    return menu


def LanguageKeyboard(user):

    buttons = Client_module.core_models.Language.objects.all().order_by('order')
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.text))

    return ReplyKeyboardMarkup(
        [end_buttons],
        resize_keyboard=True,
        one_time_keyboard=True
        )


def MainMenuKeyboard(user, cart_count):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 1)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title.replace('[{cart}]', f'[ {cart_count} ]' if cart_count != 0 else "")))

    end_buttons = BuildMenu(
        end_buttons[2:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        header_buttons=[end_buttons[0],
                        end_buttons[1]]
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def CategoryKeyboard(user, page):

    language = Client.get_user_language(user)

    data = Client.get_categories(language, page)
    buttons = data['categories']
    end_buttons = []

    for button in buttons:

        end_buttons.append(InlineKeyboardButton(button.title, callback_data=f'category {button.id}'))

    buttons = Client.get_buttons(language, 2)

    prev_button = InlineKeyboardButton(buttons[0].title, callback_data=f'prev {data["prev"]}')
    empty_button = InlineKeyboardButton(f'{page}/{data["total"]}', callback_data=f'empty')
    next_button = InlineKeyboardButton(buttons[1].title, callback_data=f'next {data["next"]}')
    back_button = InlineKeyboardButton(buttons[2].title, callback_data=f'back')

    end_buttons = BuildMenu(
        end_buttons,
        2
        )

    end_buttons.append([
        prev_button,
        empty_button,
        next_button
    ])
    end_buttons.append([back_button])

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def ProductKeyboard(user, page, category):

    language = Client.get_user_language(user)

    data = Client.get_products(language, category, page)
    buttons = data['products']
    end_buttons = []

    for button in buttons:

        end_buttons.append(InlineKeyboardButton(button.title, callback_data=f'product {button.id}'))

    buttons = Client.get_buttons(language, 2)

    prev_button = InlineKeyboardButton(buttons[0].title, callback_data=f'prev {data["prev"]} {category}')
    empty_button = InlineKeyboardButton(f'{page}/{data["total"]}', callback_data=f'empty')
    next_button = InlineKeyboardButton(buttons[1].title, callback_data=f'next {data["next"]} {category}')
    back_button = InlineKeyboardButton(buttons[2].title, callback_data=f'back')

    end_buttons = BuildMenu(
        end_buttons,
        2
        )

    end_buttons.append([
        prev_button,
        empty_button,
        next_button
    ])
    end_buttons.append([back_button])

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def ProductDetailsKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 3)
    end_buttons = []

    end_buttons.append(InlineKeyboardButton(buttons[0].title, callback_data=f'add'))
    end_buttons.append(InlineKeyboardButton(buttons[1].title, callback_data=f'back'))

    end_buttons = BuildMenu(
        end_buttons,
        1,
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def QuantityKeyboard(user, current):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 4)
    end_buttons = []

    end_buttons.append(InlineKeyboardButton(buttons[0].title, callback_data=f'minus'))
    end_buttons.append(InlineKeyboardButton(buttons[1].title.replace('{quantity}', str(current)), callback_data=f'empty'))
    end_buttons.append(InlineKeyboardButton(buttons[2].title, callback_data=f'plus'))

    end_buttons = BuildMenu(
        end_buttons,
        3,
        footer_buttons=[
            InlineKeyboardButton(buttons[3].title, callback_data=f'accept'),
            InlineKeyboardButton(buttons[4].title, callback_data=f'back'),
        ]
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def EditQuantityKeyboard(user, current):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 4)
    delete_button = Client.get_buttons(language, 14).first()
    
    end_buttons = []

    end_buttons.append(InlineKeyboardButton(buttons[0].title, callback_data=f'minus'))
    end_buttons.append(InlineKeyboardButton(buttons[1].title.replace('{quantity}', str(current)), callback_data=f'empty'))
    end_buttons.append(InlineKeyboardButton(buttons[2].title, callback_data=f'plus'))

    end_buttons = BuildMenu(
        end_buttons,
        3,
        footer_buttons=[
            InlineKeyboardButton(buttons[3].title, callback_data=f'accept'),
            InlineKeyboardButton(delete_button.title, callback_data=f'remove'),
            InlineKeyboardButton(buttons[4].title, callback_data=f'back'),
        ]
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def CartKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 5)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title))

    end_buttons = BuildMenu(
        end_buttons[:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def CartEditKeyboard(user):

    language = Client.get_user_language(user)

    button = Client.get_buttons(language, 6).first()
    end_buttons = []

    positions = Client.get_cart(user).positions.all()

    for position in positions:

        end_buttons.append(InlineKeyboardButton(f'{position.count} x {position.product.title}', callback_data=f'position {position.id}'))

    end_buttons = BuildMenu(
        end_buttons,
        1,
        footer_buttons=[
            InlineKeyboardButton(button.title, callback_data=f'back')]
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def CancelButton(user, counter):

    language = Client.get_user_language(user)

    button = Client.get_buttons(language, 7).first()
    end_buttons = []

    end_buttons.append(InlineKeyboardButton(button.title.replace('( {counter} )', f'( {counter} )' if counter != 0 else ""), callback_data=f'cancel'))

    end_buttons = BuildMenu(
        end_buttons,
        1
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def ContactKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 8)

    return ReplyKeyboardMarkup([[KeyboardButton(buttons[0].title, request_contact=True)], [KeyboardButton(buttons[1].title)]], resize_keyboard=True, one_time_keyboard=True)


def DeliveryKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 9)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title))

    end_buttons = BuildMenu(
        end_buttons[:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def LocationKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 10)

    return ReplyKeyboardMarkup([[KeyboardButton(buttons[0].title, request_location=True)], [KeyboardButton(buttons[1].title)]], resize_keyboard=True, one_time_keyboard=True)


def TimeKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 11)
    end_buttons = []

    for button in buttons:
        end_buttons.append(
            InlineKeyboardButton(button.title, callback_data=f'{button.button_code}')
            )

    end_buttons = BuildMenu(
        end_buttons[:-1],
        1,
        footer_buttons=[end_buttons[-1]],
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def PaymentTypeKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 12)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title))

    end_buttons = BuildMenu(
        end_buttons[:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def OrderAcceptKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 13)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title))

    end_buttons = BuildMenu(
        end_buttons[:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def BackKeyboard(user):
    
    language = Client.get_user_language(user)

    button = Client.get_buttons(language, 15).first()
    end_buttons = []

    end_buttons.append(KeyboardButton(button.title))

    end_buttons = BuildMenu(
        end_buttons,
        1,
        )

    return ReplyKeyboardMarkup(end_buttons, resize_keyboard=True, one_time_keyboard=True)


def PaySystemKeyboard(user):

    language = Client.get_user_language(user)

    back_button = Client.get_buttons(language, 15).first()
    ps = Client.get_paysystems()

    end_buttons = []

    for button in ps:
        end_buttons.append(
            InlineKeyboardButton(button.title, callback_data=f'{button.id}')
            )

    end_buttons = BuildMenu(
        end_buttons,
        2,
        footer_buttons=[InlineKeyboardButton(back_button.title, callback_data=f'back')],
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard


def OrderEditKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 16)
    end_buttons = []

    for button in buttons:
        end_buttons.append(
            InlineKeyboardButton(button.title, callback_data=f'{button.button_code}')
            )

    end_buttons = BuildMenu(
        end_buttons[:-1],
        2,
        footer_buttons=[end_buttons[-1]],
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard
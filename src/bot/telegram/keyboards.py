from client import Client as client

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

    buttons = Client.core_models.Language.objects.all().order_by('order')
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.text))

    return ReplyKeyboardMarkup(
        [end_buttons],
        resize_keyboard=True,
        one_time_keyboard=True
        )


def MainMenuKeyboard(user):

    language = Client.get_user_language(user)

    buttons = Client.get_buttons(language, 1)
    end_buttons = []

    for button in buttons:

        end_buttons.append(KeyboardButton(button.title))

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

    prev_button = InlineKeyboardButton(buttons[0].title, callback_data=f'next {data["next"]}')
    empty_button = InlineKeyboardButton(f'{page}/{data["total"]}', callback_data=f'empty')
    next_button = InlineKeyboardButton(buttons[1].title, callback_data=f'prev {data["prev"]}')

    end_buttons = BuildMenu(
        end_buttons,
        2
        )

    end_buttons.append([
        prev_button,
        empty_button,
        next_button
    ])
    print(f'\n\n{end_buttons}\n\n')

    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard = end_buttons

    return keyboard

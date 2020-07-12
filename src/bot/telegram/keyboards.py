import client as Client
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def BuildMenu(buttons,
              n_cols,
              header_buttons=None,
              footer_buttons=None):

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:

        menu.insert(0, header_buttons)

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

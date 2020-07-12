from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class User(StatesGroup):
    ChooseLanguage = State()
    MainMenu = State()
    Category = State()

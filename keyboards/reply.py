from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# User #

# Start keyboard
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать задачу"),
            KeyboardButton(text="Просмотр текущих задач"),
            KeyboardButton(text="Просмотр закрытых задач")
        ],
    ],
    resize_keyboard=True
)

# confirm adding task
confirm_or_change_task = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить задачу")],

        [KeyboardButton(text="Изменить предыдущее поле")],

        [KeyboardButton(text="отмена")],
    ],
    resize_keyboard=True
)

# cancel keyboard

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")]
    ]
)

# cancel or back keyboard
cancel_or_back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
        [KeyboardButton(text="Изменить предыдущее поле")]
    ]
)


# KeyboardBuilder #
def get_keyboard(
        *btns: str,
        sizes: tuple[int] = (2,),
):
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True)

from aiogram.types import BotCommand
private = [
    # BotCommand(command="...", description="..."),
    BotCommand(command="add_task", description="Добавить задачу"),
    BotCommand(command="get_tasks", description="Получить все текущие задачи"),
    BotCommand(command="close_task", description="Закрыть задачу"),
    BotCommand(command="change_task", description="Изменить задачу"),
    BotCommand(command="delete_task", description="Удалить задачу")
]

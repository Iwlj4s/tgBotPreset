# Aiogram Imports #
from aiogram import F, Router

from aiogram.filters import CommandStart, Command, StateFilter, or_f

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message, CallbackQuery

# SqlAlchemy Imports #
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dao.general_dao import GeneralDAO
from dao.tasks_dao import TasksDAO
from database import models
# My Imports #
from keyboards import reply
from keyboards.inline import get_callback_btns
from repository import user_repository

user_private_router = Router()


# STATE MACHINE #
class AddTask(StatesGroup):
    add_task_name = State()
    add_task_body = State()

    confirm_task = State()

    texts = {
        'AddTask:add_task_name': "Заново введите название задачи",
        'AddTask:add_task_body': "Заново введите Задачу"
    }


# Start
@user_private_router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    print("COMMAND START")
    await user_repository.add_user(user_tg_id=message.from_user.id,
                                   user_name=message.from_user.first_name,
                                   session=session)
    print("AFTER add_user")
    await message.answer(f"Hi, {message.from_user.first_name} !")
    await message.answer(f"Вы зарегистрированы!",
                         reply_markup=reply.main_keyboard)


@user_private_router.message(StateFilter("*"), F.text.lower() == "просмотр текущих задач")
async def view_tasks(message: Message, session: AsyncSession):
    current_user = await GeneralDAO.get_item_by_tg_id(session=session, 
                                                      item=models.User,
                                                      item_tg_id=message.from_user.id)
    tasks = await TasksDAO.get_tasks_by_user_id(session=session, user_id=current_user.id)

    await message.answer(f"Ваши задачи:",
                         reply_markup=reply.main_keyboard)
    for task in tasks:
        await message.answer(f"{task.task_name}\n"
                             f"{task.task_body}\n"
                             f"Задача создана - {task.created}",
                             reply_markup=get_callback_btns(btns={
                                 'Закрыть задачу': f'close_task_{task.id}'
                             }))


@user_private_router.message(StateFilter("*"), F.text.lower() == "просмотр закрытых задач")
async def view_closed_tasks(message: Message, session: AsyncSession):
    current_user = await GeneralDAO.get_item_by_tg_id(session=session, 
                                                      item=models.User,
                                                      item_tg_id=message.from_user.id)
    closed_tasks = await TasksDAO.get_closed_tasks_by_user_id(session=session, user_tg_id=current_user.id)

    await message.answer(f"Ваши закрытые задачи:\n",
                         reply_markup=reply.main_keyboard)
    for closed_task in closed_tasks:
        await message.answer(f"{closed_task.task_name}\n"
                             f"{closed_task.task_body}\n"
                             f"Задача создана - {closed_task.created}",
                             reply_markup=get_callback_btns(btns={
                                 'Удалить задачу': f'delete_closed_task_{closed_task.id}'
                             }))


# Close task callback
@user_private_router.callback_query(F.data.startswith("close_task_"))
async def close_task(callback_query: CallbackQuery, session: AsyncSession):
    task_id = int(callback_query.data.split('_')[-1])
    user_tg_id = callback_query.from_user.id

    task = await GeneralDAO.get_item_by_id(session=session,
                                           item_id=task_id,
                                           item=models.Task)

    await TasksDAO.add_closed_task(session=session,
                                   data=task,
                                   old_task=task)

    await callback_query.answer("Вы закрыли задачу!")
    await callback_query.message.answer(f"Вы закрыли задачу! {task.task_name}")


# Delete task
@user_private_router.callback_query(or_f(F.data.startswith("delete_task_"), F.data.startswith("delete_closed_task_")))
async def delete_task(callback_query: CallbackQuery, session: AsyncSession):
    task_id = int(callback_query.data.split('_')[-1])
    item = None

    if callback_query.data.startswith("delete_task_"):
        print("УДаляется обычная")
        item = models.Task
    else:
        print("УДаляется закрытая")
        item = models.ClosedTask

    task = await GeneralDAO.get_item_by_id(session=session, item=item, item_id=task_id)

    if not task:
        await callback_query.answer("Задача не найдена!")
        return

    try:
        await GeneralDAO.delete_item(session=session, item=item, item_id=task_id)
        await callback_query.answer("Вы удалили задачу!")
        await callback_query.message.answer(f"Вы удалили задачу! {task.task_name}")
    except Exception as e:
        await callback_query.answer("Ошибка при удалении задачи!")
        print(f"Ошибка: {e}")


# Cancel handler
@user_private_router.message(StateFilter("*"), F.text.lower() == "отмена")  # "отмена" == "cancel"
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    print("State Clear")
    await message.answer("Действие отменено",
                         reply_markup=reply.main_keyboard)


# Back handler#
@user_private_router.message(StateFilter('*'), F.text.lower() == "изменить предыдущее поле")
@user_private_router.message(StateFilter('*'), Command("Изменить предыдущее поле"))
async def back_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AddTask.add_task_name:
        await message.answer("Предыдущего шага нет, введите свое имя или нажмите 'отмена' ")
        return

    previous_state = None
    for step in AddTask.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state.state)
            await message.answer(f"Вы вернулись к предыдущему шагу\n"
                                 f"{AddTask.texts[previous_state.state]}")
            return
        previous_state = step


@user_private_router.message(or_f(Command("add_task"), (F.text.lower() == "создать задачу")))
@user_private_router.message(StateFilter(None), Command("add_task"))
async def add_task(message: Message, state: FSMContext):
    await message.answer(f"Введите название задачи",
                         reply_markup=reply.cancel_keyboard)

    await state.set_state(AddTask.add_task_name)


@user_private_router.message(AddTask.add_task_name, F.text)
async def add_task_name(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text.title())

    await message.answer("Введите задачу", reply_markup=reply.cancel_or_back_keyboard)

    await state.set_state(AddTask.add_task_body)


@user_private_router.message(AddTask.add_task_body, F.text)
async def add_task_body(message: Message, state: FSMContext):
    await state.update_data(task_body=message.text.title())

    await message.answer("Добавить задачу?", reply_markup=reply.confirm_or_change_task)

    await state.set_state(AddTask.confirm_task)


@user_private_router.message(AddTask.confirm_task, F.text.lower() == "добавить задачу")
async def confirm_task(message: Message, state: FSMContext, session: AsyncSession):
    user = await GeneralDAO.get_item_by_tg_id(session=session,
                                              item=models.User,
                                              item_tg_id=message.from_user.id)
    
    await state.update_data(user_id=user.id)
    task_data = await state.get_data()
    print(f"TASK DATA: {task_data}")

    await user_repository.add_task(data=task_data, session=session)
    task_name = task_data["task_name"]
    task_body = task_data["task_body"]
    await message.answer(f"Вот ваша задача:\n{task_name}\n{task_body}",
                         reply_markup=reply.main_keyboard)

    await state.clear()


# Echo answer func
@user_private_router.message()
async def echo_answer(message: Message):
    await message.answer(f"You say: {message.text}")

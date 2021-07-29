from loguru import logger
from aiogram import types

import config as cfg
from config import dp

# Models
from support.models import Chat, User

from addons.creation_date.data_handler import init_cd_scheduler
from .data_handler import get_tg_id_data
from addons.utils.creation_date_interpolation import approximate
from addons.utils.utils import tree_display, time_format


logger.debug("Creation account date loaded")


@dp.message_handler(regexp=r"^/me|^/start")
async def cd_get_me(message: types.Message, Chat: Chat, User: User):
    user: dict = message.to_python()["from"]
    user["account create"] = time_format(await approximate(User.id))
    await message.answer(f"👁 User info\n{tree_display(user)}")


@dp.message_handler(regexp=r"^/id ")
async def cd_get_id(message: types.Message, Chat: Chat, User: User):
    try:
        _id = int(message.get_args().split()[-1])
        user: dict = {"account create": time_format(await approximate(_id))}
        await message.answer(f"👁 User info\n{tree_display(user)}")
    except Exception:
        await message.answer("Example: <code>/id 123456789</code>")
        return


@dp.message_handler(regexp=r"/test", user_id=cfg.admins)
async def cd_test(message: types.Message, Chat: Chat, User: User):
    await message.answer("Тестирую получение нового id")
    await get_tg_id_data()

init_cd_scheduler()

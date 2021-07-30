from loguru import logger
from aiogram import types

from config import dp

# Models
from support.models import Chat, User

from addons.creation_date.data_handler import init_cd_scheduler, get_user_by_username
from addons.creation_date.data_handler import User as tlTypeUser
from addons.utils.creation_date_interpolation import approximate
from addons.utils.utils import tree_display, time_format


logger.debug("Creation account date loaded")

start_answer = [
    "Hi {username} this is BOT!"
]

@dp.message_handler(regexp=r"^/me|^/start")
async def cd_get_me(message: types.Message, Chat: Chat, User: User):
    if message.text == "/start":
        await message.answer(
            "\n".join(start_answer).format(
                username=message.from_user.full_name,
            )
        )
    user: dict = message.to_python()["from"]
    user["account create"] = time_format(await approximate(User.id))
    await message.answer(f"👁 User info\n{tree_display(user)}")


@dp.message_handler(regexp=r"^/id ")
async def cd_get_by_id(message: types.Message, Chat: Chat, User: User):
    try:
        _id = int(message.get_args().split()[-1])
        user: dict = {"account create": time_format(await approximate(_id))}
        await message.answer(f"👁 User info\n{tree_display(user)}")
    except Exception:
        await message.answer("Example: <code>/id 123456789</code>")
        return


@dp.message_handler(regexp=r"@\w+")
async def cd_get_by_username(message: types.Message, Chat: Chat, User: User):
    try:
        u = await get_user_by_username(message.text)
        entity = dict()

        if isinstance(u, tlTypeUser):
            entity["id"] = f"<code>{u.id}</code>"
            entity["is_bot"] = u.bot
            entity["first_name"] = u.first_name
            entity["last_name"] = u.last_name
            entity["username"] = u.username
            entity["account create"] = time_format(await approximate(u.id))
            entity["scam"] = u.scam
            entity["deleted"] = u.deleted
            if u.phone:
                entity["phone"] = u.phone

        else:
            entity["id"] = f"<code>{u.id}</code>"
            entity["title"] = u.title
            entity["account create"] = entity["date"].date()
            entity["username"] = u.username

        await message.answer(f"👁 {u.__class__.__name__} info\n{tree_display(entity)}")
    except Exception:
        await message.answer("Example: <code>@Leroy_SU</code>")


@dp.message_handler(is_forwarded=True)
async def cd_get_by_forward(message: types.Message, Chat: Chat, User: User):
    try:
        forward = message.to_python()
        entity = forward["forward_from"]
        entity["account create"] = time_format(await approximate(entity["id"]))
        entity["forward_date"] = time_format(forward["forward_date"])
        entity["text"] = forward["text"]

        await message.answer(f"👁 Forward info\n{tree_display(entity)}")
    except Exception:
        await message.answer("Example: <code>@Leroy_SU</code>")

init_cd_scheduler()

import datetime

from loguru import logger

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import (
    CreateChannelRequest, DeleteChannelRequest)

import config as cfg
from support.models import IdCreationDate
from support.repositories import IdCreationDateRepository
from support.scheduler import scheduler


async def get_tg_id_data(
    timestamp=int(datetime.datetime.utcnow().timestamp()),
) -> None:
    client = TelegramClient(
        StringSession(cfg.USERBOT_SESSION_STRING),
        cfg.USERBOT_API_ID,
        cfg.USERBOT_API_HASH,
    )
    if not client.is_connected():
        await client.connect()

    await client.get_dialogs()
    udp = await client(
        CreateChannelRequest(f"get_id_{timestamp}", "NONE")
    )
    _id = udp.updates[1].channel_id
    await client(
        DeleteChannelRequest(_id)
    )
    await IdCreationDateRepository.create(
        IdCreationDate(
            id=_id,
            created_at=timestamp
        )
    )
    logger.info(f"Add new id[{_id}] to database. Timestamp: {timestamp}")


def init_cd_scheduler() -> bool:
    if all(
        (cfg.USERBOT_SESSION_STRING, cfg.USERBOT_API_HASH, cfg.USERBOT_API_ID)
    ):
        scheduler.add_job(
            func=get_tg_id_data,
            trigger='interval',
            minutes=60*24*3,
            id="get_tg_id_data",
            replace_existing=True
        )
        return True
    logger.error(
        "Creation date scheduler did not start, check the userbot settings"
    )
    return False

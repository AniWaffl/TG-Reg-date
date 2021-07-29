import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession

import src.config as cfg


async def main():
    client = TelegramClient(
        StringSession(),
        cfg.USERBOT_API_ID,
        cfg.USERBOT_API_HASH,
    )
    if client.is_connected():
        print("[INFO] Telethon client alredy connected!")
        return

    await client.connect()
    phone = input("[INPUT] Phone number [+123456]: ")
    await client.send_code_request(phone)
    code = int(input("[INPUT] Security code: "))
    twoFa = str(input("[OPTIONAL INPUT] Two-steps password: "))
    twoFa = twoFa if len(twoFa) > 4 else None

    try:
        await client.sign_in(phone=phone, code=code)
    except Exception:
        await client.sign_in(password=twoFa)

    me = await client.get_me()
    print(f"[INFO] User login - {me.first_name} {me.last_name} [{me.id}]")

    string_session = StringSession.save(client.session)
    print(f"[INFO] String Session is:\n{string_session}")
    print("[INFO] Copy this to enviroment")

    await client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

from support.repositories import IdCreationDateRepository

MAX_UNIX_TIMESTAMP: int = 2_147_483_647

# TODO Refractor this trash ^_^


async def approximate(tg_id: int) -> int:
    a = await IdCreationDateRepository().get_min_id()
    near_id, near_date = a.id, a.created_at
    a = await IdCreationDateRepository().get_near_id(tg_id)
    min_id, min_date = a.id, a.created_at

    min_id = min_id if near_id != min_id else min_id - 1

    idratio = (tg_id - min_id) / (near_id - min_id)
    midDate = int((idratio * (near_date - min_date)) + min_date)

    if midDate > MAX_UNIX_TIMESTAMP:
        return MAX_UNIX_TIMESTAMP

    return midDate

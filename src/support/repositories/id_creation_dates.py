from typing import List, Optional

from support.db import id_creation_dates
from support.models import IdCreationDate
from .base import BaseRepository


class IdCreationDateRepository(BaseRepository):

    async def get_all(
        self,
        limit: int = 100,
        skip: int = 0
    ) -> List[IdCreationDate]:
        query = id_creation_dates.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[IdCreationDate]:
        query = id_creation_dates.select().where(id_creation_dates.c.id == id)
        data = await self.database.fetch_one(query)
        if data is None:
            return None
        return IdCreationDate.parse_obj(data)

    async def get_min_id(self) -> Optional[IdCreationDate]:
        query = """
SELECT id, created_at
FROM id_creation_dates
WHERE id = (SELECT MIN(id) FROM id_creation_dates);
"""
        data = await self.database.fetch_one(query)
        if data is None:
            return None
        return IdCreationDate.parse_obj(data)

    async def get_near_id(self, tg_id) -> Optional[IdCreationDate]:
        query = f"""
SELECT id, created_at, MIN(ABS(id-{tg_id}))
FROM id_creation_dates;
"""
        data = await self.database.fetch_one(query)
        if data is None:
            return None
        return IdCreationDate.parse_obj(data)

    async def create(self, u: IdCreationDate) -> IdCreationDate:
        query = id_creation_dates.insert().values(**u.dict())
        return await self.database.execute(query)

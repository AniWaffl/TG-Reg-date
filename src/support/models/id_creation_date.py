import datetime
from pydantic import BaseModel


class IdCreationDate(BaseModel):
    id: int
    created_at: int

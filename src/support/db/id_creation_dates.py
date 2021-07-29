import sqlalchemy as sa
from .base import metadata
import datetime

id_creation_dates = sa.Table(
    "id_creation_dates",
    metadata,

    sa.Column("id", sa.Integer, primary_key=True, unique=True),
    sa.Column("created_at", sa.Integer),
)

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config as cfg

executors = {
    "default": AsyncIOExecutor(),
}

job_defaults = {
    "coalesce": False,
    "max_instances": 3,
    "timezone": "UTC",
}

jobstores = {
    "default": SQLAlchemyJobStore(
        url=cfg.DATABASE_URL,),
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    job_defaults=job_defaults,
    executors=executors)

from typing import Final
from databases import Database

from ..config import get_settings


__all__ = ['db']


db: Final[Database] = Database(
    get_settings().database_url,
    min_size=get_settings().database_pool_min_size,
    max_size=get_settings().database_pool_max_size)

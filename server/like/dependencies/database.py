from typing import Final
from databases import Database

from ..config import get_settings


__all__ = ['db']


db: Final[Database] = Database(get_settings().database_url)

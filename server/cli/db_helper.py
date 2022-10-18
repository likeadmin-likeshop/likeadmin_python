import typer
from sqlalchemy import create_engine

from env import build_env

build_env(__file__)


def create_all_tables():
    from like.config import get_settings
    from like.models.base import Base
    Base.metadata.create_all(bind=create_engine(get_settings().database_url))


if __name__ == '__main__':
    typer.run(create_all_tables)

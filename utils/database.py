"""Utils for database"""
from sqlalchemy import create_engine, Engine
from orm.git_stat import Base


def create_db_engine() -> Engine:
    """Create sqlite in memory database"""
    return create_engine("sqlite:///:memory:")


def create_tables(engine: Engine) -> None:
    """Create all required tables"""
    Base.metadata.create_all(engine)

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import Database


engine = create_engine(Database.full_url)


class Base(DeclarativeBase):
    def as_dict(self, *args) -> dict:
        """Converts an orm table object to a python dictionary

        Returns:
            dict: dict with ['column'] = value
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in args}


def get_sessionmaker(engine: Engine) -> sessionmaker:
    """Create sessionmaker for orm
    Example:
        session = get_sessionmaker(engine)
        
        with Session() as session:
            ...

    Args:
        engine (Engine): Engine for sqlalchemy

    Returns:
        sessionmaker: sessionmaker Class
    """
    return sessionmaker(engine)


def get_engine(url: str, create_new: bool = False) -> Engine:
    """Create Engine and tables for database

    Args:
        url (str): URL for connect database
        create_new (bool, optional): Create new tables or not, default not. Defaults to False.

    Returns:
        Engine: Engine for sqlalchemy
    """
    engine = create_engine(url)
    if create_new:
        __init_models(engine)
    return engine


def __init_models(engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

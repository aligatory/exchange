import pathlib
from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.util.compat import contextmanager


class Database:
    base: Any = declarative_base()
    engine: Optional[Engine] = None

    @staticmethod
    def create() -> None:
        cur_path = pathlib.Path('my.db').resolve()
        Database.engine = sa.create_engine('sqlite:////' + str(cur_path))
        def fk_pragma_on_connect(dbapi_con: Any, con_record: Any) -> None:
            dbapi_con.execute('pragma foreign_keys=ON')
        event.listen(Database.engine, 'connect', fk_pragma_on_connect)
        Database.base.metadata.create_all(Database.engine)


@contextmanager
def create_session(**kwargs: Any) -> Session:

    if Database.engine is None:
        raise EngineNotCreated("Invoke Database.create() firstly")
    session = sessionmaker(bind=Database.engine)
    new_session = session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


class EngineNotCreated(BaseException):
    pass

import pathlib
from typing import Any, Optional

from sqlalchemy.ext.declarative import as_declarative
import sqlalchemy as sa
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.util.compat import contextmanager

cur_path = pathlib.Path('my.db').resolve()
engine = sa.create_engine('sqlite:////' + str(cur_path))

Base = declarative_base(bind=engine)


def fk_pragma_on_connect(dbapi_con: Any, con_record: Any) -> None:
    # pylint: disable=unused-argument
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine, 'connect', fk_pragma_on_connect)


@contextmanager
def create_session(**kwargs: Any) -> Session:
    session = sessionmaker(bind=engine)
    new_session = session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


